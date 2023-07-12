import datetime
import time
import os

time_dict = {}


def record_time(str):
    input(f"Press Enter to record {str}: ")
    current_time = datetime.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    print(f"{str}: ", time_string)
    time_dict[str] = time_string
    return time_string


if (os.system('clear') == 1):
    os.system('cls')

caller_start_time = record_time("caller start time")
receiver_start_time = record_time("receiver start time")
# leave_1 = record_time("receiver leave 1")
# rejoin_1 = record_time("receiver rejoin 1")
# leave_2 = record_time("receiver leave 2")
# rejoin_2 = record_time("receiver rejoin 2")
receiver_end_time = record_time("receiver end time")
caller_end_time = record_time("caller end time")

print("\nSummary:")
for key in time_dict:
    print(f"{key}: ", time_dict[key])


def modify_time(time_string, seconds):
    # original_time = datetime.datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f%z")
    original_time = datetime.datetime.strptime(
        time_string, "%Y-%m-%d %H:%M:%S.%f")
    modified_time = original_time + datetime.timedelta(seconds=seconds)
    modified_time_string = modified_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    return modified_time_string


delta_t = 0.5
print("\nFilter:")
print(
    f"caller: (frame.time >= \"{modify_time(caller_start_time, -delta_t)}\" and frame.time <= \"{modify_time(caller_end_time, delta_t)}\")")
print(
    f"receiver: (frame.time >= \"{modify_time(receiver_start_time, -delta_t)}\" and frame.time <= \"{modify_time(receiver_end_time, delta_t)}\")")
