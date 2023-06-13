import re

def is_ipv4(text):
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv4_addresses = re.findall(ipv4_pattern, text)
    if ipv4_addresses:
        return True
    else:
        return False

def is_ipv6(text):
    ipv6_pattern = r'\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b|\b(?:[0-9A-Fa-f]{1,4}:){0,6}(?:(?:[0-9A-Fa-f]{1,4}:){1,6})?:[0-9A-Fa-f]{1,4}\b'
    ipv6_addresses = re.findall(ipv6_pattern, text)
    if ipv6_addresses:
        return True
    else:
        return False

def generate_display_filter(ip_addresses):
    display_filter = ''
    for ip_address in ip_addresses:
        if display_filter:
            display_filter += ' or '
        if (is_ipv4(ip_address)):
            display_filter += f'ip.src == {ip_address} or ip.dst == {ip_address}'
        elif (is_ipv6(ip_address)):
            display_filter += f'ipv6.src == {ip_address} or ipv6.dst == {ip_address}'
    return display_filter

# Example usage:
ip_list = ['10.239.161.0', '157.240.245.58', '157.240.245.22', '157.240.240.58', '204.8.153.51', '10.192.48.247', '31.13.80.3', '128.197.29.224']
display_filter = generate_display_filter(ip_list)
print("\n" + display_filter + "\n")

