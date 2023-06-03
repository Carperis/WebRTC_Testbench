

import pyshark

# Path to the Wireshark capture file
capture_file = 'C:\\Users\\Sam\\Desktop\\WebRTC_Testbench\\analyser\inputs\\Wireshark Host.pcapng'
ip_dict = {'157.240.245.58:56442': {'type': 'relay', 'location': 'caller'}, '157.240.245.58:57182': {'type': 'relay', 'location': 'caller'}, '10.239.233.249:62232': {'type': 'host', 'location': 'caller'}, '10.239.233.249:52105': {'type': 'host', 'location': 'caller'}, '128.197.29.249:36960': {'type':
                                                                                                                                                                                                                                                                                                      'srflx', 'location': 'caller'}, '128.197.29.249:28071': {'type': 'srflx', 'location': 'caller'}, '157.240.245.58:56180': {'type': 'relay', 'location': 'caller'}, '10.239.233.249:9': {'type': 'host', 'location': 'caller'}, '157.240.245.58:53978': {'type': 'relay', 'location': 'caller'}, '157.240.245.58:52465': {'type': 'relay', 'location': 'caller'}, '157.240.245.58:55860': {'type': 'relay', 'location': 'caller'}, '128.197.29.249:50060': {'type': 'srflx', 'location': 'caller'}, '128.197.29.249:38743': {'type': 'srflx', 'location': 'caller'}, '128.197.29.225:28023': {'type': 'srflx', 'location': 'receiver'}, '10.239.25.33:55902': {'type': 'host', 'location': 'receiver'}, '128.197.29.225:15914': {'type': 'srflx', 'location': 'receiver'}, '157.240.245.58:56078': {'type': 'relay', 'location': 'receiver'}, '157.240.245.58:58341': {'type': 'relay', 'location': 'receiver'}, '128.197.29.249:25754': {'type': 'prflx', 'location': 'caller'}, '157.240.245.58:53239': {'type': 'relay', 'location': 'receiver'}, '10.239.25.33:9': {'type': 'host', 'location': 'receiver'}, '128.197.29.225:36307': {'type': 'prflx', 'location': 'receiver'}, '128.197.29.225:46635': {'type': 'prflx', 'location': 'receiver'}}
tshark_dir = "D:\\Wireshark\\tshark.exe"

# Open the capture file
capture = pyshark.FileCapture(capture_file, tshark_path=tshark_dir)

# Iterate over each packet in the capture
for packet in capture:
    # Check if the packet has an IP layer
    if 'IP' in packet:
        # Access IP layer attributes
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst

        # Perform analysis or print packet details
        print(f"Source IP: {src_ip}")
        print(f"Destination IP: {dst_ip}")
        print("")
    else:
        print("Packet does not have an IP layer")

# Close the capture file
capture.close()