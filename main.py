import pandas as pd
from pandasgui import show

from utils import open_file
from absolute_loader import absolute_loader

program = open_file('in1.txt')
memory_graph = absolute_loader(program)
show(memory_graph)