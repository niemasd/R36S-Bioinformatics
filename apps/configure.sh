#!/bin/bash
sudo rg351p-js2xbox --silent -t oga_joypad &
sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
echo "Finding configuration script in home directory (~)..."
CONFIG_SH=$(find ~ -name 'configure.sh' 2> /dev/null | grep 'R36S-Bioinformatics/configure.sh' | head -1)
if [[ -z "${CONFIG_SH}" ]] ; then
    echo "ERROR: R36S-Bioinformatics/configure.sh not found"
    sleep 5
else
    echo "Running configuration script: $CONFIG_SH" && echo "" && "$CONFIG_SH"
fi
sudo kill $(pidof rg351p-js2xbox)
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
