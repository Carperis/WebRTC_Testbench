import os
import sys
import json
import shutil
import re
import ipaddress


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

# e.g. stun.type.class == 0x10
stun_class = {
    0x00: "Request",
    0x01: "Indication",
    0x10: "Success Response",
    0x11: "Error Response"
}

# e.g. stun.type.method == 0x0001
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

# e.g. stun.att.type == 0x0020
stun_attribute = {
    0x0000: "Reserved [RFC8489]",
    0x0001: "MAPPED-ADDRESS [RFC8489]",
    0x0002: "Reserved [RFC8489]",
    0x0003: "Reserved [RFC5780][RFC Errata 4233]",
    0x0004: "Reserved [RFC8489]",
    0x0005: "Reserved [RFC8489]",
    0x0006: "USERNAME [RFC8489]",
    0x0007: "Reserved [RFC8489]",
    0x0008: "MESSAGE-INTEGRITY [RFC8489]",
    0x0009: "ERROR-CODE [RFC8489]",
    0x000A: "UNKNOWN-ATTRIBUTES [RFC8489]",
    0x000B: "Reserved [RFC8489]",
    0x000C: "CHANNEL-NUMBER [RFC8656]",
    0x000D: "LIFETIME [RFC8656]",
    # 0x000E-0x000F: "Reserved",
    0x0010: "Reserved [RFC8656]",
    0x0011: "Reserved",
    0x0012: "XOR-PEER-ADDRESS [RFC8656]",
    0x0013: "DATA [RFC8656]",
    0x0014: "REALM [RFC8489]",
    0x0015: "NONCE [RFC8489]",
    0x0016: "XOR-RELAYED-ADDRESS [RFC8656]",
    0x0017: "REQUESTED-ADDRESS-FAMILY [RFC8656]",
    0x0018: "EVEN-PORT [RFC8656]",
    0x0019: "REQUESTED-TRANSPORT [RFC8656]",
    0x001A: "DONT-FRAGMENT [RFC8656]",
    0x001B: "ACCESS-TOKEN [RFC7635]",
    0x001C: "MESSAGE-INTEGRITY-SHA256 [RFC8489]",
    0x001D: "PASSWORD-ALGORITHM [RFC8489]",
    0x001E: "USERHASH [RFC8489]",
    # 0x001F-0x001F: "Unassigned",
    0x0020: "XOR-MAPPED-ADDRESS [RFC8489]",
    0x0021: "Reserved [RFC8656]",
    0x0022: "RESERVATION-TOKEN [RFC8656]",
    0x0023: "Reserved",
    0x0024: "PRIORITY [RFC8445]",
    0x0025: "USE-CANDIDATE [RFC8445]",
    0x0026: "PADDING [RFC5780]",
    0x0027: "RESPONSE-PORT [RFC5780]",
    # 0x0028-0x0029: "Reserved",
    0x002A: "CONNECTION-ID [RFC6062]",
    # 0x002B-0x002F: "Unassigned",
    0x0030: "Reserved",
    # 0x0031-0x7FFF: "Unassigned",
    0x8000: "ADDITIONAL-ADDRESS-FAMILY [RFC8656]",
    0x8001: "ADDRESS-ERROR-CODE [RFC8656]",
    0x8002: "PASSWORD-ALGORITHMS [RFC8489]",
    0x8003: "ALTERNATE-DOMAIN [RFC8489]",
    0x8004: "ICMP [RFC8656]",
    # 0x8005-0x8021: "Unassigned",
    0x8022: "SOFTWARE [RFC8489]",
    0x8023: "ALTERNATE-SERVER [RFC8489]",
    0x8024: "Reserved",
    0x8025: "TRANSACTION_TRANSMIT_COUNTER [RFC7982]",
    0x8026: "Reserved",
    0x8027: "CACHE-TIMEOUT [RFC5780]",
    0x8028: "FINGERPRINT [RFC8489]",
    0x8029: "ICE-CONTROLLED [RFC8445]",
    0x802A: "ICE-CONTROLLING [RFC8445]",
    0x802B: "RESPONSE-ORIGIN [RFC5780]",
    0x802C: "OTHER-ADDRESS [RFC5780]",
    0x802D: "ECN-CHECK STUN [RFC6679]",
    0x802E: "THIRD-PARTY-AUTHORIZATION [RFC7635]",
    # 0x802F-0x802F: "Unassigned",
    0x8030: "MOBILITY-TICKET [RFC8016]",
    # 0x8031-0xBFFF: "Unassigned",
    0xC000: "CISCO-STUN-FLOWDATA [Dan_Wing]",
    0xC001: "ENF-FLOW-DESCRIPTION [Pål_Erik_Martinsen]",
    0xC002: "ENF-NETWORK-STATUS [Pål_Erik_Martinsen]",
    # 0xC003-0xC056: "Unassigned",
    0xC057: "GOOG-NETWORK-INFO [Jonas_Oreland]",
    0xC058: "GOOG-LAST-ICE-CHECK-RECEIVED [Jonas_Oreland]",
    0xC059: "GOOG-MISC-INFO [Jonas_Oreland]",
    0xC05A: "GOOG-OBSOLETE-1 [Jonas_Oreland]",
    0xC05B: "GOOG-CONNECTION-ID [Jonas_Oreland]",
    0xC05C: "GOOG-DELTA [Jonas_Oreland]",
    0xC05D: "GOOG-DELTA-ACK [Jonas_Oreland]",
    0xC05E: "GOOG-DELTA-SYNC-REQ [Jonas_Oreland]",
    # 0xC05F-0xC05F: "Unassigned",
    0xC060: "GOOG-MESSAGE-INTEGRITY-32 [Jonas_Oreland]",
    # 0xC061-0xFFFF: "Unassigned"
}
# convert packets in pcapng to json


def get_packet_json(file_name, out_name, d_filter):
    output_file = base_dir + divider + "outputs" + divider + out_name
    os.system(
        f"{tshark_dir} -r {file_name} -T json -Y \"{d_filter}\" --no-duplicate-keys > {output_file}")
    with open(output_file, 'r') as file:
        file_content = file.read()
        data = json.loads(file_content)
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
        stun_sections = pkt['_source']['layers']['stun']
        if (type(stun_sections) is not list):
            stun_sections = [stun_sections]
        else:
            print(f"Multiple stun sections! Packet number: {pkt['_source']['layers']['frame']['frame.number']}")
        for stun_section in stun_sections:
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

    # count number of packets in each category
    # total = 0
    # for key in result:
    #     print(key, len(result[key]))
    #     total += len(result[key])
    # print("Total:", total)

    return result


def get_ip_relations(ip_dict, pkts_classified, client_name):
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
            src_port = pkt['_source']['layers']['icmp']['udp']['udp.srcport']
            dst_port = pkt['_source']['layers']['icmp']['udp']['udp.dstport']
        elif (transport_layer == 'icmpv6'):
            src_port = pkt['_source']['layers']['icmpv6']['udp']['udp.srcport']
            dst_port = pkt['_source']['layers']['icmpv6']['udp']['udp.dstport']
        else:
            raise Exception("Unknown transport layer")

        ip_pairs = [[src_ip, src_port], [dst_ip, dst_port]]
        return ip_pairs

    def add_to_ip_dict(ip_dict, ip_port):
        ip = ip_port[0]
        port = ip_port[1]
        if (ip not in ip_dict):
            ip_dict[ip] = {
                "ports": [],
                "map": [],
                "relay": [],
                "mapped": [],
                "relayed": [],
                "ip_type": "",
                "Client_name": "",
                "Client_flag": False,
                "NAT_flag": False,
                "Server_flag": False,
            }
        if (port not in ip_dict[ip]["ports"]):
            ip_dict[ip]["ports"].append(port)

        type = check_ip_address_type(ip)
        if (type == "Private"):
            ip_dict[ip]["ip_type"] = "Private"
            ip_dict[ip]["Client_flag"] = True
        elif (type == "Public"):
            ip_dict[ip]["ip_type"] = "Public"
        else:
            ip_dict[ip]["ip_type"] = "Invalid IP address"

    def get_attributes(pkt):
        attr = pkt['_source']['layers']['stun']['stun.attributes']
        if (type(attr["stun.attribute"]) == list):
            attr_list = [int(code, 16) for code in attr["stun.attribute"]]
            detail_list = attr["stun.attribute_tree"]
        else:
            attr_list = [int(attr["stun.attribute"], 16)]
            detail_list = [attr["stun.attribute_tree"]]
        return attr_list, detail_list

    def check_ip_address_type(ip_address):
        try:
            ip = ipaddress.ip_address(ip_address)
            if ip.is_private:
                return "Private"
            else:
                return "Public"
        except ValueError:
            return "Invalid IP address"

    def check_xor_mapped_address(ip_dict, dst, src, attr_list, detail_list):
        if (0x0020 in attr_list):  # XOR-MAPPED-ADDRESS
            i = attr_list.index(0x0020)
            detail = detail_list[i]
            try:
                ip = detail["stun.att.ipv4"]
            except:
                ip = detail["stun.att.ipv6"]
            port = detail["stun.att.port"]
            mapped = [ip, port]
            map_dict = {"from": dst, "to": mapped}
            mapped_dict = {"from": dst, "to": mapped, "by": src}
            add_to_ip_dict(ip_dict, mapped)
            if (mapped_dict not in ip_dict[dst[0]]["mapped"]):
                ip_dict[dst[0]]["mapped"].append(mapped_dict)
            if (map_dict not in ip_dict[src[0]]["map"]):
                ip_dict[src[0]]["map"].append(map_dict)

            if (ip_dict[ip]["Server_flag"] == False):
                ip_dict[ip]["NAT_flag"] = True
                if (ip == dst[0] and ip_dict[src[0]]["ip_type"] == "Public"):
                    ip_dict[dst[0]]["Client_flag"] = True
            return True
        else:
            return False

    def check_mapped_address(ip_dict, dst, src, attr_list, detail_list):
        if (0x0001 in attr_list):  # MAPPED-ADDRESS
            i = attr_list.index(0x0020)
            detail = detail_list[i]
            try:
                ip = detail["stun.att.ipv4"]
            except:
                ip = detail["stun.att.ipv6"]
            port = detail["stun.att.port"]
            mapped = [ip, port]
            map_dict = {"from": dst, "to": mapped}
            mapped_dict = {"from": dst, "to": mapped, "by": src}
            add_to_ip_dict(ip_dict, mapped)
            if (mapped_dict not in ip_dict[dst[0]]["mapped"]):
                ip_dict[dst[0]]["mapped"].append(mapped_dict)
            if (map_dict not in ip_dict[src[0]]["map"]):
                ip_dict[src[0]]["map"].append(map_dict)

            if (ip_dict[ip]["Server_flag"] == False):
                ip_dict[ip]["NAT_flag"] = True
                if (ip == dst[0]):
                    ip_dict[dst[0]]["Client_flag"] = True
            return True
        else:
            return False

    def check_xor_relayed_address(ip_dict, src, dst, attr_list, detail_list):
        if (0x0016 in attr_list):  # XOR-RELAYED-ADDRESS
            i = attr_list.index(0x0016)
            detail = detail_list[i]
            try:
                ip = detail["stun.att.ipv4"]
            except:
                ip = detail["stun.att.ipv6"]
            port = detail["stun.att.port"]
            relayed = [ip, port]
            relay_dict = {"from": dst, "to": relayed}
            relayed_dict = {"from": dst, "to": relayed, "by": src}
            add_to_ip_dict(ip_dict, relayed)
            if (relayed_dict not in ip_dict[dst[0]]["relayed"]):
                ip_dict[dst[0]]["relayed"].append(relayed_dict)
            if (relay_dict not in ip_dict[src[0]]["relay"]):
                ip_dict[src[0]]["relay"].append(relay_dict)

            ip_dict[src[0]]["Server_flag"] = True
            ip_dict[src[0]]["NAT_flag"] = False
            ip_dict[src[0]]["Client_flag"] = False
            return True
        else:
            return False

    # ip_dict = {}
    allocate_pkts = pkts_classified['Allocate']
    binding_pkts = pkts_classified['Binding']

    for pkt in allocate_pkts:
        src, dst = get_src_and_dst(pkt)
        add_to_ip_dict(ip_dict, src)
        add_to_ip_dict(ip_dict, dst)
        if ("stun.attributes" in pkt['_source']['layers']['stun']):
            attr_list, detail_list = get_attributes(pkt)
            check_xor_mapped_address(ip_dict, dst, src, attr_list, detail_list)
            check_xor_relayed_address(
                ip_dict, src, dst, attr_list, detail_list)

    for pkt in binding_pkts:
        src, dst = get_src_and_dst(pkt)
        add_to_ip_dict(ip_dict, src)
        add_to_ip_dict(ip_dict, dst)
        if ("stun.attributes" in pkt['_source']['layers']['stun']):
            attr_list, detail_list = get_attributes(pkt)
            check_xor_mapped_address(ip_dict, dst, src, attr_list, detail_list)
            check_mapped_address(ip_dict, dst, src, attr_list, detail_list)

    for pkt in binding_pkts:
        pkt_class = pkt['_source']['layers']['stun']['stun.type_tree']['stun.type.class']
        src, dst = get_src_and_dst(pkt)
        if (int(pkt_class, 16) == 0x00 and ip_dict[src[0]]["Client_flag"] == True and ip_dict[dst[0]]["Server_flag"] == True):
            ip_dict[src[0]]["Client_name"] = client_name

    return ip_dict


def get_ip_filter(ip_dict, client_name):
    import ip_filter

    def no_client_ip(ip_dict, client_name):
        new_ip_list = []
        for ip in ip_dict:
            if (ip_dict[ip]["Client_name"] != client_name):
                new_ip_list.append(ip)
        return new_ip_list

    ip_list = list(ip_dict.keys())
    # print(ip_list)
    new_ip_list = no_client_ip(ip_dict, client_name)
    print(f'\n{new_ip_list}\n')
    filter_code = ip_filter.generate_display_filter(new_ip_list)
    print(f'\n{filter_code}\n')
    return filter_code


def count_transaction(transaction_dict, pkts_json):
    for pkt in pkts_json:
        pass


if __name__ == "__main__":
    path = base_dir + divider + "inputs" + divider
    caller_file = path + 'packets_caller.pcapng'
    receiver_file = path + 'packets_receiver.pcapng'
    stun_filter = 'stun'
    client_names = ["caller", "receiver"]
    ip_dict = {}
    transaction_dict = {}

    name = caller_file.split(divider)[-1].split('.')[0] + '.json'
    caller_json = get_packet_json(caller_file, name, stun_filter)
    caller_classified = classify_packets(caller_json)
    ip_dict = get_ip_relations(ip_dict, caller_classified, client_names[0])
    caller_ip_filter_code = get_ip_filter(ip_dict, client_names[0])
    name = caller_file.split(divider)[-1].split('.')[0] + '_all.json'
    caller_all_json = get_packet_json(caller_file, name, caller_ip_filter_code)

    name = receiver_file.split(divider)[-1].split('.')[0] + '.json'
    receiver_json = get_packet_json(receiver_file, name, stun_filter)
    receiver_classified = classify_packets(receiver_json)
    ip_dict = get_ip_relations(ip_dict, receiver_classified, client_names[1])
    receiver_ip_filter_code = get_ip_filter(ip_dict, client_names[1])
    name = receiver_file.split(divider)[-1].split('.')[0] + '_all.json'
    receiver_all_json = get_packet_json(receiver_file, name, receiver_ip_filter_code)

    all_json = caller_all_json.extend(receiver_all_json)

    print(len(caller_json), len(receiver_json))
