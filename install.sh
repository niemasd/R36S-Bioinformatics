#!/usr/bin/env bash
# Configure R36S-Bioinformatics

# constants
VERSION='0.0.1'
ES_SYSTEMS_CFG_PATH='/etc/emulationstation/es_systems.cfg'
ES_SYSTEMS_CFG_BACKUP_PATH="$ES_SYSTEMS_CFG_PATH.r36s-bioinformatics.bak"
DEPS_LINUX='cmake g++ git libc6-dev libsdl2-dev libsdl2-ttf-dev libstdc++-9-dev linux-libc-dev make ninja-build python3 python3-pip'
DEPS_PYTHON='prompt_toolkit pysdl2 pysdl2-dll'

# greet user
echo "=== R36S-Bioinformatics Configure v$VERSION ==="

# install dependencies
echo "Installing Linux dependencies..."
#(sudo apt-get update && sudo apt-get install -y --reinstall $DEPS_LINUX) || (echo "Failed to install Linux dependencies" && sleep 5 && exit 1)
echo "Installing Python dependencies..."
#(python3 -m pip install --upgrade --no-cache-dir $DEPS_PYTHON) || (echo "Failed to install Python dependencies" && sleep 5 && exit 1)

# find roms path
python3 -c "from pathlib import Path; print(max((get_path_size(path), path) for path in [Path('/roms'), Path('/roms2')])[1])"

# finish up
echo "R36S-Bioinformatics successfully configured :-)"
echo "Rebooting system in 5 seconds..."
sleep 5
#sudo reboot
