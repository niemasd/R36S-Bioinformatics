#! /usr/bin/env python3
from common import clear_screen, text_input_dialog
from time import sleep
if __name__ == "__main__":
    s = text_input_dialog(title="Test Input Title", text="Test Input Text", curr_string="Niema")
    clear_screen()
    print("Here's your text:\n=================\n%s" % s)
    sleep(5)
