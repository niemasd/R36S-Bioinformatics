#!/usr/bin/env bash
# Configure R36S-Bioinformatics

# constants
VERSION='1.0.0'
ES_SYSTEMS_CFG_PATH='/etc/emulationstation/es_systems.cfg'
ES_SYSTEMS_CFG_BACKUP_PATH="$ES_SYSTEMS_CFG_PATH.r36s-bioinformatics.bak"
DEPS_LINUX='build-essential cmake g++ git libc6-dev libstdc++-9-dev linux-libc-dev make ninja-build python3 python3-pip wget zlib1g-dev'
DEPS_PYTHON='inputs'
ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY='\t<system>\n\t\t<name>Bioinformatics</name>\n\t\t<fullname>Bioinformatics</fullname>\n\t\t<path>{roms_dir}/bioinformatics/</path>\n\t\t<extension>.sh .SH</extension>\n\t\t<command>sudo chmod 666 /dev/tty1; %ROM% 2>&1 > /dev/tty1; printf "\\033c" >> /dev/tty1</command>\n\t\t<platform>bioinformatics</platform>\n\t\t<theme>bioinformatics</theme>\n\t</system>'

# greet user
echo "                   === R36S-Bioinformatics Install v$VERSION ==="

# install dependencies
echo "Installing Linux dependencies..."
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y --reinstall $DEPS_LINUX
sudo apt-get autoremove
sudo apt-get clean
echo "Installing Python dependencies..."
python3 -m pip install --upgrade --no-cache-dir $DEPS_PYTHON

# install Minimap2
echo "Installing Minimap2..."
wget -qO- "https://github.com/lh3/minimap2/archive/refs/tags/v2.28.tar.gz" | tar -zx
cd minimap2-*
make arm_neon=1 aarch64=1
chmod a+x minimap2
sudo mv minimap2 /usr/bin/minimap2
cd ..
rm -rf minimap2-*

# find roms path
echo "Finding roms path..."
if [[ "$(ls /roms | wc -l)" -ge "$(ls /roms2 | wc -l)" ]] ; then
    ROMS='/roms'
else
    ROMS='/roms2'
fi
echo "Found roms path: $ROMS"

# update es_systems.cfg
if grep -q '<name>Bioinformatics</name>' "$ES_SYSTEMS_CFG_PATH" ; then
    echo "No updates needed in es_systems.cfg"
else
    echo "Updating es_systems.cfg..."
    cp $ES_SYSTEMS_CFG_PATH $ES_SYSTEMS_CFG_BACKUP_PATH
    python3 -c "f = open('$ES_SYSTEMS_CFG_PATH'); cfg_data = f.read(); f.close(); f = open('$ES_SYSTEMS_CFG_PATH','w'); f.write(cfg_data.replace('</systemList>','%s\n</systemList>' % '$ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY'.replace('{roms_dir}','$ROMS'))); f.close()"
fi

# install apps
echo "Installing R36S-Bioinformatics apps..."
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
rm -rf "$ROMS/bioinformatics" && cp -r "$SCRIPT_DIR/apps" "$ROMS/bioinformatics"

# finish up
echo "R36S-Bioinformatics successfully configured :-)"
echo "Rebooting system in 5 seconds..."
sleep 5
sudo reboot
