#! /usr/bin/env python3
'''
Minimap2 app
'''
from common import message_dialog, select_file, select_options_dialog
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
            ("Run", "Run"),
            (None, "Quit"),
        ]
        result = select_options_dialog(title=title, values=values)
        if result is None:
            break
        elif result == "Run":
            if ref_path is None:
                message_dialog(title="ERROR", text="Must select a reference genome")
            elif len(reads_path) == 0:
                message_dialog(title="ERROR", text="Must select at least one reads file")
            elif minimap2_preset is None:
                message_dialog(title="ERROR", text="Must select a Minimap2 preset")
            elif out_prefix is None:
                message_dialog(title="ERROR", text="Must enter an output file prefix")
            else:
                exit() # TODO RUN MINIMAP2
