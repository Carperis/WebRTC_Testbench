import subprocess
import threading
import time
import re
import os
import datetime
import noise_cancellation as nc


def read_action_from_file(file_path):
    with open(file_path, 'r') as file:
        actions = file.readlines()
    return [action.strip() for action in actions]


def record_time(str, time_dict):
    input(f"Press Enter @ {str}: ")
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    print(time_string)
    time_dict[time_string] = str
    return time_string


def get_filter(time1, time2=""):
    def modify_time(time_string, seconds):
        # original_time = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f%z")
        original_time = datetime.datetime.strptime(
            time_string, "%Y-%m-%d %H:%M:%S.%f")
        modified_time = original_time + datetime.timedelta(seconds=seconds)
        modified_time_string = modified_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        return modified_time_string

    delta_t = 0.5
    if time2 == "":
        return f"(frame.time >= \"{modify_time(time1, -delta_t)}\")"
    else:
        return f"(frame.time >= \"{modify_time(time1, -delta_t)}\" and frame.time <= \"{modify_time(time2, delta_t)}\")"


def interface_ctrl(devices, init=True):
    interfaces = {}
    for d in devices.keys():
        if init:
            command = "rvictl -s " + d
        else:
            command = "rvictl -x " + d
        try:
            result = subprocess.run(
                command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # print(f"Command '{command}' executed successfully.")
            if len(result.stdout.decode()) > 0:
                print(result.stdout.decode())

            if init:
                match = re.search(r'[\n\r].*with interface \s*([^\n\r]*)',
                                  result.stdout.decode())
                if match:
                    interfaces[d] = match.group(1)
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed.")
            print(e.stderr.decode())
    return interfaces


def tshark_init(tshark_dir, interface, traffic_dir):
    command = [tshark_dir, '-i', interface, '-w', traffic_dir]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Capturing " + interface + " traffic...")
    return process


def tshark_terminate(process):
    process.terminate()
    print("Terminating tshark process...")
    time.sleep(3)
    if process.poll() is not None:
        # Process has terminated
        returncode = process.returncode
        print("Process has terminated with return code:", returncode)
        return True
    else:
        # Process is still running
        print("Process is still running")
        return False


if __name__ == "__main__":
    app_name = "Discord"
    test_name = "O2O"
    test_round = 1
    noise_duration = 10
    actions = read_action_from_file("actions.txt")
    time_dict = {}
    devices = {
        "00008101-001A08392684001E": "caller",
        "00008027-000A50102106802E": "callee",
    }
    
    if (os.system('clear') == 1):
    os.system('cls')

    # Execute the initial commands
    interface_ctrl(devices, init=False)
    interfaces = interface_ctrl(devices)
    print(interfaces)

    process_list = []
    for d in interfaces.keys():
        cap_name = app_name + "_" + test_name + "_No" + \
            str(test_round) + "_" + str(devices[d]) + '.pcapng'
        process = tshark_init('tshark', interfaces[d], cap_name)
        process_list.append(process)

    if process_list:
        print("Capturing noise for " + str(noise_duration) + " seconds...")
        for remaining in range(noise_duration, 0, -1):
            print(f"Time remaining: {remaining} seconds" + " " * 5, end='\r')
            time.sleep(1)
        print("Noise capture is complete" + " " * 10 + "\n")

        for time_point in actions:
            record_time(time_point, time_dict)

        for process in process_list:
            tshark_terminate(process)
        interface_ctrl(devices, init=False)

        nc_filter_codes = []
        for d in interfaces.keys():
            cap_name = app_name + "_" + test_name + "_No" + \
                str(test_round) + "_" + str(devices[d]) + '.pcapng'
            nc_filter_codes.append(nc.main(cap_name, duration_seconds=noise_duration))

        # write to txt file
        file_name = app_name + "_" + test_name + \
            "_No" + str(test_round) + ".txt"
        with open(file_name, 'w') as file:
            print("\nDevices:")
            file.write("Devices:\n")
            for key in devices:
                print(f"{key}: {devices[key]},")
                file.write(f"{key}: {devices[key]},\n")
            
            print("\nActions:")
            file.write("\nActions:\n")
            for time_point in actions:
                print(time_point)
                file.write(time_point + "\n")
            
            print("\nSummary:")
            file.write("\nSummary:\n")
            for key in time_dict:
                print(f"{key}: { time_dict[key]}")
                file.write(f"{key}: { time_dict[key]}\n")
            times = list(time_dict.keys())
            print(f"\nFilter:\n{get_filter(times[0], times[-1])}")
            file.write(f"\nFilter:\n{get_filter(times[0], times[-1])}\n")
            for i in range(len(nc_filter_codes)):
                role = list(devices.values())[i]
                code = nc_filter_codes[i]
                print("\nNoise Cancellation Code ("+ role +")\n" + code)
                file.write("\nNoise Cancellation Code ("+ role +")\n" + code + "\n")
