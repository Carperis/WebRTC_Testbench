import os
import wireshark_extract
divider = "\\"
base_dir = os.path.dirname(os.path.abspath(
    __file__))  # get the current directory
path = base_dir + divider + "inputs" + divider
file_name = path + 'packets_caller.pcapng'

network_ip = "1558d67c-3835-4a88-b706-2775ff195495.local"
d_filter1 = "ip.src_host == \"" + network_ip + "\""
d_filter2 = "ip.dst_host == \"" + network_ip + "\""
d_filter = d_filter1 + " or " + d_filter2


out_name = 'test.json'
# -N: turn on name resolution
# d: enable resolution from captured DNS packets (Resolve Physical Addresses)
# n: enable network address resolution (Resolve Network Addresses)
# see: https://manpages.ubuntu.com/manpages/xenial/en/man1/tshark.1.html
add_arg = "-Nnd -e ip.src -e ip.src_host -e ip.dst -e ip.dst_host"
delete = True
wireshark_extract.get_packet_json(
    file_name, out_name, d_filter, add_arg, delete)
