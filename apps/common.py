#! /usr/bin/env python3
'''
Common functions and classes for R36S-Bioinformatics
'''

# general imports
from pathlib import Path

# general constants
ROOT_PATH = Path('/')

# import prompt_toolkit
try:
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog, radiolist_dialog
except:
    raise RuntimeError("Missing Python package 'prompt_toolkit'. Try rerunning the R36S-Bioinformatics 'INSTALL' app.")

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
