import subprocess
from tabulate import tabulate

def run_command(command: str) -> str:
    """Execute a system command and return the output."""
    return subprocess.getoutput(command)

def get_wifi_profiles() -> list:
    """Retrieve a list of Wi-Fi profiles."""
    wifi_info = run_command("netsh wlan show profiles").split("\n")
    return [line.split(":")[1].strip() for line in wifi_info if "All User Profile" in line]

def get_wifi_passwords(wifi_list: list) -> list:
    """Retrieve passwords for a list of Wi-Fi profiles."""
    wifi_details = []
    for wifi in wifi_list:
        keys = run_command(f'netsh wlan show profiles name="{wifi}" key=clear').split("\n")
        password = next((line.split(":")[1].strip() for line in keys if "Key Content" in line), "N/A")
        wifi_details.append({"name": wifi, "password": password})
    return wifi_details

def display_wifi_passwords():
    """Fetch and display Wi-Fi names and passwords in a tabular format."""
    wifi_list = get_wifi_profiles()
    wifi_details = get_wifi_passwords(wifi_list)
    return wifi_details
    