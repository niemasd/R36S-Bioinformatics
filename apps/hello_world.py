#! /usr/bin/env python3
'''
Hello World app
'''
import sdl2
import sdl2.ext
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
joystick = sdl2.SDL_JoystickOpen(0)
sdl2.ext.Window("test", size=(640,480),position=(0,0),flags=sdl2.SDL_WINDOW_SHOWN)
window.refresh())
while True:
    for event in sdl2.ext.get_events():
        if event.type==sdl2.SDL_KEYDOWN:
            print sdl2.SDL_GetKeyName(event.key.keysym.sym).lower()
        elif event.type==sdl2.SDL_JOYAXISMOTION:
            print [event.jaxis.axis,event.jaxis.value]
