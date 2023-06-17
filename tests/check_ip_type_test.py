import ipaddress

def check_ip_address_type(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        if ip.is_private:
            return "Private"
        else:
            return "Public"
    except ValueError:
        return "Invalid IP address"

# Example usage:
ip_list = ['239.255.255.250', '157.240.245.58', '157.240.245.22', '157.240.240.58', '204.8.153.51', '10.192.48.247', '31.13.80.3', '128.197.29.224']
for address in ip_list:
    address_type = check_ip_address_type(address)
    print(f"The IP address {address} is {address_type}")
