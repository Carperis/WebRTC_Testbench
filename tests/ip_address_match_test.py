import re

# def find_ipv4_addresses(text):
#     ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
#     ipv4_addresses = re.findall(ipv4_pattern, text)
#     return ipv4_addresses

# def find_ipv6_addresses(text):
#     ipv6_pattern = r'\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b|\b(?:[0-9A-Fa-f]{1,4}:){0,6}(?:(?:[0-9A-Fa-f]{1,4}:){1,6})?:[0-9A-Fa-f]{1,4}\b'
#     ipv6_addresses = re.findall(ipv6_pattern, text)
#     return ipv6_addresses

def find_ipv4_addr_port(text):
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b\s*(\d+)\b'
    ipv4_addresses = re.search(ipv4_pattern, text)
    return ipv4_addresses.group(0).replace(" ", ":")

def find_ipv6_addr_port(text):
    ipv6_pattern = r'\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b|\b(?:[0-9A-Fa-f]{1,4}:){0,6}(?:(?:[0-9A-Fa-f]{1,4}:){1,6})?:[0-9A-Fa-f]{1,4}\b\s*(\d+)\b'
    ipv6_addresses = re.search(ipv6_pattern, text)
    return ipv6_addresses.group(0).replace(" ", ":")

# Example usage
# input_text = "This is an example text with IPv4 address 192.168.0.1 and IPv6 address 2001:0db8:85a3:0000:0000:8a2e:0370:7334"
input_text = "sdpMid: 0, sdpMLineIndex: 0, candidate: candidate:875917003 1 udp 2122000639 2601:19b:80:c980:fd90:d9f3:437e:ed71 53124 typ host generation 0 ufrag i/MM network-id 6 network-cost 10"
# input_text = "sdpMid: 1, sdpMLineIndex: 1, candidate: candidate:1646281953 1 udp 2122066175 2601:19b:80:c980::bf7b 53129 typ host generation 0 ufrag i/MM network-id 5 network-cost 10"
# ipv4_addresses_found = find_ipv4_addresses(input_text)
# ipv6_addresses_found = find_ipv6_addresses(input_text)
ipv4_addresses_found = find_ipv4_addr_port(input_text)
ipv6_addresses_found = find_ipv6_addr_port(input_text)

print("IPv4 addresses found:", ipv4_addresses_found)
print("IPv6 addresses found:", ipv6_addresses_found)
