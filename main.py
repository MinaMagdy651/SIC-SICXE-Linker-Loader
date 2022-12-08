from pandasgui import show
from utils import open_file
from absolute_loader import absolute_loader
from  SICXE_linker_loader import linker_loader


path = str(input('File name: '))
path += '.txt'
program = open_file(path)
choice = int(input('Type 1 for SIC Absolute loader, 2 for SICXE Loader-Linker: '))
while True:
    if choice == 1:
        memory_graph = absolute_loader(program)
        break
    elif choice == 2:
        memory_graph = linker_loader(program)
        break
    else:
        print('Wrong Input')
        choice = int(input('Type 1 for SIC Absolute loader, 2 for SICXE Loader-Linker: '))

show(memory_graph)
