import block_ip
import unblock_ip
import get_local_ip
import ping_test
import time
import threading
import os

max_time = 120 # seconds
local_ip = get_local_ip.get_local_ip()
ip = input('Enter the remote IP address to block: ')
print("\n[Test IP 1]----------------------------------------\n")

test1 = ping_test.perform_ping_test(ip)
if (test1 == True):
    print(f"Before blocking: Ping test to {ip} was successful!")
else:
    print(f"Before blocking: Ping test to {ip} failed.")
print("\n[Block IP]----------------------------------------\n")

block_ip.block_ip(ip)
print("\n[Test IP 2]----------------------------------------\n")

test2 = ping_test.perform_ping_test(ip)
if (test2 == True):
    print(f"After blocking: Ping test to {ip} was successful!")
else:
    print(f"After blocking: Ping test to {ip} failed.")
print("\n[Waiting]----------------------------------------\n")

def timer(stop_event, max_time, current_time):
    t = 0
    while t < max_time and not stop_event.is_set():
        print(f"Time left: {max_time - t} seconds", end="\r")
        t += 1
        current_time[0] = t
        time.sleep(1)  # Delay of 1 second between counts

    print(f"Time used: {t} seconds")
    print("\n[Unblock IP]----------------------------------------\n")

    unblock_ip.unblock_ip(ip)
    print("\n[Test IP 3]----------------------------------------\n")

    test3 = ping_test.perform_ping_test(ip)
    if (test3 == True):
        print(f"After unblocking: Ping test to {ip} was successful!")
    else:
        print(f"After unblocking: Ping test to {ip} failed.")
    os._exit(1)
    
    

def manual_stop_timer(stop_event, ip, t):
    time.sleep(1)
    user_input = input(f"Enter 'q' to unblock {ip}: \n")
    print(f"Your input was: {user_input}")
    while(user_input != 'q'):
        user_input = input("Enter 'q' to unblock {ip}: \n")
        print(f"Your input was: {user_input}")
    stop_event.set()
    print(f"Time used: {t[0]} seconds")
    print("\n[Unblock IP]----------------------------------------\n")

    unblock_ip.unblock_ip(ip)
    print("\n[Test IP 3]----------------------------------------\n")

    test3 = ping_test.perform_ping_test(ip)
    if (test3 == True):
        print(f"After unblocking: Ping test to {ip} was successful!")
    else:
        print(f"After unblocking: Ping test to {ip} failed.")
    os._exit(1)

current_time = [None]
stop_event = threading.Event()
count_thread = threading.Thread(target=timer, args=(stop_event, max_time, current_time))
input_thread = threading.Thread(target=manual_stop_timer, args=(stop_event,ip, current_time))
input_thread.start()
count_thread.start()