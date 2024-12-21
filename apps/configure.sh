#!/bin/bash
sudo rg351p-js2xbox --silent -t oga_joypad &
sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
echo "Finding configuration script in home directory (~)..."
CONFIG_PY=$(find ~ -name 'configure.py' 2> /dev/null | grep 'hiR36S-Bioinformatics/configure.py' | head -1)
if [[ -z "${CONFIG_PY}" ]] ; then
    echo "ERROR: R36S-Bioinformatics/configure.py not found"
    sleep 5
else
    echo "Running configuration script: $CONFIG_PY" && echo "" && python3 "$CONFIG_PY"
fi
sudo kill $(pidof rg351p-js2xbox)
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
