import pandas as pd
from utils import get_prog_dimension, get_memory_dimension, get_memory_addresses, get_text_records, add_hex
def empty_memory_graph():
    return pd.DataFrame(columns = ['Memory_Address', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'])

def memory_allocation(text_records, memory_graph):
    for record in text_records:
        start = record['Start'][:-1] + '0'
        column = record['Start'][-1]
        values = record['Values']
        index = memory_graph[memory_graph.Memory_Address == start].index

        for value in values:
            memory_graph.loc[index, column] = value
            column = add_hex(column, '1')

            if column == '10':
                index += 1
                column = '0'
    return memory_graph

def absolute_loader(program):
    start, length = get_prog_dimension(program[0])
    text_records = get_text_records(program)

    memory_start, memory_end = get_memory_dimension(start, length)
    memory_addresses = get_memory_addresses(memory_start, memory_end)

    memory_graph = empty_memory_graph()
    memory_graph.Memory_Address = memory_addresses
    memory_graph.fillna('xx', inplace = True)

    memory_graph = memory_allocation(text_records, memory_graph)

    return memory_graph