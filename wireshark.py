import pyshark


def analyze_turn_packets(pcap_file, tshark_dir):
    capture = pyshark.FileCapture(pcap_file, tshark_path=tshark_dir)

    # Filter packets to include only TURN protocol packets
    capture.apply_on_packets(
        lambda pkt: pkt.transport_layer == 'UDP' and 'TURN' in pkt.layers)

    # Analyze each packet
    for packet in capture:
        # Extract relevant information from the TURN packet
        timestamp = packet.sniff_time
        source_ip = packet.ip.src
        destination_ip = packet.ip.dst
        turn_type = packet.turn.type
        turn_method = packet.turn.method

        # Print or process the extracted information as per your requirement
        print(f'Timestamp: {timestamp}')
        print(f'Source IP: {source_ip}')
        print(f'Destination IP: {destination_ip}')
        print(f'TURN Type: {turn_type}')
        print(f'TURN Method: {turn_method}')
        print('---')

    capture.close()


with open('tshark_path.txt', 'r') as file:
    tshark_dir = file.read()

# Provide the path to your pcapng file
pcap_file_path = 'packets_caller.pcapng'

analyze_turn_packets(pcap_file_path, tshark_dir)
