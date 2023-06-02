import threading
import time

# Event to synchronize Thread A and Thread B
event = threading.Event()

# Flag to indicate when Thread A has ended
thread_a_ended = False

# Function to be executed in Thread A
def thread_a():
    global thread_a_ended

    for i in range(1, 11):
        print(f" Thread A counter: {i} sec")
        time.sleep(1)

        if i == 5:
            event.set()  # Signal Thread B to start

    thread_a_ended = True  # Set the flag to indicate Thread A has ended
    event.set()  # Signal Thread B to end
    print(" Thread A ended")

# Function to be executed in Thread B
def thread_b():
    while True:
        event.wait()  # Wait for Thread A to signal
        event.clear()  # Reset the event

        for i in range(50, 61):
            print(f" Thread B counter: {i} sec")
            time.sleep(1)

            if event.is_set() or thread_a_ended:
                break  # Exit the loop if Thread A signals or ends

        if not event.is_set():
            break  # Exit the loop if Thread A ends

    print(" Thread B ended")

# Create and start Thread A
thread_a = threading.Thread(target=thread_a)
thread_a.start()

# Create and start Thread B
thread_b = threading.Thread(target=thread_b)
thread_b.start()

# Wait for Thread A to complete
thread_a.join()

# Wait for Thread B to complete
thread_b.join()

print("All threads completed")
