import json


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
    stats = PC_data[focus_key]["stats"]
    candidateID_dict = {}

    # Extract keys containing "-ip"
    keys_with_ip = [key for key in stats.keys() if "-ip" in key]

    for key in keys_with_ip:
        id = key.split("-")[0]
        candidateID_dict[id] = {"address": "",
                                "port": "", "location": "", "type": ""}

    for key in stats.keys():
        if ("-address" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["address"] = json.loads(list_str)[0]
            candidateID_dict[id]["location"] = stats[key]['statsType'].split(
                "-")[0]
        elif ("-port" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["port"] = json.loads(list_str)[0]
        elif ("-candidateType" in key):
            id = key.split("-")[0]
            list_str = stats[key]['values']
            candidateID_dict[id]["type"] = json.loads(list_str)[0]

    # print(candidateID_dict)

    return candidateID_dict


file_name_caller = "Dump Host.txt"
file_name_receiver = "Dump Peer.txt"
caller_dict = unpack_dump(file_name_caller)
receiver_dict = unpack_dump(file_name_receiver)

ip_dict = {}
for key in caller_dict.keys():
    if (len(caller_dict[key]["address"]) != 0):
        new_key = caller_dict[key]["address"] + ":" + str(caller_dict[key]["port"])
        ip_dict[new_key] = {}
        ip_dict[new_key]["type"] = caller_dict[key]["type"]
        if (caller_dict[key]["location"] == "local"):
            ip_dict[new_key]["location"] = "caller"
        else:  
            ip_dict[new_key]["location"] = "receiver"
        
for key in receiver_dict.keys():
    if (len(receiver_dict[key]["address"]) != 0):
        new_key = receiver_dict[key]["address"] + ":" + str(receiver_dict[key]["port"])
        ip_dict[new_key] = {}
        ip_dict[new_key]["type"] = receiver_dict[key]["type"]
        if (receiver_dict[key]["location"] == "local"):
            ip_dict[new_key]["location"] = "receiver"
        else:  
            ip_dict[new_key]["location"] = "caller"

print(ip_dict)

import pandas as pd

# Convert dictionary to pandas DataFrame
df = pd.DataFrame.from_dict(ip_dict, orient='index')

# Save DataFrame to Excel
df.to_excel('output.xlsx', index_label='Keys')
    

