from src.gen_files.ConsoleHelpers import input_helper as ih
from src.gen_files import gen_scripts as gs

def remove_suffix_from_names(lst):
    return [str.replace('AT', '') for str in lst]


lst =  ih.get_input_list("a")
lst = remove_suffix_from_names(lst)
print('\n\n\n\n')
print(gs.open_list_as_string(lst, '\n'))