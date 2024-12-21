#! /usr/bin/env python3
'''
File browser app
'''
from common import select_file, view_file_info
from pathlib import Path
from prompt_toolkit.shortcuts import message_dialog
if __name__ == "__main__":
    print("RUNNING FILE BROWSER APP")
    message_dialog(title="FILE BROWSER", text="FILE BROWSER").run()
    curr_path = Path('/')
    while True:
        result = select_file(curr_path=curr_path)
        if result is None:
            break
        else:
            view_file_info(result)
            curr_path = result.parent
