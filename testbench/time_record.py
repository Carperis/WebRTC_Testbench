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
    "Client A joins a channel and opens the camera.",
    "Client B joins the channel and opens the camera.",
    "Client C joins the channel and opens the camera.",
    "Client A closes the camera.",
    "Client A reopens the camera.",
    "Client A switches to cellular network.",
    "Client A leaves the channel.",
    "Client A rejoins the channel.",
    "Client A switches back to wifi.",
    "Client C leaves the channel.",
    "Client C joins a new channel.",
    "Client A leaves the old channel.",
    "Client A joins the new channel.",
    "Client A switches to the old channel.",
    "Client A switches to the new channel.",
    "Client B leaves the old channel.",
    "Client B joins the new channel.",
    "Client A leaves the new channel.",
    "Client B leaves the new channel.",
    "Client C leaves the new channel."
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
