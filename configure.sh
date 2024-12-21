#!/usr/bin/env bash
# Configure R36S-Bioinformatics

# constants
VERSION='0.0.1'
ES_SYSTEMS_CFG_PATH='/etc/emulationstation/es_systems.cfg'
ES_SYSTEMS_CFG_BACKUP_PATH="$ES_SYSTEMS_CFG_PATH.r36s-bioinformatics.bak"
DEPS_LINUX='cmake g++ git libc6-dev libsdl2-dev libsdl2-ttf-dev libstdc++-9-dev linux-libc-dev make ninja-build python3 python3-pip'
DEPS_PYTHON='prompt_toolkit pysdl2 pysdl2-dll'

# set things up
sudo rg351p-js2xbox --silent -t oga_joypad &
sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# run configuration script
echo "=== R36S-Bioinformatics Configure v$VERSION ==="
echo "Checking for updates to configuration script..."
GIT_UPDATED=$(git pull | grep "Updating")
if [[ -z "${GIT_UPDATED}" ]] ; then
    echo "No updates available."
else
    echo "Updated successfully. Rerunning..."
    bash $0
    exit 0
fi

# finish up
KILL_PID=$(pidof rg351p-js2xbox)
if [[ -z "${KILL_PID}" ]] ; then
    echo sudo kill $(pidof rg351p-js2xbox)
fi
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
