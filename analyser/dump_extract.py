import json
import os
import sys
import re

base_dir = os.path.dirname(os.path.abspath(
    __file__))  # get the current directory


def unpack_dump(file_name):

    # Read the text file
    with open(file_name, 'r', encoding='utf-8') as file:
        file_data = file.read()

    # Convert the text to JSON
    json_data = json.loads(file_data)

    PC_data = json_data["PeerConnections"]
    PC_keys = PC_data.keys()
    focus_key = list(PC_keys)[0]
    data_length = len(PC_data[focus_key]["stats"])
    for key in PC_keys:
        if (len(PC_data[key]["stats"]) > data_length):
            focus_key = key
            data_length = len(PC_data[key]["stats"])
    json_data = PC_data[focus_key]
    return json_data


def extract_candidateID(json_data):
    stats = json_data["stats"]
    candidateID_dict = {}

    # Extract keys containing "-ip"
    keys_with_ip = [key for key in stats.keys() if "-ip" in key]

    for key in keys_with_ip:
        id = key.split("-")[0]
        candidateID_dict[id] = {"address": "",
                                "port": "", "location": "", "type": ""}

    for key in stats.keys():
        if ("-address" in key or "-relatedAddress" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["address"] = json.loads(list_str)[0]
            candidateID_dict[id]["location"] = stats[key]['statsType'].split(
                "-")[0]
        elif ("-port" in key or "-relatedPort" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["port"] = json.loads(list_str)[0]
            if ("-relatedPort" in key):
                candidateID_dict[id]["port"] = str(
                    json.loads(list_str)[0]) + " (related)"
        elif ("-candidateType" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["type"] = json.loads(list_str)[0]

    # print(candidateID_dict)

    return candidateID_dict


def extract_icecandidate(json_data):
    log = json_data["updateLog"]  # log is a list
    sdpMid_list = []
    ice_dict = {}

    for info_dict in log:
        text = info_dict["value"]
        if (info_dict["type"] == "transceiverAdded"):
            sdpMid_list.append(find_media_kind(text))
        elif (info_dict["type"] == "icecandidate"):
            sdpMid = find_media_num(text)
            subtext = text.split("typ")[0]
            
            # ipv4_addr = find_ipv4(subtext)
            # ipv6_addr = find_ipv6(subtext)
            # if (len(ipv4_addr) >= 1):
            #     ip = ipv4_addr
            # elif (len(ipv6_addr) >= 1):
            #     ip = ipv6_addr
            # ip = ip[0] + "_" + ip[1]
            
            subsubtext = subtext.split(" ")
            addr = subsubtext[len(subsubtext)-3]
            port = subsubtext[len(subsubtext)-2]
            ip = addr + "_" + port
            
            ice_dict[ip] = {}
            try:
                ice_dict[ip]["media"] = str(sdpMid) + "_" + sdpMid_list[sdpMid]
            except:
                ice_dict[ip]["media"] = str(sdpMid)
            ice_dict[ip]["type"] = find_addr_type(text)
            ice_dict[ip]["protocol"] = find_protocol(text)
            remote_ip = find_remote_ip(text)
            if (remote_ip != ""):
                ice_dict[ip]["remote"] = remote_ip
            else:
                ice_dict[ip]["remote"] = ""
            

    return ice_dict
    # pass


def identify_os():
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'Mac OS'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    else:
        return 'Unknown'


def find_protocol(text):
    try:
        pattern = r'\b(\w+)\s+(\w+)\s+(\d+)\b'
        result = re.search(pattern, text)
        matched_text = result.group(2)
    except:
        matched_text = ""
    return matched_text


def find_remote_ip(text):
    try:
        pattern = r'raddr\s+(.*?)\s+rport\s+(.*?) '
        result = re.search(pattern, text)
        matched_text = result.group(1) + "_" + result.group(2)
    except:
        matched_text = ""
    return matched_text


def find_addr_type(text):
    try:
        pattern = r"typ (.*?) "
        result = re.search(pattern, text)
        matched_text = result.group(1)
    except:
        matched_text = ""
    return matched_text


def find_media_num(text):
    pattern = r"sdpMid:(.*?),"
    result = re.search(pattern, text)
    return int(result.group(1).strip())


def find_media_kind(text):
    try:
        pattern = r"kind:'(.*?)'"
        result = re.search(pattern, text)
        matched_text = result.group(1)
    except:
        matched_text = ""
    return matched_text


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


if __name__ == "__main__":
    if (identify_os() == 'Windows'):
        divider = "\\"
    elif (identify_os() == 'Mac OS'):
        divider = "/"

    # file_name_caller = "webrtc_dump_caller.txt"
    # file_name_receiver = "webrtc_dump_receiver.txt"
    file_name_caller = "dump_caller.txt"
    file_name_receiver = "dump_receiver.txt"
    file_names = [file_name_caller, file_name_receiver]
    location_names = ["caller", "receiver"]

    ip_dict = {}
    for i in range(2):
        location_name1 = location_names[i]
        location_name2 = location_names[1-i]
        file_name = file_names[i]
        dump_json = unpack_dump(base_dir + divider +
                                "inputs" + divider + file_name)

        candidateID_dict = extract_candidateID(dump_json)
        for key in candidateID_dict.keys():
            if (len(candidateID_dict[key]["address"]) != 0):
                new_key = candidateID_dict[key]["address"] + \
                    "_" + str(candidateID_dict[key]["port"])
                ip_dict[new_key] = {}
                ip_dict[new_key]["type"] = candidateID_dict[key]["type"]
                if (candidateID_dict[key]["location"] == "local"):
                    ip_dict[new_key]["location"] = location_name1
                else:
                    ip_dict[new_key]["location"] = location_name2

        ice_dict = extract_icecandidate(dump_json)
        for key in ice_dict.keys():
            if (key not in ip_dict.keys()):
                ip_dict[key] = {}
            ip_dict[key]["type"] = ice_dict[key]["type"]
            ip_dict[key]["media"] = ice_dict[key]["media"]
            ip_dict[key]["protocol"] = ice_dict[key]["protocol"]
            ip_dict[key]["remote"] = ice_dict[key]["remote"]
        # print(ice_dict)

    # print(ip_dict)

    import pandas as pd

    # Convert dictionary to pandas DataFrame
    df = pd.DataFrame.from_dict(ip_dict, orient='index')

    # Save DataFrame to Excel
    df.to_excel(base_dir +  divider + "outputs" + divider + 'ip info.xlsx', index_label='Keys')
