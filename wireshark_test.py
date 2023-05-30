import subprocess
import os
import time

base_dir = "C:\\Users\\Sam\\Desktop\\WebRTC_Testbench"
tshark_dir = "D:\\Wireshark\\tshark"
interface = "WLAN"
traffic_dir = base_dir + "\\captured_traffic.pcapng"


def start_wireshark():

    # Define the TShark command
    interface = "WLAN"
    # Replace 'eth0' with the desired interface
    command = [tshark_dir, '-i', interface, '-w', traffic_dir]

    # Start TShark process
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # # Read the captured output
    # start = time.time()
    # while True:
    #     end = time.time()
    #     print(end - start)
    #     if end - start > 10:
    #         break
    #     output = process.stdout.readline().decode('utf-8')
    #     print(output.strip())
    time.sleep(5)

    process.terminate()
    print("Process terminated")
    # Check for any errors
    # if process.returncode != 0:
    #     print(f"An error occurred: {process.stderr.read().decode('utf-8')}")
    time.sleep(5)
    if process.poll() is not None:
    # Process has terminated
        returncode = process.returncode
        print("Process has terminated with return code:", returncode)
    else:
        # Process is still running
        print("Process is still running")


if __name__ == "__main__":
    # calculate run time
    start = time.time()
    start_wireshark()
    try:
        os.remove(traffic_dir)
        print(f"Deleted {traffic_dir}")
    except FileNotFoundError:
        print(f"File {traffic_dir} not found")
    except OSError as e:
        print(f"Error occurred while deleting {traffic_dir}: {e}")
    end = time.time()
    print("Run time: ", end - start)
