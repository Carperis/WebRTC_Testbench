import subprocess

def perform_ping_test(host):
    # Run the ping command
    result = subprocess.run(['ping', host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Check the return code
    if result.returncode == 0:
        # Ping was successful
        return True
    else:
        # Ping failed
        return False

# Perform the ping test
host = '8.8.8.8'
ping_success = perform_ping_test(host)

# Display the result
if ping_success:
    print(f"Ping test to {host} was successful!")
else:
    print(f"Ping test to {host} failed.")
