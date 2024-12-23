#! /usr/bin/env python3
'''
File browser app
'''
from common import select_file, view_file_info
from pathlib import Path
VERSION = '1.0.0'
if __name__ == "__main__":
    curr_path = Path('/')
    while True:
        result = select_file(title="File Browser v%s" % VERSION, curr_path=curr_path)
        if result is None:
            break
        else:
            view_file_info(result)
            curr_path = result.parent
