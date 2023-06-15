import pyshark
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import ipaddress

# tshark -r test2.pcapng -T json -Y frame.number==38880

def get_packet_json():
    os.system("tshark -r test2.pcapng -T json -Y frame.number==38880 > test.json")

def extract_stun_packets(pcapng_file, tshark_dir):
    # cap = pyshark.FileCapture(pcapng_file, tshark_path=tshark_dir, display_filter='stun')
    # cap_sum = pyshark.FileCapture(pcapng_file, tshark_path=tshark_dir, only_summaries=True, display_filter='stun',)
    cap = pyshark.FileCapture(pcapng_file, tshark_path=tshark_dir, display_filter='stun')
    
    # These 3 lines are to fix pyshark internal bug of missing first packet
    first_stun_num = int(cap[0].number) - 1 
    d_filter = f'stun || frame.number == {str(first_stun_num)}'
    print(d_filter)
    
    cap_sum = pyshark.FileCapture(pcapng_file, tshark_path=tshark_dir, only_summaries=True, display_filter=d_filter,)
    
    return cap, cap_sum


def get_response_dict(cap):
    # Create a dictionary to store packet response relationships
    response_dict = {}

    for packet in cap:
        print(packet)
        packet_number = int(packet.number)
        try:
            response_to = int(packet.stun.response_to)
        except:
            continue

        # If the packet has a response_to value, update the dictionary
        if (response_to > 0):
            response_dict[packet_number] = response_to

    # Print the packet response relationships
    for packet_number, response_to in response_dict.items():
        print("Packet {} responds to packet {}".format(
            packet_number, response_to))

    return response_dict


def get_packets_dict(cap, cap_sum, identifier):
    def get_stun_type(msg_code):
        part1_dict = {
            "00": "Request",
            "01": "Indication",
            "10": "Success Response",
            "11": "Error Response"
        }
        part2_dict = {
            "0": "Unknown0",
            "1": "Binding",
            "2": "Unknown2",
            "3": "Allocate",
            "4": "Refresh",
            "5": "Unknown5",
            "6": "Send",
            "7": "Data",
            "8": "CreatePermission",
            "9": "Channel-Bind",
            "a": "Unknowna",
            "b": "Unknownb",
            "c": "Unknownc",
            "d": "Unknownd",
            "e": "Unknowne",
            "f": "Unknownf"
        }
        hex_code = msg_code.split("x")[1].lower()
        part1 = hex_code[1:3]
        part2 = hex_code[3:4]
        text = part2_dict[part2] + " " + part1_dict[part1]
        return text

    def unpack_time(time_all):
        time_parts = time_all.split(" ")
        date = time_parts[0] + " " + time_parts[2] + time_parts[3]
        time = time_parts[4]
        try:
            zone = time_parts[5] + " " + time_parts[6] + " " + time_parts[7]
        except:
            zone = ""
        # print(time_parts)
        return [date, time, zone]

    packets_dict = {}
    
    c1 = 0
    for packet in cap:
        c1 += 1
        
    c2 = 0
    for packet in cap_sum:
        c2 += 1
        
    print(c1, c2)

    i = 0
    while(True):
        packet = cap[i]
        pkt_sum = cap_sum[i]
        print(packet.number, pkt_sum.no)
        # print(packet)
        sec = float(packet.frame_info.time_epoch)

        packets_dict[sec] = {}
        packets_dict[sec]["client"] = identifier

        #get packet number
        packet_number = int(packet.number) 
        packets_dict[sec]["packet_number"] = packet_number

        #get time
        time_all = packet.frame_info.time 
        [date, time, zone] = unpack_time(time_all)
        packets_dict[sec]["time"] = {}
        packets_dict[sec]["time"]["date"] = date
        packets_dict[sec]["time"]["time"] = time
        packets_dict[sec]["time"]["zone"] = zone
        packets_dict[sec]["time"]["sec"] = sec

        #get ip addresses
        if (hasattr(packet, "ip")):
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
        elif (hasattr(packet, "ipv6")):
            src_ip = packet.ipv6.src
            dst_ip = packet.ipv6.dst
        
        # get ports
        if (hasattr(packet, "udp")):
            src_port = packet.udp.srcport
            dst_port = packet.udp.dstport
            packets_dict[sec]["protocol"] = "UDP"
        elif (hasattr(packet, "tcp")):
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
            packets_dict[sec]["protocol"] = "TCP"
        elif (hasattr(packet, "icmp")):
            src_port = packet.icmp.udp_srcport
            dst_port = packet.icmp.udp_dstport
            packets_dict[sec]["protocol"] = "ICMP"
        elif (hasattr(packet, "icmpv6")):
            src_port = packet.icmpv6.udp_srcport
            dst_port = packet.icmpv6.udp_dstport
            packets_dict[sec]["protocol"] = "ICMPv6"
        else:
            raise Exception("No port found")
        
        packets_dict[sec]["src_ip"] = src_ip
        packets_dict[sec]["src_port"] = src_port
        packets_dict[sec]["dst_ip"] = dst_ip
        packets_dict[sec]["dst_port"] = dst_port
        
        #get message type
        if (hasattr(packet.stun, "type")):
            msg_code = packet.stun.type
            msg_type = get_stun_type(msg_code)
        elif (hasattr(packet.stun, "channel")):
            msg_code = packet.stun.channel
            msg_type = "ChannelData TURN Message"
        else:
            raise Exception("No message type found")
        packets_dict[sec]["msg_code"] = msg_code
        packets_dict[sec]["msg_type"] = msg_type
        
        
        # get "response_to" or "response_in" packet numbers
        if (hasattr(packet.stun, "response_to")):
            response_to = int(packet.stun.response_to)
        else:
            response_to = ""
        if (hasattr(packet.stun, "response_in")):
            response_in = int(packet.stun.response_in)
        else:
            response_in = ""
        packets_dict[sec]["response_to"] = response_to
        packets_dict[sec]["response_in"] = response_in
        
        if (hasattr(packet.stun, "attributes")):
            attr = pkt_sum.info.split(msg_type)[1].strip()
        else:
            attr = ""
        packets_dict[sec]["attributes"] = attr
            
        # try:
        #     if (packet.stun.att_type == "0x0020"): # XOR-MAPPED-ADDRESS
        #         print(packet)
        # except:
        #     xor_mapped_address = ""
        # try:
        #     if (packet.stun.att_type == "0x0016"): # XOR-RELAYED-ADDRESS
        
        try:
            packet_next = cap[i+1]
            pkt_sum_next = cap_sum[i+1]
            i = i + 1
        except:
            break
        

    return packets_dict


def mix_packets_dict(packets_dict1, packets_dict2):
    all_packets_dict = {}
    keys1 = list(packets_dict1.keys())
    keys2 = list(packets_dict2.keys())
    index1 = 0
    index2 = 0
    limit1 = False
    limit2 = False
    while (index1 < len(keys1) or index2 < len(keys2)):
        if (index1 == len(keys1)):
            limit1 = True
        else:
            key1 = keys1[index1]
        if (index2 == len(keys2)):
            limit2 = True
        else:
            key2 = keys2[index2]
        if (key1 < key2):
            if (limit1):
                all_packets_dict[key2] = packets_dict2[key2]
                index2 += 1
                continue
            all_packets_dict[key1] = packets_dict1[key1]
            index1 += 1
        else:
            if (limit2):
                all_packets_dict[key1] = packets_dict1[key1]
                index1 += 1
                continue
            all_packets_dict[key2] = packets_dict2[key2]
            index2 += 1

    return all_packets_dict


def get_ip_dict(packets_dict):
    def check_ip_address_type(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)
            if ip.is_private:
                return "Private"
            else:
                return "Public"
        except ValueError:
            return "Invalid IP address"

    ip_dict = {}  # count the occurrence for each ip

    for num in packets_dict.keys():
        src_ip = packets_dict[num]["src_ip"]
        src_port = packets_dict[num]["src_port"]
        dst_ip = packets_dict[num]["dst_ip"]
        dst_port = packets_dict[num]["dst_port"]
        identifier = packets_dict[num]["identifier"]

        ips = [src_ip + "_" + str(src_port), dst_ip + "_" + str(dst_port)]
        for ip in ips:
            addr = ip.split("_")[0]
            port = ip.split("_")[1]
            if addr not in ip_dict:
                ip_dict[addr] = {}
                type = check_ip_address_type(addr)
                ip_dict[addr]["type"] = type
                if (type == "Private"):
                    ip_dict[addr]["identifier"] = identifier
                ip_dict[addr][port] = 0
            elif port not in ip_dict[addr]:
                ip_dict[addr][port] = 0
            ip_dict[addr][port] += 1

    return ip_dict


def visualize(all_packets_dict, all_ip_dict):
    def rearrange_nodes(addresses):
        print(addresses)
        indexes = input(f"arrange 1~5 for {addresses}: \n")
        indexes = [(int(char) - 1) for char in indexes]
        nodes = [""] * 5
        for i in range(len(indexes)):
            index = indexes[i]
            if (nodes[index] == ""):
                nodes[index] = addresses[i]
            else:
                nodes[index] = nodes[index] + "/" + addresses[i]
        print(nodes)
        return nodes

    fig, ax = plt.subplots()
    addresses = list(all_ip_dict.keys())
    nodes = rearrange_nodes(addresses)

    xindex = {}
    for i in range(len(nodes)):
        addrs = nodes[i].split("/")
        for addr in addrs:
            xindex[addr.strip()] = i

    times = len(all_packets_dict.keys())

    # Set up x-axis for nodes
    ax.xaxis.tick_top()
    ax.xaxis.set_ticks_position('none')
    ax.set_xticks(np.arange(0, len(nodes), 1))
    ax.set_xticklabels(nodes)

    # Set up y-axis for time
    ax.yaxis.set_ticks_position('none')
    ax.set_yticks(np.arange(0, times, 1))
    ax.invert_yaxis()

    # Plot vertical time lines
    for node in range(len(nodes)):
        ax.axvline(node, color='gray', linestyle='--')

    time_labels = []

    for i in range(len(all_packets_dict)):
        key = list(all_packets_dict.keys())[i]
        arrow = all_packets_dict[key]
        source = xindex[arrow['src_ip']]
        target = xindex[arrow['dst_ip']]
        time = i
        time_labels.append(arrow["time"]["time"])
        description = arrow['identifier'] + \
            str(arrow['packet_number']) + ": " + arrow['msg_type']

        start_x = source
        start_y = time
        end_x = target
        end_y = time

        dx = end_x - start_x
        dy = end_y - start_y

        if (dx < 0):
            dx += 0.05
            text_pos = target + 0.1
        else:
            dx -= 0.05
            text_pos = source + 0.1
        ax.arrow(start_x, start_y, dx, dy, head_width=0.2,
                 head_length=0.05, fc='black', ec='black')
        ax.text(text_pos, time - 0.1, description)

    ax.set_yticklabels(time_labels)
    plt.ylabel('Time')
    plt.title('Time Sequence Diagram')
    plt.show()


def identify_os():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'Mac OS'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    else:
        return 'Unknown'


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(
        __file__))  # get the current directory

    if (identify_os() == 'Windows'):
        divider = "\\"
    elif (identify_os() == 'Mac OS'):
        divider = "/"

    with open('tshark_location.txt', 'r') as file:
        tshark_dir = file.read().strip()

    # Provide the path to your pcapng file
    caller_file = 'packets_caller.pcapng'
    receiver_file = 'packets_receiver.pcapng'
    path = base_dir + divider + "inputs" + divider

    caller_cap, caller_sum = extract_stun_packets(path + caller_file, tshark_dir)
    receiver_cap, receiver_sum = extract_stun_packets(path + receiver_file, tshark_dir)

    caller_packets_dict = get_packets_dict(caller_cap, caller_sum, "caller")
    receiver_packets_dict = get_packets_dict(receiver_cap, receiver_sum, "receiver")
    all_packets_dict = mix_packets_dict(
        caller_packets_dict, receiver_packets_dict)
    all_ip_dict = get_ip_dict(all_packets_dict)
    # caller_ip_dict = get_ip_dict(caller_packets_dict)
    # receiver_ip_dict = get_ip_dict(receiver_packets_dict)
    # visualize(all_packets_dict, all_ip_dict)

    print("")
    print(list(all_ip_dict.keys()))
    print("")
