import socket

def get_local_ip():
    try:
        # Create a temporary socket
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))  # Connect to a known external server

        # Get the local IP address
        local_ip = temp_socket.getsockname()[0]

        # Close the temporary socket
        temp_socket.close()

        return local_ip
    except socket.error:
        return "Unable to retrieve local IP"

# Call the function to get the local IP address
ip_address = get_local_ip()
print("Local IP address:", ip_address)

