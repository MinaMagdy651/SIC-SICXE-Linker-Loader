import pandas as pd
from utils import *

def absolute_loader(program):
    #Getting the start and the length
    start, length = get_prog_dimension(program[0])

    #Parsing the T-Records
    text_records = get_text_records(program)

    #Calculating the actual memory start and end
    memory_start, memory_end = get_memory_dimension(start, length)

    #Generating the memory addresses 
    memory_addresses = get_memory_addresses(memory_start, memory_end)

    #Generating and empty memory graph
    memory_graph = empty_memory_graph()

    #Filling the memory with the addresses 
    memory_graph.Memory_Address = memory_addresses

    memory_graph.fillna('xx', inplace = True)

    #Filling the memory with the T-Records 
    memory_graph = memory_allocation(text_records, memory_graph, "0000")

    return memory_graph