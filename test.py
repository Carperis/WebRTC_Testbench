import datetime

def record_time():
    input("Press Enter to record the time...")
    current_time = datetime.datetime.now()
    time_format = current_time.strftime("%Y-%m-%d %H:%M:%S.%f %Z")
    print("Recorded time:", time_format)

record_time()
