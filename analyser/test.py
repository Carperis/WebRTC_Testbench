import os
import sys
import json
import shutil


def identify_os():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'Mac OS'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    else:
        return 'Unknown'


base_dir = os.path.dirname(os.path.abspath(
    __file__))  # get the current directory

if (identify_os() == 'Windows'):
    divider = "\\"
elif (identify_os() == 'Mac OS'):
    divider = "/"

with open('tshark_location.txt', 'r') as file:
    tshark_dir = file.read().strip()


stun_method = {
    0x000: "Reserved [RFC8489]",
    0x001: "Binding [RFC8489]",
    0x002: "Reserved [RFC8489]",
    0x003: "Allocate [RFC8656]",
    0x004: "Refresh [RFC8656]",
    # 0x005: "Unassigned",
    0x006: "Send [RFC8656]",
    0x007: "Data [RFC8656]",
    0x008: "CreatePermission [RFC8656]",
    0x009: "ChannelBind [RFC8656]",
    0x00A: "Connect [RFC6062]",
    0x00B: "ConnectionBind [RFC6062]",
    0x00C: "ConnectionAttempt [RFC6062]",
    # 0x00D-0x07F: "Unassigned",
    0x080: "GOOG-PING [Jonas_Oreland]",
    # 0x081-0x0FF: "Unassigned",
    # 0x100-0xFFF: "Reserved [RFC7983]"
}


# convert packets in pcapng to json
def get_packet_json(file_name, d_filter):
    name = file_name.split(divider)[-1].split('.')[0] + '.json'
    output_file = base_dir + divider + "outputs" + divider + name
    os.system(
        f"{tshark_dir} -r {file_name} -T json -Y {d_filter} > {output_file}")
    with open(output_file, 'r') as file:
        data = json.load(file)
    # shutil.rmtree(output_file, ignore_errors=True)
    # print(data)
    return data


def classify_packets(pkts_json):
    result = {}
    method_codes = list(stun_method.keys())
    for key in method_codes:
        result[stun_method[key].split(" ")[0]] = []

    result["ChannelMessage"] = []
    result["Unknown"] = []

    for pkt in pkts_json:
        stun_section = pkt['_source']['layers']['stun']
        if ('stun.type_tree' in stun_section):
            code = int(stun_section['stun.type_tree']['stun.type.method'], 16)
            if (code in method_codes):
                result[stun_method[code].split(" ")[0]].append(pkt)
            else:
                result["Unknown"].append(pkt)
        elif ('stun.channel' in stun_section):
            code = int(stun_section['stun.channel'], 16)
            result["ChannelMessage"].append(pkt)
        else:
            raise Exception("Unknown packet type")

    # # count number of packets in each category
    # total = 0
    # for key in result:
    #     print(key, len(result[key]))
    #     total += len(result[key])
    # print("Total:", total)

    return result

def get_ip_relations(pkts_classified):
    def get_src_and_dst(pkt):
        ip_layer = list(pkt['_source']['layers'].keys())[2]
        transport_layer = list(pkt['_source']['layers'].keys())[3]
        
        if (ip_layer == 'ip'):
            src_ip = pkt['_source']['layers']['ip']['ip.src']
            dst_ip = pkt['_source']['layers']['ip']['ip.dst']
        elif (ip_layer == 'ipv6'):
            src_ip = pkt['_source']['layers']['ipv6']['ipv6.src']
            dst_ip = pkt['_source']['layers']['ipv6']['ipv6.dst']
        else:
            raise Exception("Unknown IP layer")
        
        if (transport_layer == 'udp'):
            src_port = pkt['_source']['layers']['udp']['udp.srcport']
            dst_port = pkt['_source']['layers']['udp']['udp.dstport']
        elif (transport_layer == 'tcp'):
            src_port = pkt['_source']['layers']['tcp']['tcp.srcport']
            dst_port = pkt['_source']['layers']['tcp']['tcp.dstport']
        elif (transport_layer == 'icmp'):
            src_port = pkt['_source']['layers']['icmp']['udp_srcport']
            dst_port = pkt['_source']['layers']['icmp']['udp_dstport']
        elif (transport_layer == 'icmpv6'):
            src_port = pkt['_source']['layers']['icmpv6']['udp_srcport']
            dst_port = pkt['_source']['layers']['icmpv6']['udp_dstport']
        else:
            raise Exception("Unknown transport layer")

        ip_list = [[src_ip, src_port], [dst_ip, dst_port]]
        return ip_list
    
    ip_dict = {}
    # binding_pkts = pkts_classified['Binding']
    allocate_pkts = pkts_classified['Allocate']
    for pkt in allocate_pkts:
        ip_list = get_src_and_dst(pkt)
        
        attr = pkt['_source']['layers']['stun']['stun.attributes']
        print(attr)
        
        
        

path = base_dir + divider + "inputs" + divider
caller_file = path + 'packets_caller.pcapng'
receiver_file = path + 'packets_receiver.pcapng'
stun_filter = 'stun'
# stun_filter = 'stun.type.method == 0x0001'

caller_json = get_packet_json(caller_file, stun_filter)
receiver_json = get_packet_json(receiver_file, stun_filter)

caller_classified = classify_packets(caller_json)
receiver_classified = classify_packets(receiver_json)

get_ip_relations(caller_classified)

print(len(caller_json), len(receiver_json))
