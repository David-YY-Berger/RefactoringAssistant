
from colorama import init

init()


class TextColors:

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = "\033[38;5;245m"

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    END = '\033[0m'

    NOTE_COLOR = CYAN + BOLD
    WARNING_COLOR = RED + BOLD
    HEADER_COLOR = GRAY + BOLD + UNDERLINE

def print_box(text, width=100, bold=False):
    box_line = '+' + '-' * (width - 2) + '+'
    if bold:
        content_line = '| ' + TextColors.BOLD + text.center(width - 4) + TextColors.END + ' |'
    else:
        content_line = '| ' + text.center(width - 4) + ' |'

    print('\n')
    print(box_line)
    print(content_line)
    print(box_line)


def print_centered(text, width=100, bold=False):
    if bold:
        centered_line = TextColors.BOLD + text.center(width) + TextColors.END
    else:
        centered_line = text.center(width)

    print(centered_line)


def print_step_separator(step_string):
    separator = '-'
    num_to_add = 100 - len(step_string)
    step_text = TextColors.BOLD + step_string + TextColors.END
    print(separator * 5, step_text + ':', separator * num_to_add, '\n')


def print_things_to_remember(note_list):
    if not isinstance(note_list, list) or not all(isinstance(note, str) for note in note_list):
        raise ValueError("Note list must be a list of strings.")
    if not note_list:
        print("No notes to display.")
        return
    print(TextColors.NOTE_COLOR +  "\tA few things to remember:" + TextColors.END)
    for note in note_list:
        print(TextColors.NOTE_COLOR + f"\t\t * {note}")

    print(TextColors.END + '\n')


def print_note(msg):
    print(TextColors.NOTE_COLOR + msg + TextColors.END)


def print_warning(msg):
    print(TextColors.WARNING_COLOR + msg + TextColors.END)


def print_header(msg):
    print(TextColors.HEADER_COLOR + msg + ":" + TextColors.END )


