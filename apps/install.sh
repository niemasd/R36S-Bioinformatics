#!/bin/bash
# app to run install.sh

# set things up
sudo rg351p-js2xbox --silent -t oga_joypad &
sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# run app
echo "Finding install script in home directory (~)..."
INSTALL_SH=$(find ~ -name 'install.sh' 2> /dev/null | grep 'R36S-Bioinformatics/install.sh' | head -1)
if [[ -z "${INSTALL_SH}" ]] ; then
    echo "ERROR: R36S-Bioinformatics/install.sh not found"
    sleep 5
else
    echo "Running install script: $INSTALL_SH" #&& echo "" && cd $(echo $INSTALL_SH | rev | cut -d'/' -f2- | rev) && git pull && "$INSTALL_SH"
fi

# finish up
KILL_PID=$(pidof rg351p-js2xbox)
if [[ ! -z "${KILL_PID}" ]] ; then
    sudo kill $(pidof rg351p-js2xbox)
fi
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
