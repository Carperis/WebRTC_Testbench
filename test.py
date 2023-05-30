import subprocess
import threading

stop_flag = False

# Run Tshark command and capture the output
def capture_traffic(interface):
    tshark_dir = "D:\\Wireshark\\tshark"
    command = [tshark_dir, '-i', interface, '-w', 'captured_traffic.pcapng']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode('utf-8')
        if not output or stop_flag:
            break
        print(output.strip())

    process.terminate()
    _, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode('utf-8')}")

# Specify the network interface to capture traffic from
interface = 'WLAN'

# Start capturing traffic using Tshark in a separate thread
capture_thread = threading.Thread(target=capture_traffic, args=(interface,))
capture_thread.start()

# Wait for user input to stop capturing
input("Press Enter to stop capturing...")

# Set the stop flag to stop capturing
stop_flag = True
print (stop_flag)

# Wait for the capture thread to complete
capture_thread.join()

print("Capture completed. Saved to captured_traffic.pcapng")
