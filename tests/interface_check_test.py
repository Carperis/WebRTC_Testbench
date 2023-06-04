import netifaces

def get_active_interface():
    gateways = netifaces.gateways()
    default_gateway = gateways['default']

    for interface, details in default_gateway.items():
        if details[1] is not None:
            return details[1]

    return None

# Get the active interface
active_interface = get_active_interface()

# Print the active interface
if active_interface is not None:
    print(f"The active interface is: {active_interface}")
else:
    print("No active interface found.")

import psutil

def get_most_active_interface():
    interfaces = psutil.net_io_counters(pernic=True)
    most_active_interface = None
    max_bytes_sent = 0

    for interface, stats in interfaces.items():
        bytes_sent = stats.bytes_sent
        bytes_recv = stats.bytes_recv
        if (bytes_sent == bytes_recv):
            continue
        if (bytes_sent > max_bytes_sent):
            max_bytes_sent = bytes_sent
            most_active_interface = interface
            
    return most_active_interface

# Call the function to get the most active interface
active_interface = get_most_active_interface()
print("Most Active Interface:", active_interface)