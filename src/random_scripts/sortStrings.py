
import src.gen_files.ConsoleHelpers.input_helper as ih
import src.gen_files.gen_scripts as gs

lst = ih.get_input_list("enter strings, separated by \\n")
lst = [string.strip() for string in lst]
lst = sorted(lst)

str = gs.open_list_as_string(lst, '\n')
print(str)
