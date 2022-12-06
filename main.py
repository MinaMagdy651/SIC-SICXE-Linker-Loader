import pandas as pd
from pandasgui import show

from utils import open_file
from absolute_loader import absolute_loader
from  SICXE_linker_loader import linker_loader

program = open_file('in2.txt')
#memory_graph = absolute_loader(program)
memory_graph = linker_loader(program)
show(memory_graph)