#! /usr/bin/env python3
'''
Common functions and classes for R36S-Bioinformatics
'''

# general imports
from pathlib import Path
from time import sleep
import re

# general constants
ROOT_PATH = Path('/')
SCREEN_HEIGHT = 30
SCREEN_WIDTH = 80

# ANSI escape sequences: https://jakob-bagterp.github.io/colorist-for-python/ansi-escape-codes/standard-16-colors/#foreground-text-and-background-colors
class ANSI:
    BLACK =   '\033[90m'
    RED =     '\033[91m'
    GREEN =   '\033[92m'
    YELLOW =  '\033[93m'
    BLUE =    '\033[94m'
    MAGENTA = '\033[95m'
    CYAN =    '\033[96m'
    WHITE =   '\033[97m'
    ENDC =    '\033[0m'

# import `inputs`: https://github.com/zeth/inputs
try:
    from inputs import get_gamepad
except:
    raise RuntimeError("Missing Python package 'inputs'. Try rerunning the R36S-Bioinformatics 'INSTALL' app.")

# mapping from `inputs` gamepad to R36S controller
INPUT_TO_R36S = {
    'ABS_RX':             'RIGHTX',
    'ABS_RY':             'RIGHTY',
    'ABS_X':              'LEFTX',
    'ABS_Y':              'LEFTY',
    'BTN_DPAD_DOWN':      'DOWN',
    'BTN_DPAD_LEFT':      'LEFT',
    'BTN_DPAD_RIGHT':     'RIGHT',
    'BTN_DPAD_UP':        'UP',
    'BTN_EAST':           'A',
    'BTN_NORTH':          'X',
    'BTN_SOUTH':          'B',
    'BTN_TL':             'L1',
    'BTN_TL2':            'L2',
    'BTN_TR':             'R1',
    'BTN_TR2':            'R2',
    'BTN_TRIGGER_HAPPY1': 'SELECT',
    'BTN_TRIGGER_HAPPY2': 'START',
    'BTN_TRIGGER_HAPPY3': 'L3',
    'BTN_TRIGGER_HAPPY4': 'R3',
    'BTN_TRIGGER_HAPPY5': 'FN',
    'BTN_WEST':           'Y',
}
R36S_TO_INPUT = {v:k for k,v in INPUT_TO_R36S.items()}

# remove ANSI sequences from a string (e.g. to accurately calculate length): https://stackoverflow.com/a/14693789/2134991
def remove_ansi(s):
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', s)

# add spaces to the left of a string to center it to a max length
def pad_to_center(s, max_width=SCREEN_WIDTH):
    visible_length = len(remove_ansi(s))
    if visible_length >= max_width:
        return s
    else:
        return ' '*((max_width - visible_length) // 2) + s

# print a full-screen blank string to clear the screen
def clear_screen(screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
    print(' '*(screen_width*screen_height))

# generator to yield each controller event as (button, state) tuples
# button states: 0 = unpressed; 1 = pressed
# joystick states: 0 = neutral; <0 = left (X) or up (Y); >0 = right (X) or down (Y)
def get_controller_events():
    while True:
        events = get_gamepad()
        for event in events:
            if event.code in INPUT_TO_R36S:
                yield (INPUT_TO_R36S[event.code], event.state)

# mimic the prompt_toolkit message_dialog: https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html#message-box
def message_dialog(title=None, text=None):
    exit() # TODO

# mimic the prompt_toolkit radiolist_dialog: https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html#radio-list-dialog
def select_options_dialog(values, title=None, text=None, select_multi=False):
    # set up title + text
    lines = [''] # start with empty line to make sure we're at the start of a line for actual content
    if title is not None:
        lines.append(pad_to_center(ANSI.MAGENTA + '= ' + title + ' =' + ANSI.ENDC))
    if select_multi:
        lines.append(pad_to_center(ANSI.YELLOW + 'Press START when selection is complete' + ANSI.ENDC))
    if text is not None:
        lines += [s.rstrip() for s in text.splitlines()]
    if title is not None or text is not None or select_multi:
        lines.append('') # add empty line between title/text and options

    # set up selection
    first_selectable_ind = len(lines)
    values = [(None, ANSI.RED + "= Cancel =" + ANSI.ENDC)] + values
    return_values = [None] + [v for v,t in values]
    lines += [('   ( ) ' + t) for v,t in values]
    selection = set()

    # file selection loop
    curr_ind = first_selectable_ind
    while True:
        # print options
        lines[curr_ind] = '-> ' + lines[curr_ind][3:]
        clear_screen()
        print('\n'.join(lines), end='')
        lines[curr_ind] = '   ' + lines[curr_ind][3:]

        # listen for user input
        for button, state in get_controller_events():
            if button == 'LEFTY' or button == 'RIGHTY':
                if state < 0 and curr_ind > first_selectable_ind:
                    curr_ind -= 1
                elif state > 0 and curr_ind < (len(lines) - 1):
                    curr_ind += 1
            elif state == 1:
                if button == 'A':
                    if curr_ind == first_selectable_ind: # Cancel option
                        return None
                    elif select_multi:
                        if curr_ind in selection:
                            selection.remove(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + ' ' + lines[curr_ind][:5]
                        else:
                            selection.add(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + '*' + lines[curr_ind][:5]
                    else:
                        return return_values[curr_ind]
                elif button == 'START' and select_multi:
                    return [return_values[i] for i in sorted(selection)]
                elif button == 'UP' and curr_ind > first_selectable_ind:
                    curr_ind -= 1
                elif button == 'DOWN' and curr_ind < (len(lines) - 1):
                    curr_ind += 1

# file selector
def select_file(curr_path=Path('~').resolve(), select_folder=False):
    title = "Select File/Folder"
    while True:
        text = "Current Directory: %s" % curr_path
        values = list()
        if select_folder and curr_path.is_dir():
            values.append((curr_path.parent, ANSI.GREEN + '=== Select Current Directory ===' + ANSI.ENDC))
        if curr_path != ROOT_PATH:
            values.append((curr_path.parent, ANSI.BLUE + '..' + ANSI.ENDC))
        values += sorted(((p, ANSI.BLUE + p.name + ANSI.ENDC if p.is_dir() else p.name) for p in curr_path.glob('*')), key=lambda x: x[0].name.lower())
        result = select_options_dialog(title=title, text=text, values=values, select_multi=False)
        if result is None or result.is_file():
            return result
        elif result.is_dir():
            curr_path = result
        else:
            raise ValueError("Invalid selection: %s" % result)

# view file info
def view_file_info(path):
    stat_result = path.stat()
    title = "File Information"
    text = ANSI.BLUE + '- Path:' + ANSI.ENDC + (' %s' % path)
    text += ('\n' + ANSI.BLUE + '- Size:' + ANSI.ENDC + (' %s bytes' % '{:,}'.format(stat_result.st_size)))
    message_dialog(title=title, text=text)
