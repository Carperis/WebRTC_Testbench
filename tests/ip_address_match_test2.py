import re
text = "2601:19b:80:c980:92e0:23f2:875e:64d 53122 10.0.0.192 53123"
def find_ipv4(text):
    ipv4_pattern = r'\b((?:\d{1,3}\.){3}\d{1,3})\b'
    ipv4_addresses = re.findall(ipv4_pattern, text)
    if (len(ipv4_addresses) != 0):
        addr = ipv4_addresses[0]
        pattern = addr + r' (\d+)\b'
        port = re.findall(pattern, text)
        result = [addr, port[0]]
    else:
        result = []  
    return result


def find_ipv6(text):
    ipv6_pattern = r'\b(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}\b|\b(?:[0-9A-Fa-f]{1,4}:){0,6}(?:(?:[0-9A-Fa-f]{1,4}:){1,6})?:[0-9A-Fa-f]{1,4}\b'
    ipv6_addresses = re.findall(ipv6_pattern, text)
    if (len(ipv6_addresses) != 0):
        addr = ipv6_addresses[0]
        pattern = addr + r' (\d+)\b'
        port = re.findall(pattern, text)
        result = [addr, port[0]]
    else:
        result = []
    return result

print(find_ipv4(text))
print(find_ipv6(text))