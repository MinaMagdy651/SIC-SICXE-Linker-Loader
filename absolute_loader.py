import pandas as pd
from utils import get_prog_dimension, get_memory_dimension, get_memory_addresses, get_text_records, memory_allocation, empty_memory_graph

def absolute_loader(program):
    start, length = get_prog_dimension(program[0])
    text_records = get_text_records(program)

    memory_start, memory_end = get_memory_dimension(start, length)
    memory_addresses = get_memory_addresses(memory_start, memory_end)

    memory_graph = empty_memory_graph()
    memory_graph.Memory_Address = memory_addresses
    memory_graph.fillna('xx', inplace = True)

    memory_graph = memory_allocation(text_records, memory_graph, "0000")

    return memory_graph