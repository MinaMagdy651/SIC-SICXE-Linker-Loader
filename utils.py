import re
def open_file(file):
    with open(file) as f:
        program = [line[: -1] for line in f]
    return program


def add_hex(num1, num2):
    return hex(int(num1, 16) + int(num2, 16))[2: ].upper()

def get_prog_dimension(head_record):
    start = head_record[9: 13]
    length = head_record[15: ]
    return start, add_hex(start, length)

def get_memory_dimension(start, length):
    memory_start = start[: 3] + str(0)
    memory_end = length[: 2] + hex(int(length[3], 16) + 1)[2: ].upper() + str(0)
    return memory_start, memory_end

def get_memory_addresses(memory_start, memory_end):
    memory_addresses = []
    while(int(memory_start, 16) <= int(memory_end, 16)):
        memory_addresses.append(memory_start)
        memory_start = add_hex(memory_start, '10')
    return memory_addresses

def get_text_records(program):
    text_records = []
    for line in program:
        if line[0] == 'T':
            text_records.append(text_record(line))
    return text_records

def text_record(text_record):
    start = text_record[3: 7]
    values = re.findall('..?', text_record[9: ])
    return {
        'Start': start,
        'Values': values
    }