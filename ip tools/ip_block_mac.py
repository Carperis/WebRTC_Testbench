# need to run with "sudo python3 ip_block_mac.py"

import os

ip = input('Enter the remote IP address to block: ')
with open('/etc/pf.conf', 'a') as file:
    line = f'block drop from any to {ip}\n'
    print(f"\n\"{line.strip()}\" is added to /etc/pf.conf\n")
    file.write(line)

cmd1 = "sudo pfctl -f /etc/pf.conf"
cmd2 = "sudo pfctl -e"
os.system(cmd1)
print(f">>> \"{cmd1}\" is executed to load PF config\n")
os.system(cmd2)
print(f">>> \"{cmd2}\" is executed to enable PF config\n")
