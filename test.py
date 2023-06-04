import sys

def identify_os():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'Mac OS'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    else:
        return 'Unknown'

# Identify the operating system
os = identify_os()

# Display the result
print(f"Operating System: {os}")
