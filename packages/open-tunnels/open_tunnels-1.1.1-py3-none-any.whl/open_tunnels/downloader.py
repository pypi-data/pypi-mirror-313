import os
import platform
import requests

def get_latest_version_info():
    version_url = "https://github.com/cloudflare/cloudflared/releases/latest"
    response = requests.get(version_url)
    if response.status_code == 200:
        version = response.url.split('/')[-1]
        return version
    else:
        print(f"Failed to get latest version info. Status code: {response.status_code}")
        return None

def get_system_type():
    system = platform.system().lower()
    architecture = platform.machine().lower()
    
    if 'windows' in system:
        if 'amd64' in architecture or 'x86_64' in architecture:
            return 'windows-amd64', 'cloudflared-windows-amd64.exe'
        elif 'arm64' in architecture or 'aarch64' in architecture:
            return 'windows-arm64', 'cloudflared-windows-arm64.exe'
        else:
            return "cloudflared"  , "cloudflared"
    return None, None

def download_cloudflared(destination_dir):
    latest_version = get_latest_version_info()
    if not latest_version:
        return None
    
    system_type, file_name = get_system_type()
    if not system_type or not file_name:
        print("Unsupported system type.")
        return None
    if not system_type == "cloudflared":

        release_file_path = os.path.join(destination_dir, f"release_{system_type}.txt")
        current_version = None

        if os.path.exists(release_file_path):
            with open(release_file_path, 'r') as file:
                current_version = file.read().strip()

        if current_version == latest_version:
            print(f"You already have the latest version of cloudflared for {system_type}.")
            return os.path.join(destination_dir, file_name)

        url = f"https://github.com/cloudflare/cloudflared/releases/download/{latest_version}/{file_name}"
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(destination_dir, file_name)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            with open(release_file_path, 'w') as file:
                file.write(latest_version)
            print(f"Downloaded {file_name} for {system_type} to {file_path}")
            print(f"Updated release_{system_type}.txt with version {latest_version}")
            return file_path
        else:
            print(f"Failed to download {file_name}. Status code: {response.status_code}")
            return None
    else:
        return "cloudflared"

