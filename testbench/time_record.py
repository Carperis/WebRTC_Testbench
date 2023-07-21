import datetime
import time
import os

# make sure all devices are in the same time zone, and the time is synced.


def record_time(str):
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
    "Client C initiates a meeting link, shares the link to Client A and Client B, and joins the room.",
    "Client B joins the room.",
    "Client A joins the room.",
    "Client B closes the camera.",
    "Client B reopens the camera.",
    "Client A switches to cellular network.",
    "Client A leaves the room.",
    "Client A rejoins the room.",
    "Client A switches back to wifi.",
    "Client C leaves the room.",
    "Client C initiates a new meeting link, shares the link to Client A and Client B, and joins the room.",
    "Client A leaves the old room.",
    "Client A joins the new room.",
    "Client A leaves the new room (switch from).",
    "Client A rejoins the old room (switch to).",
    "Client B leaves the old room.",
    "Client B joins the new room.",
    "Client A leaves the old room (switch from).",
    "Client A rejoins the new room (switch to).",
    "Client A leaves the new room.",
    "Client B leaves the new room.",
    "Client C leaves the new room."
]

time_dict = {}

for time_point in time_points:
    record_time(time_point)

print("\nSummary:")
for key in time_dict:
    print(f"{key}: { time_dict[key]}")

times = list(time_dict.keys())
print("\nFilter:")
print(get_filter(times[0], times[-1]))
