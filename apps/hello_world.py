#! /usr/bin/env python3
'''
Hello World app
'''
from common import get_controller_events
if __name__ == "__main__":
    print("Welcome to R36S-Bioinformatics!")
    print("This 'Hello, World!' app will print your button inputs.")
    print("To exit, press 'START' and 'SELECT' simultaneously.")
    button_state = dict()
    for button, state in get_controller_events():
        print("Button: %s\tState: %d" % (button, state))
        button_state[button] = state
        if (button_state['START'] + button_state['SELECT']) == 2:
            exit()
