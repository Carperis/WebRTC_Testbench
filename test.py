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
