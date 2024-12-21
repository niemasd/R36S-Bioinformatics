#! /usr/bin/env python3
'''
File browser app
'''
from common import select_file, view_file_info
from pathlib import Path
if __name__ == "__main__":
    curr_path = Path('/')
    while True:
        result = select_file(curr_path=curr_path)
        if result is None:
            break
        else:
            view_file_info(result)
            curr_path = result.parent
