from functools import reduce
from operator import mul


def hex_to_bin(x):
    bits = len(x) * 4
    val = int(x, base=16)
    return f'{val:0>{bits}b}'


def parse_packet(packet, cursor=0):
    version = int(packet[cursor:cursor + 3], base=2)
    cursor += 3
    type_id = int(packet[cursor:cursor + 3], base=2)
    cursor += 3

    parsed_packet = {'version': version, 'type_id': type_id, 'value': None}

    if type_id == 4:
        last_group = False
        value_bits = ''
        while not last_group:
            last_group = packet[cursor] == '0'
            cursor += 1
            value_bits += packet[cursor:cursor + 4]
            cursor += 4
        value = int(value_bits, base=2)
        parsed_packet['value'] = value

    else:
        length_type_id = packet[cursor]
        cursor += 1
        if length_type_id == '0':
            subpacket_bit_length = int(packet[cursor:cursor + 15], base=2)
            cursor += 15
            stop_index = cursor + subpacket_bit_length
            subpackets = []
            while cursor < stop_index:
                subpacket, cursor = parse_packet(packet, cursor)
                subpackets.append(subpacket)
        else:
            num_subpackets = int(packet[cursor:cursor + 11], base=2)
            cursor += 11
            subpackets = []
            for i in range(num_subpackets):
                subpacket, cursor = parse_packet(packet, cursor)
                subpackets.append(subpacket)
        parsed_packet['value'] = subpackets

    return parsed_packet, cursor


def calculate_part_1(parsed_packet):
    res = parsed_packet['version']
    if parsed_packet['type_id'] != 4:
        for subpacket in parsed_packet['value']:
            res += calculate_part_1(subpacket)
    return res


def calculate_part_2(parsed_packet):
    type_id = parsed_packet['type_id']
    if type_id == 4:
        return parsed_packet['value']

    values = [calculate_part_2(p) for p in parsed_packet['value']]

    if type_id == 0:
        return sum(values)
    elif type_id == 1:
        return reduce(mul, values)
    elif type_id == 2:
        return min(values)
    elif type_id == 3:
        return max(values)
    elif type_id == 5:
        return 1 if values[0] > values[1] else 0
    elif type_id == 6:
        return 1 if values[0] < values[1] else 0
    elif type_id == 7:
        return 1 if values[0] == values[1] else 0


with open('input') as f:
    packet_hex = next(f).strip()

packet = hex_to_bin(packet_hex)
parsed_packet, _ = parse_packet(packet)

print(calculate_part_1(parsed_packet))
print(calculate_part_2(parsed_packet))
