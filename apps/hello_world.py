#! /usr/bin/env python3
'''
Hello World app
'''
from common import get_controller_events
from time import sleep
if __name__ == "__main__":
    print("Welcome to R36S-Bioinformatics!")
    print("This 'Hello, World!' app will print your button inputs.")
    print("To exit, press 'START' and 'SELECT' simultaneously.")
    button_state = dict()
    while True:
        for event in get_gamepad():
            button_state[INPUT_TO_R36S[event.code]] = event.state
            if (button_state['START'] + button_state['SELECT']) == 2:
                exit()
