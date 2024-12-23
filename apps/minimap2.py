#! /usr/bin/env python3
'''
Minimap2 app
'''
from common import select_file, select_options_dialog
from pathlib import Path
VERSION = '1.0.0'
if __name__ == "__main__":
    title = "Minimap2 App v%s" % VERSION
    ref_path = None
    reads_paths = list()
    minimap2_preset = None
    out_prefix = None
    while True:
        values = [
            (None, "Quit"),
        ]
        result = select_options_dialog(title=title, values=values)
        if result is None:
            break
