import subprocess
import os
import time


def start_wireshark():
    # Change directory to the location of tshark.exe
    tshark_dir = "D:\\Wireshark\\"  # Replace with the actual directory path
    os.chdir(tshark_dir)
    
    # Define the TShark command
    interface = "WLAN"
    # Replace 'eth0' with the desired interface
    tshark_cmd = ['tshark', '-i', interface]

    # Start TShark process
    process = subprocess.Popen(
        tshark_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read the captured output
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            # Process the output as desired
            print(output.strip())

    # Wait for the process to finish
    process.wait()

    # Check for any errors
    if process.returncode != 0:
        print(f"An error occurred: {process.stderr.read().decode('utf-8')}")


if __name__ == "__main__":
    # calculate run time
    start = time.time()
    start_wireshark()
    end = time.time()
    print("Run time: ", end - start)
