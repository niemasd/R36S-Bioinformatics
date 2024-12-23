#! /usr/bin/env python3
'''
Hello World app
'''
from common import get_controller_events, pad_to_center
VERSION = '1.0.0'
if __name__ == "__main__":
    print(pad_to_center("= Hello World v%s =" % VERSION))
    print()
    print("Welcome to R36S-Bioinformatics!")
    print("This 'Hello, World!' app will print your button inputs.")
    print("To exit, press 'START' and 'SELECT' simultaneously.")
    print()
    button_state = {'START':0, 'SELECT':0}
    for button, state in get_controller_events():
        print("Button: %s\tState: %d" % (button, state))
        button_state[button] = state
        if (button_state['START'] + button_state['SELECT']) == 2:
            exit()
