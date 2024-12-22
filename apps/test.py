#! /usr/bin/env python3
from common import text_input_dialog
from time import sleep
if __name__ == "__main__":
    s = text_input_dialog(title="Test Input Title", text="Test Input Text", curr_string="Niema")
    print_lines("Here's your text:\n=================\n%s" % s)
    sleep(5)
