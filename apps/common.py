#! /usr/bin/env python3
'''
Common functions and classes for R36S-Bioinformatics
'''

# general imports
from os import system
from pathlib import Path
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

# add spaces to the left of a string to center it to a max length
def pad_to_center(s, max_width=SCREEN_WIDTH):
    visible_length = len(s)
    if visible_length >= max_width:
        return s
    else:
        return ' '*((max_width - visible_length) // 2) + s

# clear the terminal screen
def clear_screen():
    system('clear')

# print lines to screen, and try to center around a specific index if there are more lines than the max
def print_lines(lines, center_ind=0, max_width=SCREEN_WIDTH, max_height=SCREEN_HEIGHT):
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
    shown_lines = [l[:max_width] for l in shown_lines]
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
def message_dialog(title=None, text=None):
    lines = list()
    if title is not None:
        lines.append(pad_to_center('= %s =' % title))
    if text is not None:
        lines += [s.rstrip() for s in text.splitlines()]
    print_lines(lines)
    for button, state in get_controller_events():
        if state == 1 and button in {'A', 'B', 'START'}:
            return

# mimic the prompt_toolkit radiolist_dialog: https://python-prompt-toolkit.readthedocs.io/en/stable/pages/dialogs.html#radio-list-dialog
def select_options_dialog(values, title=None, text=None, select_multi=False, small_jump=5, big_jump=10):
    # set up title + text
    lines = list()
    if title is not None:
        lines.append(pad_to_center('= %s =' % title))
    if select_multi:
        lines.append(pad_to_center("Press START when selection is complete"))
    if text is not None:
        lines += [s.rstrip() for s in text.splitlines()]
    if title is not None or text is not None or select_multi:
        lines.append('') # add empty line between title/text and options

    # set up selection
    values = [(None, "= Cancel =")] + values
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
                    if curr_ind == first_selectable_ind: # Cancel option
                        return None
                    elif select_multi:
                        if curr_ind in selection:
                            selection.remove(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + ' ' + lines[curr_ind][:5]
                            break
                        else:
                            selection.add(curr_ind)
                            lines[curr_ind] = lines[curr_ind][:4] + '*' + lines[curr_ind][:5]
                            break
                    else:
                        return return_values[curr_ind]
                elif button == 'B' and lines[first_selectable_ind + 1] == '   ( ) ../':
                    return return_values[first_selectable_ind + 1]
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

# file selector
def select_file(curr_path=Path('~').resolve(), select_folder=False):
    title = "Select File/Folder"
    while True:
        text = "Current Directory: %s" % curr_path
        values = list()
        if select_folder and curr_path.is_dir():
            values.append((curr_path.parent, '=== Select Current Directory ==='))
        if curr_path != ROOT_PATH:
            values.append((curr_path.parent, '../'))
        values += sorted(((p, p.name + '/' if p.is_dir() else p.name) for p in curr_path.glob('*')), key=lambda x: x[0].name.lower())
        result = select_options_dialog(title=title, text=text, values=values, select_multi=False)
        if result is None or result.is_file():
            return result
        elif result == '..':
            curr_path = curr_path.parent
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
