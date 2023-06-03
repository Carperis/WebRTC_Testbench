# Need to run vscode or cmd as administrator

import subprocess

ip_address = input("Enter the remote IP address to block: ")
try:
    # Execute netsh command to add a firewall rule
    command = f"netsh advfirewall firewall add rule name=\"BLOCK IP ADDRESS - {ip_address}\" dir=out action=block remoteip={ip_address}"
    subprocess.run(command, shell=True, check=True)
    print(f"Blocked traffic to {ip_address}")
except subprocess.CalledProcessError as e:
    print(f"Error blocking traffic to {ip_address}: {e}")


