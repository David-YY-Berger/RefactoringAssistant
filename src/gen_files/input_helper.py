

def readable(str):
    return str.capitalize().replace('_', ' ')


def get_input_options(prompt, option_list):
    print(prompt)
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
    return input_list
