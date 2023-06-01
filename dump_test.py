import re

def extract_statistics(dump_content):
    # Extract statistics section
    statistics_section = re.search(r'Statistics(.*?)(?=Peer Connections|$)', dump_content, re.DOTALL)
    if statistics_section:
        statistics_data = statistics_section.group(1)
        # Extract desired statistics data from the section
        # Modify the regular expressions according to the specific data you want to extract
        rtt = re.search(r'Round Trip Time \(ms\):\s+(\d+)', statistics_data)
        packet_loss = re.search(r'Packet Loss Ratio:\s+(\d+)', statistics_data)
        bitrate = re.search(r'Bitrate \(bps\):\s+(\d+)', statistics_data)

        if rtt:
            print('Round Trip Time:', rtt.group(1))
        if packet_loss:
            print('Packet Loss Ratio:', packet_loss.group(1))
        if bitrate:
            print('Bitrate:', bitrate.group(1))

def extract_peer_connections(dump_content):
    # Extract peer connections section
    peer_connections_section = re.search(r'Peer Connections(.*?)(?=Media Streams|$)', dump_content, re.DOTALL)
    if peer_connections_section:
        peer_connections_data = peer_connections_section.group(1)
        # Extract desired peer connections data from the section
        # Modify the regular expressions according to the specific data you want to extract
        local_candidates = re.findall(r'Local Candidate: (.*?),', peer_connections_data)
        remote_candidates = re.findall(r'Remote Candidate: (.*?),', peer_connections_data)
        transport_protocol = re.search(r'Transport Protocol: (.*?)\n', peer_connections_data)

        print('Local Candidates:', local_candidates)
        print('Remote Candidates:', remote_candidates)
        if transport_protocol:
            print('Transport Protocol:', transport_protocol.group(1))

# Read the WebRTC Internals dump file
with open('webrtc_dump.txt', 'r') as file:
    dump_content = file.read()

# Extract desired information from the dump file
extract_statistics(dump_content)
extract_peer_connections(dump_content)
