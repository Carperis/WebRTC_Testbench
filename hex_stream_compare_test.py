import textwrap
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
    out1 = string1
    out2 = string2
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
        color = list(colors.keys())[i % numofcolors]
        out1 = out1.replace(
            sequence, get_colored_text(sequence, color))
        out2 = out2.replace(
            sequence, get_colored_text(sequence, color))
        i += 1

    return out1, out2


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


def print_six_columns(string):
    columns = textwrap.wrap(string, 2)
    rows = textwrap.wrap(' '.join(columns), 48)

    for row in rows:
        print(row)


binding_request = "dceb690a884d2c8db1739452080045000080c18f0000801100000a0000bf4216d487ec3dc356006c21da000100502112a44254355157556d705736457274000600097a5267393a41777758000000c0570004000003e7802a000859864e73f6de964100250000002400046e001eff00080014a573c50e9fd9faebedd9854516f4ef6377f3f5ea80280004cdb53c31"
binding_success_response = "2c8db1739452dceb690a884d08004500006c7c0740003711a61d4216d4870a0000bfc356ec3d0058878a0101003c2112a44254355157556d705736457274002000080001cd2f6802b9b8000600097a5267393a4177775820202000080014f67672f19152ab35ccba48b4e2fbdcb9e464555c8028000442375a27"
udp1 = "dceb690a884d2c8db173945208004500011ec1950000801100000a0000bf4216d487ec3dc356010a227890ef1b512374d809907f173ebede000231000110b70000005ac7809216493a82ae8b4b061fc9ddad74e8542fb5cdc5a5972e3eb2adc4310728700334f54484a4f32cce3fbcbad80d3f1ba5c44672b42b25abc42117a57ba8108641b4e4e5ae4a7549bca2ff2207935b6d04a99fe53317b34fb87b1c73c8b47822193cd367f0ecefc10bc10fd85efec0879490c03b6e95e8d4a4c3d489f5c4c705db308c7dfd449d8af8a4fd3eef90a081e33838ebefe013eeab06e1e4f2206c0663473d840bf85a1d43fd6e640a9f5842258254f231c18d905a6b5c1e9ed97dc98cfb5341ca761ca40fdb62c4ab8b1db519d11d1b708232da1a951f3304f71bdae243aef5ec1cf486"
udp2 = "dceb690a884d2c8db173945208004500011ac1960000801100000a0000bf4216d487ec3dc35601062274b06f1b522374d809907f173ebede00013100020010ca3dd9badf68f483df0e6623af664f758da34715339a4bdb767906813344aeaa27070108c6851d8fccb754c888184d6399a7ca53c4698de9357367b74a65cc44e5b29953ffb6e003ddf48016e90191575f373681a272ae802dfb858b8bd10ea7a1e785280776df4c50f27963e3b27d2136ea8f7d18a278be2213aeb5e13bf725fcb73d6633110073123889718be2598d308112b14b718eaed6aef4c401dc58c9a9b60faa7cc5c5cb3f61cfafb6b6ab6b4266190eaea3341a216a54fefd83b22a425725e31ac4994797c88d3c21bb17949458646915598ba245230ee7a739b208e8947407d1b4150cc4"
udp3 = "dceb690a884d2c8db173945208004500011ac1970000801100000a0000bf4216d487ec3dc35601062274b06f1b532374d809907f173ebede00013100030007e58c674073ad3c756ffac22f7fb7f5c8099a1532151130ae6922a4cc7c3134ded58bec957c613e1cc4fc6aaa292d6db76e2c49d00d2c8f5ea3076e3eb766196390b84fcff44c4b44a5b4b10736ddb80f692dcf85f6808402e781827e25731fe41e9dcf4be33fe69f9025eb9dcbaab1c79f115034a00668be37846215dc1b85d2d5fcb0a292b243e929942ba5560a7851c0ebbbea2ce994555b18e588c2db22d59ab1b3a3cdff1a1f01172c9880f3338b576cf641906c1ce8883b68c4e4d5d90eb8dd12d9575c11ae9cca3625ba38fdaf39d949431c2a9c152f9f849f63193c73fd848aefe12edf7458"
udpn = "dceb690a884d2c8db17394520800450000dfc1c00000801100000a0000bf4216d487ec3dc35600cb2239906f1b7c23753989907f173ebede000231002c10da000000ad384537caabd0b44f9987ff104cec01c0441f8ef4188d014a71b2b22bcd9468c61a478c06461f4c80f52a1d5b3dec305b7121daabb5bb3160982036d5c3215f174e6bae02f54d1be79ff1a35972855dde485c5f06b8a067d21ec3a3eac5b19710040632055a690e52af210469d7c93a1a22f14b4e58ee8569b201931b941cfc4a186faed6d9211ab6d08c951f277c82a544549f6634dbbd67a2027371870cee77acdaa8cf9563990816d8"
udp1_msg = "dceb690a884d2c8db173945208004500004b1f760000801100000a0000bf9df0f53ac189c41400379e32906f0470ca41079785e59f0ebede00032286a2d531001310ff00000035870a4e07f6859ad24043fd9b0d23c75aa5f2"
udp2_msg = "dceb690a884d2c8db173945208004500004a1f790000801100000a0000bf9df0f53ac189c41400369e31906f0471ca410b5785e59f0ebede00032286b88531001410ff000000a0e3531000282c0c59c963855901a710a7f7"
n = 4

out1, out2 = highlight_common_sequences(
    udpn, udp1_msg, n)
# 7a526739 3a 41777758 = zRg9:AwwX
# 41777758 3a 7a526739 = AwwX:zRg9
# messgae cookie 2112a442
print("\nstring1 =\n", out1)
# print_six_columns(out1)
print("\nstring2 =\n", out2)
# print_six_columns(out2)
