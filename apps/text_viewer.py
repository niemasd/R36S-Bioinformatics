#! /usr/bin/env python3
'''
Text viewer app
'''
from common import select_file, view_text_file
from pathlib import Path
VERSION = '1.0.0'
if __name__ == "__main__":
    curr_path = Path('/')
    while True:
        result = select_file(title="Text Viewer v%s" % VERSION, curr_path=curr_path)
        if result is None:
            break
        else:
            view_text_file(result)
            curr_path = result.parent
