# need to run with "sudo python3 ip_unblock_mac.py"

import os

# Read the contents of the file into a list
with open('/etc/pf.conf', 'r') as file:
    old_lines = file.readlines()

# Remove the last line that matches the specific text
ip = input('Enter the remote IP address to unblock: ')
target_line = f'block drop from any to {ip}'
new_lines = [line for line in old_lines if not line.strip() == target_line]
if (old_lines == new_lines):
    print(f"\n\"{target_line.strip()}\" is not found in /etc/pf.conf\n")
else:
    print(f"\n\"{target_line.strip()}\" is removed from /etc/pf.conf\n")

# Write the modified list back to the file
with open('/etc/pf.conf', 'w') as file:
    file.writelines(new_lines)
    
cmd1 = "sudo pfctl -f /etc/pf.conf"
cmd2 = "sudo pfctl -e"
os.system(cmd1)
print(f">>> \"{cmd1}\" is executed to load PF config\n")
os.system(cmd2)
print(f">>> \"{cmd2}\" is executed to enable PF config\n")
