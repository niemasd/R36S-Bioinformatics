#! /usr/bin/env python3
'''
Hello World app
'''
from common import get_controller_events
if __name__ == "__main__":
    print("Welcome to R36S-Bioinformatics!")
    print("This 'Hello, World!' app will print your button inputs.")
    print("To exit, press 'START' and 'SELECT' simultaneously.")
    start_pressed = False; select_pressed = False
    for button, state in get_controller_events():
        print("Button: %s\tState: %d" % (button, state))
        if button == 'START':
            start_pressed = (state == 1)
        elif button == 'SELECT':
            select_pressed = (state == 1)
        if start_pressed and select_pressed:
            exit()
