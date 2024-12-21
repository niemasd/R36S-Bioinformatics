#!/usr/bin/env bash
# app to update dependencies + apps

# set things up
sudo rg351p-js2xbox --silent -t oga_joypad &
sudo ln -s /dev/input/event3 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick
sudo chmod 777 /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# update Linux and Python dependencies
echo "Updating Linux dependencies..."
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean
echo "Updating Python dependencies..."
python3 -m pip list --outdated | awk 'NR>2 {print $1}' | xargs -n1 python3 -m pip install --upgrade --no-cache-dir

# find and update R36S-Bioinformatics repo path
echo "Finding R36S-Bioinformatics repo in home directory (~)..."
INSTALL_SH=$(find ~ -name 'install.sh' 2> /dev/null | grep 'R36S-Bioinformatics/install.sh' | head -1)
if [[ -z "${INSTALL_SH}" ]] ; then
    echo "R36S-Bioinformatics repo not found. Cloning into home directory (~)..."
    cd ~
    git clone https://github.com/niemasd/R36S-Bioinformatics.git
    INSTALL_SH="$(realpath ~/R36S-Bioinformatics/install.sh)"
fi
REPO_PATH="$(echo $INSTALL_SH | rev | cut -d'/' -f2- | rev)"
echo "Updating R36S-Bioinformatics repo path: $REPO_PATH"
cd "$REPO_PATH" && git pull

# find roms path
echo "Finding roms path..."
if [[ "$(ls /roms | wc -l)" -ge "$(ls /roms2 | wc -l)" ]] ; then
    ROMS='/roms'
else
    ROMS='/roms2'
fi
echo "Found roms path: $ROMS"

# update apps
echo "Updating R36S-Bioinformatics apps..."
rm -rf "$ROMS/bioinformatics" && cp -r "$REPO_PATH/apps" "$ROMS/bioinformatics"
echo "R36S-Bioinformatics successfully updated :-)"
echo "Rebooting system in 5 seconds..."
sleep 5

# finish up
KILL_PID=$(pidof rg351p-js2xbox)
if [[ ! -z "${KILL_PID}" ]] ; then
    sudo kill $(pidof rg351p-js2xbox)
fi
sudo rm /dev/input/by-path/platform-odroidgo2-joypad-event-joystick

# reboot system
sudo reboot
