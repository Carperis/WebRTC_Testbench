import netifaces

def get_ipv4_addresses():
    ipv4_addresses = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        try:
            addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
            ipv4_addresses.extend(address['addr'] for address in addresses)
        except KeyError:
            pass
    return ipv4_addresses

def get_ipv6_addresses():
    ipv6_addresses = []
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        try:
            addresses = netifaces.ifaddresses(interface)[netifaces.AF_INET6]
            ipv6_addresses.extend(address['addr'] for address in addresses)
        except KeyError:
            pass
    return ipv6_addresses

ipv4_addresses = get_ipv4_addresses()
ipv6_addresses = get_ipv6_addresses()

print("IPv4 addresses:", ipv4_addresses)
print("IPv6 addresses:", ipv6_addresses)
