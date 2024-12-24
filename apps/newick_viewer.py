#! /usr/bin/env python3
'''
Newick Viewer app
'''
from common import message_dialog, select_file
from pathlib import Path
from subprocess import run
VERSION = '1.0.0'
if __name__ == "__main__":
    curr_path = Path('/')
    while True:
        result = select_file(title="Newick Viewer v%s" % VERSION, curr_path=curr_path)
        if result is None:
            break
        print("Loading file:\n%s" % result)
        if result.suffix.strip().lower() == '.gz':
            command = 'zcat "%s" | nw_display -' % result
        else:
            command = 'nw_display "%s"' % result
        ret = run(command, shell=True, capture_output=True)
        message_dialog(title=str(result), text=ret.stdout.decode())
        curr_path = result.parent
