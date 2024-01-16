from src.gen_files.ConsoleHelpers import print_functions as pf

def readable(str):
    return str.capitalize().replace('_', ' ')


def get_input_enum_options(prompt, option_list):
    print(prompt + " (Enter just the number)")
    possible_options = []
    for op in option_list:
        print(str(op.value) + ". " + readable(op.name))
        possible_options.append(str(op.value))
    keep_going = True
    while keep_going:
        cmd = input()
        if not cmd.isnumeric():
            print("Please enter a number")
        elif cmd not in possible_options:
            print("Please only enter one of the given options")
        else:
            keep_going = False
            return int(cmd)


def get_input_list(prompt):
    print(prompt + ". Enter 'end' to finish")
    input_list = []
    buf = " "
    while (buf != "end"):
        input_list.append(buf)
        buf = input()
    input_list = [s for s in input_list if not s.isspace()]
    print("Processing...")
    return input_list


def get_input_ensure_valid(prompt, boolean_function, error_msg):
    buf = ''
    while True:
        buf = input(prompt)
        if boolean_function(buf):
            return buf
        else:
            print(error_msg)


def get_chosen_items_from_list(init_prompt, enter_list_prompt, option_list):
    pf.print_note('\n' + init_prompt)
    print(enter_list_prompt +
          "\nSeparate numbers by whitespace. Enter 'end' to finish: ")
    select_all = 'Select all - recommended'
    option_list = [select_all] + option_list

    for i, option in enumerate(option_list, start=1):
        print(f"{i}. {option}")
    res = set()

    while True:
        user_input = input()
        if user_input.lower() == 'end':
            break
        try:
            # Split the input into a list of integers
            choices = {int(choice) for choice in user_input.split()}
            res.update(option_list[choice - 1] for choice in choices if 1 <= choice <= len(option_list))
        except ValueError:
            print("Invalid input. Please enter valid numbers separated by whitespace.")
    if(res.__contains__(select_all)):
        option_list.remove(select_all)
        return option_list
    else:
        return res

















