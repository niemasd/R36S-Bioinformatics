#! /usr/bin/env python3
'''
Common functions and classes for R36S-Bioinformatics
'''

# general imports
from gzip import open as gopen
from pathlib import Path
from subprocess import run
from sys import stdout
from time import sleep
import re

# general constants
ROOT_PATH = Path('/')
SCREEN_HEIGHT = 30
SCREEN_WIDTH = 80

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

# virtual keyboard layouts
KEYBOARD_LOWER = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '`'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '\\', 'SPACE'],
]
KEYBOARD_UPPER = [
    ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '~'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', '|', 'SPACE'],
]

# Minimap2 presets
MINIMAP2_PRESETS = {
    'lr:hq':     'accurate long reads (error rate <1%) against a reference genome',
    'splice':    'spliced alignment for long reads',
    'splice:hq': 'spliced alignment for accurate long reads',
    'asm5':      'asm-to-ref mapping, for ~0.1% sequence divergence',
    'asm10':     'asm-to-ref mapping, for ~1% sequence divergence',
    'asm20':     'asm-to-ref mapping, for ~5% sequence divergence',
    'sr':        'short reads against a reference',
    'map-pb':    'CLR vs reference mapping',
    'map-hifi':  'HiFi vs reference mapping',
    'map-ont':   'Nanopore vs reference mapping',
    'map-iclr':  'ICLR vs reference mapping',
    'ava-pb':    'PacBio CLR read overlap',
    'ava-ont':   'Nanopore read overlap',
}

# add spaces to the left of a string to center it to a max length
def pad_to_center(s, max_width=SCREEN_WIDTH):
    visible_length = len(s)
    if visible_length >= max_width:
        return s
    else:
        return ' '*((max_width - visible_length) // 2) + s

# clear the terminal screen
def clear_screen():
    run('clear', shell=True)

# print lines to screen, and try to center around a specific index if there are more lines than the max
def print_lines(lines, center_ind=0, left_col=0, max_width=SCREEN_WIDTH, max_height=SCREEN_HEIGHT):
    if len(lines) <= max_height:
        shown_lines = lines
    else:
        half_height = max_height // 2
        if center_ind - half_height < 0:
            shown_lines = lines[:max_height]
        elif center_ind + half_height > len(lines):
            shown_lines = lines[-max_height:]
        else:
            shown_lines = lines[center_ind - half_height : center_ind + half_height]
    shown_lines = [l[left_col : left_col + max_width] for l in shown_lines]
    clear_screen()
    print('\n'.join(shown_lines), end='')

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
def message_dialog(title=None, text=None, max_width=SCREEN_WIDTH, max_height=SCREEN_HEIGHT, small_jump=5, big_jump=10):
    lines = list()
    if title is not None:
        lines.append(pad_to_center('= %s =' % title))
    if text is not None:
        lines += [s.rstrip() for s in text.splitlines()]
    left_col = 0
    half_height = max_height // 2
    min_ind = half_height
    max_ind = len(lines) - half_height
    curr_ind = min_ind
    while True:
        print_lines(lines, center_ind=curr_ind, left_col=left_col, max_width=max_width, max_height=max_height)
        for button, state in get_controller_events():
            if button == 'LEFTY' or button == 'RIGHTY':
                if state < 0:
                    curr_ind = max(curr_ind - 1, min_ind)
                    break
                elif state > 0:
                    curr_ind = min(curr_ind + 1, max_ind)
                    break
            elif button == 'LEFTX' or button == 'RIGHTX':
                if state < 0:
                    left_col = max(left_col - 1, 0)
                    break
                elif state > 0:
                    left_col += 1
                    break
            elif state == 1:
                if button in {'A', 'B', 'START'}:
                    return
                elif button == 'L1':
                    curr_ind = max(curr_ind - big_jump, min_ind)
                    break
                elif button == 'L2':
                    curr_ind = max(curr_ind - small_jump, min_ind)
                    break
                elif button == 'UP':
                    curr_ind = max(curr_ind - 1, min_ind)
                    break
                elif button == 'R1':
                    curr_ind = min(curr_ind + big_jump, max_ind)
                    break
                elif button == 'R2':
                    curr_ind = min(curr_ind + small_jump, max_ind)
                    break
                elif button == 'DOWN':
                    curr_ind = min(curr_ind + 1, max_ind)
                    break
                elif button == 'LEFT':
                    left_col = max(left_col - 1, 0)
                    break
                elif button == 'RIGHT':
                    left_col += 1
                    break

# mimic the prompt_toolkit radiolist_dialog: https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html#radio-list-dialog
def select_options_dialog(values, title=None, text=None, select_multi=False, small_jump=5, big_jump=10, B_match='( ) ../'):
    # set up title + text
    lines = list()
    if title is not None:
        lines.append(pad_to_center('= %s =' % title))
    if select_multi:
        lines.append(pad_to_center("Press START when selection is complete"))
    lines.append(pad_to_center("Press SELECT to cancel"))
    if text is not None:
        lines += [s.rstrip() for s in text.splitlines()]
    if title is not None or text is not None or select_multi:
        lines.append('') # add empty line between title/text and options

    # set up selection
    first_selectable_ind = len(lines)
    return_values = [None]*len(lines) + [v for v,t in values]
    lines += [('   ( ) ' + t) for v,t in values]
    selection = set()

    # file selection loop
    curr_ind = first_selectable_ind
    left_col = 0 # to allow for scrolling left/right
    while True:
        # print options
        lines[curr_ind] = '-> ' + lines[curr_ind][3:]
        print_lines(lines, center_ind=curr_ind, left_col=left_col)
        lines[curr_ind] = '   ' + lines[curr_ind][3:]

        # listen for user input
        for button, state in get_controller_events():
            if button == 'LEFTY' or button == 'RIGHTY':
                if state < 0:
                    curr_ind = max(curr_ind - 1, first_selectable_ind)
                    break
                elif state > 0:
                    curr_ind = min(curr_ind + 1, len(lines) - 1)
                    break
            elif button == 'LEFTX' or button == 'RIGHTX':
                if state < 0:
                    left_col = max(left_col - 1, 0)
                    break
                elif state > 0:
                    left_col += 1
                    break
            elif state == 1:
                if button == 'A':
                    if select_multi:
                        if curr_ind in selection:
                            selection.remove(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + ' ' + lines[curr_ind][5:]
                            break
                        else:
                            selection.add(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + '*' + lines[curr_ind][5:]
                            break
                    else:
                        return return_values[curr_ind]
                elif button == 'SELECT':
                    return None
                elif button == 'B':
                    tmp = [i for i in range(len(lines)) if lines[i].strip().endswith(B_match)]
                    if len(tmp) != 0:
                        return return_values[tmp[0]]
                elif button == 'START' and select_multi:
                    return [return_values[i] for i in sorted(selection)]
                elif button == 'UP':
                    curr_ind = max(curr_ind - 1, first_selectable_ind)
                    break
                elif button == 'L1':
                    curr_ind = max(curr_ind - big_jump, first_selectable_ind)
                    break
                elif button == 'L2':
                    curr_ind = max(curr_ind - small_jump, first_selectable_ind)
                    break
                elif button == 'DOWN':
                    curr_ind = min(curr_ind + 1, len(lines) - 1)
                    break
                elif button == 'R1':
                    curr_ind = min(curr_ind + big_jump, len(lines) - 1)
                    break
                elif button == 'R2':
                    curr_ind = min(curr_ind + small_jump, len(lines) - 1)
                    break
                elif button == 'LEFT':
                    left_col = max(left_col - 1, 0)
                    break
                elif button == 'RIGHT':
                    left_col += 1
                    break

# mimic the prompt_toolkit input_dialog: https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html#input-box
def text_input_dialog(title=None, text=None, curr_string=''):
    # set things up
    header = list()
    if title is not None:
        header.append(pad_to_center('= %s =' % title))
    header += [pad_to_center("A = select, B = backspace, Y = tab, X = newline, R1/R2/L1/L2 = shift"), pad_to_center("START = finish, SELECT = cancel"), '']
    if text is not None:
        header += [s.rstrip() for s in text.splitlines()]

    # text entry loop
    curr_row = 0
    curr_col = 0
    lower = True
    lr_states = {'L1':0, 'L2':0, 'R1':0, 'R2':0}
    while True:
        keyboard = KEYBOARD_LOWER if lower else KEYBOARD_UPPER
        lines = header + ['', curr_string, ''] + [''.join(('(%s)' % keyboard[row][col]) if (row == curr_row and col == curr_col) else (' %s ' % keyboard[row][col]) for col in range(len(keyboard[row]))) for row in range(len(keyboard))]
        print_lines(lines)
        for button, state in get_controller_events():
            if button in lr_states:
                lr_states[button] = state
                lower = (sum(lr_states.values()) == 0)
                break
            elif button == 'LEFTY' or button == 'RIGHTY':
                if state < 0:
                    curr_row = max(curr_row - 1, 0)
                    break
                elif state > 0:
                    curr_row = min(curr_row + 1, len(keyboard) - 1)
                    break
            elif button == 'LEFTX' or button == 'RIGHTX':
                if state < 0:
                    curr_col = max(curr_col - 1, 0)
                    break
                elif state > 0:
                    curr_col = min(curr_col + 1, len(keyboard[curr_row]) - 1)
                    break
            elif state == 1:
                if button == 'UP':
                    curr_row = max(curr_row - 1, 0)
                    break
                elif button == 'DOWN':
                    curr_row = min(curr_row + 1, len(keyboard) - 1)
                    break
                elif button == 'LEFT':
                    curr_col = max(curr_col - 1, 0)
                    break
                elif button == 'RIGHT':
                    curr_col = min(curr_col + 1, len(keyboard[curr_row]) - 1)
                    break
                elif button == 'START':
                    return curr_string
                elif button == 'SELECT':
                    return None
                elif button == 'A':
                    if keyboard[curr_row][curr_col] == 'SPACE':
                        curr_string += ' '
                    else:
                        curr_string += keyboard[curr_row][curr_col]
                    break
                elif button == 'Y':
                    curr_string += '\t'
                elif button == 'X':
                    curr_string += '\n'
                elif button == 'B':
                    curr_string = curr_string[:-1]
                    break

# file selector
def select_file(curr_path=Path('~').resolve(), select_folder=False, select_multi=False, title="Select File/Folder"):
    while True:
        text = "Current Directory: %s" % curr_path
        values = list()
        if select_folder and curr_path.is_dir():
            values.append(('.', '=== Select Current Directory ==='))
        if curr_path != ROOT_PATH:
            values.append((curr_path.parent, '../'))
        values += sorted(((p, p.name + '/' if p.is_dir() else p.name) for p in curr_path.glob('*') if (not select_folder) or p.is_dir()), key=lambda x: x[0].name.lower())
        result = select_options_dialog(title=title, text=text, values=values, select_multi=select_multi)
        if result == '.':
            return curr_path
        elif result is None or isinstance(result, list) or result.is_file():
            return result
        elif result.is_dir():
            curr_path = result
        else:
            raise ValueError("Invalid selection: %s" % result)

# view file info
def view_file_info(path):
    stat_result = path.stat()
    title = "File Information"
    text = '- Path: %s' % path
    text += '\n- Size: %s bytes' % '{:,}'.format(stat_result.st_size)
    message_dialog(title=title, text=text)

# view text file
def view_text_file(path, max_num_lines=1000):
    truncated = False
    try:
        clear_screen()
        print("Loading file:\n%s" % path)
        if path.suffix.lower() == '.gz':
            f = gopen(path, 'rt')
        else:
            f = open(path, 'rt')
        lines = list()
        for line_num, line in enumerate(f):
            if line_num == max_num_lines:
                truncated = True
                break
            lines.append(line.rstrip('\n').replace('\t', '    '))
        f.close()
    except:
        message_dialog(title="ERROR", text="Failed to open file:\n%s" % path)
        return
    data = '\n'.join(lines)
    if truncated:
        data = "%s\n%s" % (pad_to_center("= ONLY SHOWING FIRST %d LINES =" % max_num_lines), data)
    message_dialog(title=str(path), text=data)
