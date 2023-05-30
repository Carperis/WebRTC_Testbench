import subprocess
import time
import os

# Run Tshark command and capture the output
def capture_traffic(interface):
    tshark_dir = "D:\\Wireshark\\tshark"
    command = [tshark_dir, '-i', interface, '-a', f'duration:10', '-w', 'captured_traffic.pcapng']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    _, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode('utf-8')}")

# Specify the network interface to capture traffic from
interface = 'WLAN'

# Start capturing traffic using Tshark
capture_traffic(interface)

print("Capture completed. Saved to captured_traffic.pcapng")

# Wait for a few seconds to allow the process to release the file lock
time.sleep(5)

# Delete the pcapng file
file_path = 'captured_traffic.pcapng'
try:
    os.remove(file_path)
    print(f"Deleted {file_path}")
except FileNotFoundError:
    print(f"File {file_path} not found")
except OSError as e:
    print(f"Error occurred while deleting {file_path}: {e}")

