import sqlite3
import subprocess
import shlex
import re
import threading
import time
import uuid
import psutil
import ntplib
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, abort
from flask_session import Session
from . import downloader # Use relative import
import os

app = Flask(__name__)

# Configure secret key and session
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class TokenManager:
    def __init__(self):
        self.db_name = 'tokens.db'
        self._setup_database()

    def _setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                expiry DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def generate_token(self):
        token = uuid.uuid4().hex
        expiry = datetime.now() + timedelta(minutes=30)  # Token expires after 30 minutes
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tokens (token, expiry) VALUES (?, ?)', (token, expiry))
        conn.commit()
        conn.close()
        return token

    def validate_token(self, token):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT expiry FROM tokens WHERE token = ?', (token,))
        result = cursor.fetchone()
        conn.close()
        if result:
            expiry = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S.%f')
            if expiry > datetime.now():
                return True
            else:
                self.revoke_token(token)
        return False

    def revoke_token(self, token):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tokens WHERE token = ?', (token,))
        conn.commit()
        conn.close()

token_manager = TokenManager()

class TunnelManager:
    def __init__(self):
        self.db_name = 'runtime.db'
        self.time_servers = ['pool.ntp.org', 'time.nist.gov', 'time.google.com']
        self.active_tunnels = {}  # Keep track of active tunnels
        self._setup_database()
        self._mark_stopped_tunnels_on_startup()
        # Start background thread to monitor tunnels
        threading.Thread(target=self._monitor_tunnels, daemon=True).start()

    def _setup_database(self):
        # Initialize the database and tables
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tunnels (
                tunnel_name TEXT,
                hex_code TEXT PRIMARY KEY,
                process_name TEXT,
                start_time TEXT,
                end_time TEXT,
                pids TEXT,
                url TEXT,
                host TEXT,
                port TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                url TEXT,
                hex_code TEXT,
                start_time TEXT,
                end_time TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _mark_stopped_tunnels_on_startup(self):
        # On startup, mark all tunnels as stopped since the processes are no longer running
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT hex_code, pids FROM tunnels WHERE end_time IS NULL')
        results = cursor.fetchall()
        for hex_code, pids in results:
            pid_list = list(map(int, pids.split(',')))
            running = False
            for pid in pid_list:
                if psutil.pid_exists(pid):
                    running = True
                    break
            if not running:
                # Tunnel is not running; update end_time
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cursor.execute('''
                    UPDATE tunnels SET end_time = ? WHERE hex_code = ?
                ''', (end_time, hex_code))
                cursor.execute('''
                    UPDATE urls SET end_time = ? WHERE hex_code = ?
                ''', (end_time, hex_code))
        conn.commit()
        conn.close()

    def _get_network_time(self):
        # Fetch current time from multiple NTP servers
        for server in self.time_servers:
            try:
                client = ntplib.NTPClient()
                response = client.request(server, version=3)
                return datetime.fromtimestamp(response.tx_time)
            except:
                continue
        # Fallback to local system time if all NTP servers fail
        return datetime.now()

    def _extract_url(self, line):
        # Use regex to find the Cloudflared URL in the output
        match = re.search(r'https://.*?\.trycloudflare\.com', line)
        if match:
            return match.group(0)
        return None

    def start_tunnel(self, tunnel_name, host, port):
        # Check if tunnel name is unique or the previous tunnel with the same name has stopped
        if not self._can_use_tunnel_name(tunnel_name):
            return {'error': 'Tunnel name is already in use by an active tunnel.'}

        # Generate a unique hex code for this tunnel session
        hex_code = uuid.uuid4().hex
        process_name = f"cloudflared_tunnel_{hex_code}"

        # Command to start the Cloudflared tunnel
        with open("driver.txt" , "r") as drive:
           driver_path = drive.read()
        drive.close()
        command = f'"{driver_path}" tunnel --url {host}:{port} --protocol http2'
        args = shlex.split(command)

        # Start the subprocess
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Record the start time using network time
        start_time = self._get_network_time()

        # Capture all related process IDs
        pids = self._get_process_tree_pids(process.pid)

        # Monitor output to extract the URL
        url = None
        while True:
            line = process.stdout.readline()
            if line:
                url = self._extract_url(line)
                if url:
                    break
            elif process.poll() is not None:
                # Process has terminated
                break
            else:
                time.sleep(0.1)

        if not url:
            return {'error': 'Failed to start tunnel. Please check your Cloudflared installation.'}

        # Store session details in the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tunnels (tunnel_name, hex_code, process_name, start_time, end_time, pids, url, host, port)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tunnel_name,
            hex_code,
            process_name,
            start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            None,
            ','.join(map(str, pids)),
            url,
            host,
            port
        ))
        cursor.execute('''
            INSERT INTO urls (url, hex_code, start_time, end_time)
            VALUES (?, ?, ?, ?)
        ''', (
            url,
            hex_code,
            start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            None
        ))
        conn.commit()
        conn.close()

        # Keep track of active tunnels
        self.active_tunnels[hex_code] = {
            'pids': pids,
            'process': process
        }

        return {
            'success': True,
            'url': url,
            'hex_code': hex_code,
            'tunnel_name': tunnel_name,
            'host': host,
            'port': port,
            'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def _can_use_tunnel_name(self, tunnel_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT tunnel_name, end_time FROM tunnels WHERE tunnel_name = ?', (tunnel_name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            # Allow reuse if the previous tunnel with the same name has ended
            if result[1] is not None:
                return True
            else:
                return False
        else:
            return True

    def _get_process_tree_pids(self, parent_pid):
        # Retrieve all descendant PIDs of the parent process
        try:
            parent = psutil.Process(parent_pid)
            descendants = parent.children(recursive=True)
            pids = [parent_pid] + [child.pid for child in descendants]
            return pids
        except psutil.NoSuchProcess:
            return [parent_pid]

    def stop_tunnel(self, hex_code):
        # Fetch the PIDs associated with the hex code
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT pids FROM tunnels WHERE hex_code = ?', (hex_code,))
        result = cursor.fetchone()
        if result:
            pids = list(map(int, result[0].split(',')))
            # Terminate all processes
            for pid in pids:
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                except psutil.NoSuchProcess:
                    continue
            # Update the end time in the database
            end_time = self._get_network_time()
            cursor.execute('''
                UPDATE tunnels SET end_time = ? WHERE hex_code = ?
            ''', (
                end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                hex_code
            ))
            cursor.execute('''
                UPDATE urls SET end_time = ? WHERE hex_code = ?
            ''', (
                end_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                hex_code
            ))
            conn.commit()
            # Remove from active tunnels
            if hex_code in self.active_tunnels:
                try:
                    self.active_tunnels[hex_code]['process'].terminate()
                except:
                    pass
                del self.active_tunnels[hex_code]
            conn.close()
            return True
        else:
            conn.close()
            return False

    def list_all_tunnels(self):
        # List all tunnels and their usage durations
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tunnels ORDER BY start_time DESC')
        results = cursor.fetchall()
        conn.close()
        tunnel_list = []
        serial_number = 1  # Start serial number from 1
        for row in results:
            tunnel_name = row[0]
            hex_code = row[1]
            url = row[6]
            host = row[7]
            port = row[8]
            start_time = row[3]
            end_time = row[4]
            start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            if end_time:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                duration = str(end_dt - start_dt)
                status = 'Stopped'
            else:
                end_dt = None
                duration = str(datetime.now() - start_dt)
                status = 'Active'
            tunnel_info = {
                'serial_number': serial_number,
                'tunnel_name': tunnel_name,
                'hex_code': hex_code,
                'url': url,
                'host': host,
                'port': port,
                'status': status,
                'start_time': start_dt.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_dt.strftime('%Y-%m-%d %H:%M:%S') if end_dt else '',
                'duration': duration.split('.')[0]
            }
            tunnel_list.append(tunnel_info)
            serial_number += 1  # Increment serial number
        return tunnel_list

    def get_active_tunnels_over_time(self):
        # Calculate the number of active tunnels over time
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT start_time, end_time FROM tunnels
        ''')
        results = cursor.fetchall()
        conn.close()

        time_events = []

        for start_time, end_time in results:
            start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            time_events.append((start_dt, 1))  # Tunnel starts, +1
            if end_time:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                time_events.append((end_dt, -1))  # Tunnel ends, -1

        # Sort events by time
        time_events.sort(key=lambda x: x[0])

        times = []
        active_counts = []
        current_count = 0
        for t, change in time_events:
            current_count += change
            times.append(t.strftime('%Y-%m-%d %H:%M:%S'))
            active_counts.append(current_count)

        return {'times': times, 'active_counts': active_counts}

    def get_tunnel_durations(self):
        # Get the durations of all tunnels
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT start_time, end_time FROM tunnels
        ''')
        results = cursor.fetchall()
        conn.close()

        durations = []
        for start_time, end_time in results:
            start_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            if end_time:
                end_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
            else:
                end_dt = datetime.now()
            duration = end_dt - start_dt
            durations.append(duration.total_seconds() / 60)  # Duration in minutes

        return durations

    def get_host_port_usage(self):
        # Get counts of tunnels per host and port
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT host, COUNT(*) FROM tunnels GROUP BY host
        ''')
        host_data = cursor.fetchall()
        cursor.execute('''
            SELECT port, COUNT(*) FROM tunnels GROUP BY port
        ''')
        port_data = cursor.fetchall()
        conn.close()

        hosts = [row[0] for row in host_data]
        host_counts = [row[1] for row in host_data]

        ports = [row[0] for row in port_data]
        port_counts = [row[1] for row in port_data]

        return {'hosts': hosts, 'host_counts': host_counts, 'ports': ports, 'port_counts': port_counts}

    def _monitor_tunnels(self):
        # Monitor active tunnels and remove any that have terminated
        while True:
            hex_codes = list(self.active_tunnels.keys())
            for hex_code in hex_codes:
                try:
                    process = self.active_tunnels[hex_code]['process']
                    if process.poll() is not None:
                        # Process has terminated
                        self.stop_tunnel(hex_code)
                except Exception as e:
                    # In case the process is not accessible, remove it
                    self.stop_tunnel(hex_code)
            time.sleep(5)

    def stop_all_tunnels(self):
        # Stop all active tunnels
        hex_codes = list(self.active_tunnels.keys())
        for hex_code in hex_codes:
            self.stop_tunnel(hex_code)

tunnel_manager = TunnelManager()

def token_required(f):
    def wrap(*args, **kwargs):
        token = session.get('token')
        if token and token_manager.validate_token(token):
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized access. Please refresh the page.'}), 401
    wrap.__name__ = f.__name__
    return wrap

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def dashboard():
    if 'token' not in session or not token_manager.validate_token(session['token']):
        token = token_manager.generate_token()
        session['token'] = token
    return render_template('dash.html')

@app.route('/start_tunnel', methods=['POST'])
@token_required
def start_tunnel_route():
    data = request.get_json()
    tunnel_name = data.get('tunnel_name')
    host = data.get('host')
    port = data.get('port')
    result = tunnel_manager.start_tunnel(tunnel_name, host, port)
    return jsonify(result)

@app.route('/stop_tunnel', methods=['POST'])
@token_required
def stop_tunnel_route():
    data = request.get_json()
    hex_code = data.get('hex_code')
    success = tunnel_manager.stop_tunnel(hex_code)
    return jsonify({'success': success})

@app.route('/list_tunnels', methods=['GET'])
@token_required
def list_tunnels_route():
    tunnels = tunnel_manager.list_all_tunnels()
    return jsonify(tunnels)

@app.route('/tunnel_details/<hex_code>', methods=['GET'])
@token_required
def get_tunnel_details(hex_code):
    # Fetch tunnel details from the database
    conn = sqlite3.connect(tunnel_manager.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tunnels WHERE hex_code = ?', (hex_code,))
    result = cursor.fetchone()
    conn.close()
    if result:
        start_dt = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S.%f')
        if result[4]:
            end_dt = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S.%f')
            duration = str(end_dt - start_dt)
            status = 'Stopped'
        else:
            duration = str(datetime.now() - start_dt)
            status = 'Active'
        tunnel_info = {
            'tunnel_name': result[0],
            'hex_code': result[1],
            'url': result[6],
            'host': result[7],
            'port': result[8],
            'start_time': start_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_dt.strftime('%Y-%m-%d %H:%M:%S') if result[4] else 'Active',
            'status': status,
            'duration': duration.split('.')[0]
        }
        return jsonify(tunnel_info)
    else:
        return jsonify({'error': 'Tunnel not found'}), 404

@app.route('/details/<hex_code>')
def tunnel_details(hex_code):
    if 'token' not in session or not token_manager.validate_token(session['token']):
        token = token_manager.generate_token()
        session['token'] = token
    return render_template('details.html', hex_code=hex_code)

@app.route('/tunnels')
def tunnels():
    if 'token' not in session or not token_manager.validate_token(session['token']):
        token = token_manager.generate_token()
        session['token'] = token
    return render_template('tunnels.html')

@app.route('/search_tunnels', methods=['GET'])
@token_required
def search_tunnels():
    query = request.args.get('q', '').lower()
    all_tunnels = tunnel_manager.list_all_tunnels()
    filtered_tunnels = []
    for tunnel in all_tunnels:
        if (query in tunnel['tunnel_name'].lower() or
            query in tunnel['hex_code'].lower() or
            query in tunnel['url'].lower()):
            filtered_tunnels.append(tunnel)
    return jsonify(filtered_tunnels)

@app.route('/chart_data', methods=['GET'])
@token_required
def chart_data():
    # Data for Tunnels Started Over Time
    conn = sqlite3.connect(tunnel_manager.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT date(start_time), COUNT(*) FROM tunnels GROUP BY date(start_time)')
    data = cursor.fetchall()
    chart1_data = {
        'labels': [row[0] for row in data],
        'values': [row[1] for row in data]
    }

    # Data for Active Tunnels Over Time
    active_tunnels_data = tunnel_manager.get_active_tunnels_over_time()

    # Data for Tunnel Durations
    durations = tunnel_manager.get_tunnel_durations()

    # Data for Host and Port Usage
    host_port_data = tunnel_manager.get_host_port_usage()

    return jsonify({
        'chart1_data': chart1_data,
        'active_tunnels_data': active_tunnels_data,
        'durations': durations,
        'host_port_data': host_port_data
    })

@app.route('/shutdown', methods=['GET'])
def shutdown():
    tunnel_manager.stop_all_tunnels()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    return 'Server shutting down...'

if __name__ == '__main__':
    driver = downloader.download_cloudflared(os.path.join(os.getcwd() , "driver"))
    with open("driver.txt" , "w") as drive:
        drive.write(driver)
    drive.close()
    app.run(port = 6700 , host = "0.0.0.0")
