import datetime
import time
import os

# make sure all devices are in the same time zone, and the time is synced.


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


if (os.system('clear') == 1):
    os.system('cls')

time_points = [
    "Caller initiates a call link and joins the call.",
    "Callee joins the call.",
    "Callee closes the camera.",
    "Callee reopens the camera.",
    "Caller leaves the call.",
    "Caller rejoins the call.",
    "Caller switches to cellular network.",
    "Caller leaves the call.",
    "Caller rejoins the call.",
    "Caller switches back to wifi.",
    "Caller leaves the call.",
    "Callee leaves the call."
]


time_dict = {}

for time_point in time_points:
    record_time(time_point, time_dict)

print("\nSummary:")
for key in time_dict:
    print(f"{key}: { time_dict[key]}")

times = list(time_dict.keys())
print("\nFilter:")
print(get_filter(times[0], times[-1]))
