#! /usr/bin/env python3
'''
Hello World app
'''
# https://github.com/zeth/inputs
from inputs import get_gamepad
if __name__ == "__main__":
    print("Welcome to R36S-Bioinformatics!")
    print("This 'Hello, World!' app will print your button inputs.")
    print("To exit, press 'START' and 'SELECT' simultaneously.")
    start_pressed = False
    select_pressed = False
    while True:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)
            if event.ev_type == 'Key':
                if event.code == 'BTN_TRIGGER_HAPPY2':
                    start_pressed = (event.state == 1)
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    select_pressed = (event.state == 1)
            if start_pressed and select_pressed:
                break
