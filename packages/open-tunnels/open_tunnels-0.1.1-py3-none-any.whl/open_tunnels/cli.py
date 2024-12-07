import subprocess
import sqlite3
import uuid
import time
import shlex
import re
import ntplib
from datetime import datetime
import psutil
import signal
import sys
import os
import webbrowser
from jinja2 import Template

class TunnelManager:
    def __init__(self):
        self.db_name = 'runtime.db'
        self.time_servers = ['pool.ntp.org', 'time.nist.gov', 'time.google.com']
        self.active_tunnels = {}  # Keep track of active tunnels
        self._setup_database()
        # Register the exit handler
        signal.signal(signal.SIGINT, self.exit_handler)
        signal.signal(signal.SIGTERM, self.exit_handler)
    
    def _setup_database(self):
        # Initialize the database and tables
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tunnels (
                hex_code TEXT PRIMARY KEY,
                process_name TEXT,
                start_time TEXT,
                end_time TEXT,
                pids TEXT,
                url TEXT
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
    
    def start_tunnel(self, host, port):
        # Generate a unique hex code for this tunnel session
        hex_code = uuid.uuid4().hex
        process_name = f"cloudflared_tunnel_{hex_code}"
    
        # Command to start the Cloudflared tunnel
        command = f"cloudflared tunnel --url {host}:{port} --protocol http2"
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
    
        # Store session details in the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tunnels (hex_code, process_name, start_time, end_time, pids, url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            hex_code,
            process_name,
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            None,
            ','.join(map(str, pids)),
            url
        ))
        cursor.execute('''
            INSERT INTO urls (url, hex_code, start_time, end_time)
            VALUES (?, ?, ?, ?)
        ''', (
            url,
            hex_code,
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            None
        ))
        conn.commit()
        conn.close()

        # Keep track of active tunnels
        self.active_tunnels[hex_code] = pids
    
        print(f"\nTunnel started successfully!")
        print(f"URL: {url}")
        print(f"Hex Code: {hex_code}\n")
    
    def _get_process_tree_pids(self, parent_pid):
        # Retrieve all descendant PIDs of the parent process
        parent = psutil.Process(parent_pid)
        descendants = parent.children(recursive=True)
        pids = [parent_pid] + [child.pid for child in descendants]
        return pids
    
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
                end_time.strftime('%Y-%m-%d %H:%M:%S'),
                hex_code
            ))
            cursor.execute('''
                UPDATE urls SET end_time = ? WHERE hex_code = ?
            ''', (
                end_time.strftime('%Y-%m-%d %H:%M:%S'),
                hex_code
            ))
            conn.commit()
            print(f"\nTunnel with hex code {hex_code} has been stopped.\n")
            # Remove from active tunnels
            if hex_code in self.active_tunnels:
                del self.active_tunnels[hex_code]
        else:
            print(f"\nNo active tunnel found with hex code {hex_code}.\n")
        conn.close()
    
    def stop_all_tunnels(self):
        # Stop all active tunnels
        if self.active_tunnels:
            for hex_code in list(self.active_tunnels.keys()):
                self.stop_tunnel(hex_code)
            print("All active tunnels have been stopped.\n")
        else:
            print("No active tunnels to stop.\n")
    
    def exit_handler(self, signum, frame):
        # Handle program exit and terminate all tunnels
        print("\nGracefully shutting down all tunnels...")
        self.stop_all_tunnels()
        sys.exit(0)
    
    def get_tunnel_duration(self, hex_code):
        # Calculate how long the tunnel was active
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT start_time, end_time FROM tunnels WHERE hex_code = ?
        ''', (hex_code,))
        result = cursor.fetchone()
        conn.close()
        if result:
            start_time = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
            end_time_str = result[1]
            end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S') if end_time_str else self._get_network_time()
            duration = end_time - start_time
            return duration
        else:
            print(f"No tunnel found with hex code {hex_code}.")
            return None
    
    def list_all_urls(self):
        # List all URLs and their usage durations
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT url, hex_code, start_time, end_time FROM urls')
        results = cursor.fetchall()
        conn.close()
        url_list = []
        for url, hex_code, start_str, end_str in results:
            start_time = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S') if end_str else self._get_network_time()
            duration = end_time - start_time
            url_info = {
                'url': url,
                'hex_code': hex_code,
                'start_time': start_time,
                'end_time': end_time if end_str else None,
                'duration': duration
            }
            url_list.append(url_info)
        return url_list
    
    def generate_history_html(self):
        # Create an HTML file displaying all tunnel histories
        url_list = self.list_all_urls()
        template_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tunnel History</title>
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }
                header {
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                h1 {
                    margin: 0;
                }
                #search-container {
                    margin: 20px;
                    text-align: center;
                }
                #search-input {
                    width: 50%;
                    padding: 10px;
                    font-size: 16px;
                }
                table {
                    width: 90%;
                    margin: 20px auto;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 12px;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #4CAF50;
                    color: white;
                }
                tr:hover {
                    background-color: #f1f1f1;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                #detail-container {
                    display: none;
                    width: 80%;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .material-icons {
                    vertical-align: middle;
                    cursor: pointer;
                }
                .action-icons {
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 10px;
                }
                .hidden {
                    display: none;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Tunnel History</h1>
            </header>
            <div id="search-container">
                <input type="text" id="search-input" placeholder="Search by URL or Hex Code..." onkeyup="searchTable()">
            </div>
            <table id="tunnel-table">
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Hex Code</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {% for url_info in url_list %}
                    <tr onclick="showDetails('{{ url_info.url }}', '{{ url_info.hex_code }}', '{{ url_info.start_time }}', '{{ url_info.end_time }}', '{{ url_info.duration }}')">
                        <td>{{ url_info.url }}</td>
                        <td>{{ url_info.hex_code }}</td>
                        <td>{{ url_info.start_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                        <td>
                            {% if url_info.end_time %}
                                {{ url_info.end_time.strftime('%Y-%m-%d %H:%M:%S') }}
                            {% else %}
                                Active
                            {% endif %}
                        </td>
                        <td>{{ url_info.duration }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div id="detail-container">
                <h2>Tunnel Details</h2>
                <p><strong>URL:</strong> <span id="detail-url"></span></p>
                <p><strong>Hex Code:</strong> <span id="detail-hex"></span></p>
                <p><strong>Start Time:</strong> <span id="detail-start-time"></span></p>
                <p><strong>End Time:</strong> <span id="detail-end-time"></span></p>
                <p><strong>Duration:</strong> <span id="detail-duration"></span></p>
                <div class="action-icons">
                    <span class="material-icons" onclick="copyDetails()">content_copy</span>
                    <span class="material-icons" onclick="printDetails()">print</span>
                </div>
            </div>
            <script>
                function searchTable() {
                    var input, filter, table, tr, td, i, txtValue;
                    input = document.getElementById("search-input");
                    filter = input.value.toUpperCase();
                    table = document.getElementById("tunnel-table");
                    tr = table.getElementsByTagName("tr");
                    for (i = 1; i < tr.length; i++) {
                        tr[i].style.display = "none";
                        td = tr[i].getElementsByTagName("td");
                        for (var j = 0; j < td.length; j++) {
                            if (td[j]) {
                                txtValue = td[j].textContent || td[j].innerText;
                                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                                    tr[i].style.display = "";
                                    break;
                                }
                            }
                        }
                    }
                }
                function showDetails(url, hex, startTime, endTime, duration) {
                    document.getElementById('detail-url').innerText = url;
                    document.getElementById('detail-hex').innerText = hex;
                    document.getElementById('detail-start-time').innerText = startTime;
                    document.getElementById('detail-end-time').innerText = endTime || 'Active';
                    document.getElementById('detail-duration').innerText = duration;
                    document.getElementById('detail-container').style.display = 'block';
                }
                function copyDetails() {
                    var details = "URL: " + document.getElementById('detail-url').innerText + "\\n" +
                                  "Hex Code: " + document.getElementById('detail-hex').innerText + "\\n" +
                                  "Start Time: " + document.getElementById('detail-start-time').innerText + "\\n" +
                                  "End Time: " + document.getElementById('detail-end-time').innerText + "\\n" +
                                  "Duration: " + document.getElementById('detail-duration').innerText;
                    navigator.clipboard.writeText(details).then(function() {
                        alert('Details copied to clipboard.');
                    }, function(err) {
                        alert('Could not copy text: ', err);
                    });
                }
                function printDetails() {
                    var printContents = document.getElementById('detail-container').innerHTML;
                    var originalContents = document.body.innerHTML;
                    document.body.innerHTML = printContents;
                    window.print();
                    document.body.innerHTML = originalContents;
                    location.reload();
                }
            </script>
        </body>
        </html>
        '''
        template = Template(template_html)
        rendered_html = template.render(url_list=url_list)
        with open('history.html', 'w') as f:
            f.write(rendered_html)
        # Open the HTML file in the default web browser
        webbrowser.open('file://' + os.path.realpath('history.html'))
        print("\nHistory has been generated and opened in your web browser.\n")
    
    def run(self):
        while True:
            action = input("Enter 'start' to start a new tunnel, 'stop' to stop a tunnel, 'list' to list all URLs, or 'history' to view history: ").strip().lower()
            if action == 'start':
                host = input("Enter the host (e.g., localhost): ").strip()
                port = input("Enter the port number: ").strip()
                self.start_tunnel(host, port)
            elif action == 'stop':
                hex_code = input("Enter the hex code of the tunnel to stop or 'all' to stop all tunnels: ").strip()
                if hex_code == 'all':
                    self.stop_all_tunnels()
                else:
                    self.stop_tunnel(hex_code)
            elif action == 'list':
                urls = self.list_all_urls()
                for url_info in urls:
                    print(f"\nURL: {url_info['url']}")
                    print(f"Hex Code: {url_info['hex_code']}")
                    print(f"Start Time: {url_info['start_time']}")
                    print(f"End Time: {url_info['end_time'] if url_info['end_time'] else 'Active'}")
                    print(f"Duration: {url_info['duration']}")
                print("\n")
            elif action == 'history':
                self.generate_history_html()
            else:
                print("Invalid action. Please enter 'start', 'stop', 'list', or 'history'.")
    
    def __del__(self):
        # Destructor to ensure cleanup if object is destroyed
        self.stop_all_tunnels()

# Entry point for the script
if __name__ == "__main__":
    manager = TunnelManager()
    manager.run()
