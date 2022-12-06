import pandas as pd
import re
from utils import add_hex, sub_hex, get_memory_dimension, get_memory_addresses, get_text_records, memory_allocation, empty_memory_graph, out_estab

def control_section_head_info(head_record):
    name = head_record[1: 7].strip()
    length = head_record[15: ]
    return name, length

def control_section_defintion_reference(definition, reference):
    definition = definition[1: ]
    definition = re.findall('......?', definition)
    i = 0
    definitions = []
    while i < len(definition):
        symbol = definition[i].strip()
        address = definition[i+1][2:]
        definitions.append({
            'Symbol': symbol,
            'Address': address
        })
        i += 2
    
    reference = reference[1: ]
    reference = re.findall('......?', reference)
    references = [var.strip() for var in reference]
    
    return definitions, references

def control_section_modification(control_section):
    modification_list = []
    for line in control_section:
        if line[0] == 'M':
            address = line[1: 7]
            size = line[7: 9]
            operation = line[9: ]
            modification_list.append({
                'Address': address,
                'Size': size,
                'Operation': operation
            })
            
    return  modification_list

def get_control_sections(program):
    control_sections = []
    control_section = []
    for line in program:
        control_section.append(line)
        if(line[0] == 'E'):
            name, length = control_section_head_info(control_section[0])
            definitions, references = control_section_defintion_reference(control_section[1], control_section[2])
            t_records = get_text_records(control_section)
            modification_list = control_section_modification(control_section)
            control_section_obj = {
                'Name': name,
                'Length': length,
                'Definitions': definitions,
                'References': references,
                'T-Records' : t_records,
                'M-Records': modification_list
            }
            control_sections.append(control_section_obj)
            control_section = []

    return control_sections

def get_estab_df(control_sections, starting_address):
    dict = []
    total_length = starting_address
    for control_section in control_sections:
        name = control_section['Name']
        address = starting_address
        dict.append({
            'Control_Section':name,
            'Symbol_Name': ' ',
            'Address': address,
            'Length': control_section['Length']
        })
        total_length = add_hex(total_length, control_section['Length'])
        
        for definition in control_section['Definitions']:
            symbol = definition['Symbol']
            address = add_hex(definition['Address'], starting_address)
            
            dict.append({
                'Control_Section':' ',
                'Symbol_Name': symbol,
                'Address': address,
                'Length': ' '
                })
        starting_address = add_hex(starting_address, control_section['Length'])
    return pd.DataFrame(dict), total_length
    
def get_estab_dict(estab_df):
    list = {}
    for i in range(len(estab_df)):
        line = estab_df.iloc[i]
        if(line.Control_Section == ' '):
            symbol = line.Symbol_Name
        else:
            symbol = line.Control_Section
        address = line.Address
        list[symbol] = address
        
    return list
    

def sicxe_memory_allocation(control_sections, memory_graph, estab_dict):
    for control_section in control_sections:
        memory_graph = memory_allocation(control_section['T-Records'], memory_graph, estab_dict[control_section['Name']])
    return memory_graph

def memory_modifier(memory_graph, address, size, operation, estab_dict):
    start = address[:-1]+ '0'
    column = address[-1]
    old_column = column
    index = memory_graph[memory_graph.Memory_Address == start].index[0]
    old_index = index
    old_value = ' '
    for i in range(3):
        old_value += memory_graph.loc[index, column]
        column = add_hex(column, '1')
        if column == '10':
            index += 1
            column = '0'
            
    old_value = old_value.strip()
        
    column = old_column
    index = old_index
    
    symbol = operation[1: ]
    operand = estab_dict[symbol]
    if(size == '05'):
        if(operation[0] == '+'):
            new_value = old_value[0] + add_hex(old_value[1: ], operand).zfill(5)
        else:
            new_value = old_value[0] + sub_hex(old_value[1: ], operand).zfill(5)
            
    else:
        if(operation[0] == '+'):
            new_value = add_hex(old_value, operand)
        else:
            new_value = sub_hex(old_value, operand)
            
    
    new_value = new_value.zfill(6)
    #Overflow
    if len(new_value) == 7:
        new_value = new_value[1: ]
        
    new_value = re.findall('..?', new_value)

    for i in range(3):
        memory_graph.loc[index, column] = new_value[i]
        
        column = add_hex(column, '1')
        if column == '10':
            index += 1
            column = '0'
    
    return memory_graph

def apply_m_record(memory_graph, control_sections, estab_dict):
    for control_section in control_sections:
        name = control_section['Name']
        starting_address = estab_dict[name]
        m_records = control_section['M-Records']
        for record in m_records:
            address = add_hex(record['Address'], starting_address)
            size = record['Size']
            operation = record['Operation']
            memory_graph = memory_modifier(memory_graph, address, size, operation, estab_dict)
    return memory_graph

def linker_loader(program):
    starting_address = str(input('Starting Address: '))
    control_sections = get_control_sections(program)
    estab_df, end = get_estab_df(control_sections, starting_address)
    estab_dict = get_estab_dict(estab_df)
    memory_start, memory_end = get_memory_dimension(starting_address, end)
    memory_addresses = get_memory_addresses(memory_start, memory_end)
    
    memory_graph = empty_memory_graph()
    memory_graph.Memory_Address = memory_addresses
    memory_graph.fillna('xx', inplace = True)
    memory_graph = sicxe_memory_allocation(control_sections, memory_graph, estab_dict)
    memory_graph = apply_m_record(memory_graph, control_sections, estab_dict)
    out_estab(estab_df)

    return memory_graph