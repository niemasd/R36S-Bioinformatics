#! /usr/bin/env python3
'''
Common functions and classes for R36S-Bioinformatics
'''

# general imports
from pathlib import Path

# general constants
ROOT_PATH = Path('/')

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

# generator to yield each controller event as (button, state) tuples
# button states: 0 = unpressed; 1 = pressed
# joystick states: 0 = neutral; <0 = left (X) or up (Y); >0 = right (X) or down (Y)
def get_controller_events():
    while True:
        events = get_gamepad()
        for event in events:
            if event.code in INPUT_TO_R36S:
                yield (INPUT_TO_R36S[event.code], event.state)

'''
# file selector
def select_file(curr_path=Path('~').resolve(), select_folder=False):
    title = "Select File/Folder"
    while True:
        text = "Current Directory: %s" % curr_path
        values = list()
        if select_folder and curr_path.is_dir():
            values.append((curr_path.parent, HTML('<ansigreen>=== Select Current Directory ===</ansigreen>')))
        if curr_path != ROOT_PATH:
            values.append((curr_path.parent, HTML('<ansiblue>..</ansiblue>')))
        values += sorted(((p, HTML('<ansiblue>%s</ansiblue>' % p.name) if p.is_dir() else p.name) for p in curr_path.glob('*')), key=lambda x: x[0].name.lower())
        result = radiolist_dialog(title=title, text=text, values=values).run()
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
    text = '- <ansiblue>Path:</ansiblue> %s' % path
    text += '\n- <ansiblue>Size:</ansiblue> %s bytes' % '{:,}'.format(stat_result.st_size)
    text = HTML(text)
    message_dialog(title=title, text=text).run()
'''
