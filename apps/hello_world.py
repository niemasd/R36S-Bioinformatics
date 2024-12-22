#! /usr/bin/env python3
'''
Hello World app
'''
from inputs import get_gamepad
def main():
    while True:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)
if __name__ == "__main__":
    main()
