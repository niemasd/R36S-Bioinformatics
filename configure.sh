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

# greet user
echo "=== R36S-Bioinformatics Configure v$VERSION ==="

# git pull the latest version
echo "Checking for updates to configuration script..."
if [[ "$(git pull | tr -d '\n')" == "Already up to date." ]] ; then
    echo "No updates available."
else
    echo "Updated successfully"
    bash $0
    exit 0
fi

# install dependencies
echo "Installing Linux dependencies..."
#(sudo apt-get update && sudo apt-get install -y --reinstall $DEPS_LINUX) || (echo "Failed to install Linux dependencies" && sleep 5 && exit 1)
echo "Installing Python dependencies..."
#(python3 -m pip install --upgrade --no-cache-dir $DEPS_PYTHON) || (echo "Failed to install Python dependencies" && sleep 5 && exit 1)

# finish up
echo "R36S-Bioinformatics successfully configured :-)"
sleep 5
KILL_PID=$(pidof rg351p-js2xbox)
if [[ ! -z "${KILL_PID}" ]] ; then
    sudo kill $(pidof rg351p-js2xbox)
fi
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# reboot system
echo "Rebooting system in 5 seconds..."
sleep 5
#sudo reboot
