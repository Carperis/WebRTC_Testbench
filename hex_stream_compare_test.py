colors = {
        # 'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        # 'white': '\033[37m',
        'reset': '\033[0m'
    }

def highlight_common_sequences(string1, string2, n):
    highlighted_string1 = string1
    highlighted_string2 = string2
    common_sequences = []

    i = 0
    while i < len(string1)-n:
        match_flag = False
        match_flag_old = False
        for j in range(i + n - 1, len(string1)):
            sequence = string1[i:j+1]
            match_flag_old = match_flag
            if sequence in string2:
                match_flag = True
                if (match_flag and j == len(string1)-1):
                    common_sequences.append(sequence)
                    break
            else:
                match_flag = False
                if (match_flag_old and not match_flag):
                    common_sequences.append(string1[i:j])
                break
        if (match_flag):
            i = j + 1
        elif (match_flag_old):
            i = j
        i += 1
    
    i = 0
    numofcolors = 6
    for sequence in common_sequences:
        color = list(colors.keys())[i%numofcolors]
        highlighted_string1 = highlighted_string1.replace(
            sequence, get_colored_text(sequence, color))
        highlighted_string2 = highlighted_string2.replace(
            sequence, get_colored_text(sequence, color))
        i += 1

    return highlighted_string1, highlighted_string2

def get_colored_text(text, color):
    if color in colors:
        colored_text = f"{colors[color]}{text}{colors['reset']}"
        return colored_text
    else:
        return text
    
# def print_six_columns(string):
#     columns = [string[i:i+2] for i in range(0, len(string), 2)]
#     rows = [columns[i:i+6] for i in range(0, len(columns), 6)]

#     for row in rows:
#         formatted_row = ' '.join(row)
#         print(formatted_row)

import textwrap

def print_six_columns(string):
    columns = textwrap.wrap(string, 2)
    rows = textwrap.wrap(' '.join(columns), 48)

    for row in rows:
        print(row)

        
string1 = "dceb690a884d2c8db173945208004500011ec1950000801100000a0000bf4216d487ec3dc356010a227890ef1b512374d809907f173ebede000231000110b70000005ac7809216493a82ae8b4b061fc9ddad74e8542fb5cdc5a5972e3eb2adc4310728700334f54484a4f32cce3fbcbad80d3f1ba5c44672b42b25abc42117a57ba8108641b4e4e5ae4a7549bca2ff2207935b6d04a99fe53317b34fb87b1c73c8b47822193cd367f0ecefc10bc10fd85efec0879490c03b6e95e8d4a4c3d489f5c4c705db308c7dfd449d8af8a4fd3eef90a081e33838ebefe013eeab06e1e4f2206c0663473d840bf85a1d43fd6e640a9f5842258254f231c18d905a6b5c1e9ed97dc98cfb5341ca761ca40fdb62c4ab8b1db519d11d1b708232da1a951f3304f71bdae243aef5ec1cf486"
string2 = "dceb690a884d2c8db173945208004500006cc19c0000801100000a0000bf4216d487ec3dc356005821c6b06f1b582374d809907f173ebede000131000800d7cec3d565cdc01ba37692f08730591a77818ca65b23d25d143c880e70aa5596e3bfb7d8de40f8bf264e88e770e52c7f84ff31215360b7f4abe7519e"
n = 4

highlighted_string1, highlighted_string2 = highlight_common_sequences(
    string1, string2, n)

print("\nstring1 =\n", highlighted_string1)
# print_six_columns(highlighted_string1)
print("\nstring2 =\n", highlighted_string2)
# print_six_columns(highlighted_string2)
