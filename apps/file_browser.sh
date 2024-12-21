#!/usr/bin/env bash
# execute file browser app

# set things up
#sudo rg351p-js2xbox --silent -t oga_joypad &
#sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
#sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# run app
printf "\e32mHi, Niema!"
#SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
#python3 "$SCRIPT_DIR/file_browser.py"
sleep 5

# finish up
#KILL_PID=$(pidof rg351p-js2xbox)
#if [[ ! -z "${KILL_PID}" ]] ; then
#    sudo kill $(pidof rg351p-js2xbox)
#fi
#sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
