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
    start_pressed = False; select_pressed = False
    for button, state in get_controller_events():
        print("Button: %s\tState: %s" % (button, state))
        sleep(1)
        if button == 'START':
            print("IN IF START")
            sleep(1)
            start_pressed = (state == 1)
            print("START PRESSED UPDATE")
            sleep(1)
        elif button == 'SELECT':
            print("IN ELIF SELECT")
            sleep(1)
            select_pressed = (state == 1)
            print("SELECT PRESSED UPDATE")
            sleep(1)
        print("BEFORE EXIT CHECK")
        sleep(1)
        if start_pressed and select_pressed:
            print("Exiting :-)")
            sleep(5)
            exit()
