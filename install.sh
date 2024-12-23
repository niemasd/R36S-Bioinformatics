#!/usr/bin/env bash
# Configure R36S-Bioinformatics

# constants
VERSION='1.0.0'
ES_SYSTEMS_CFG_PATH='/etc/emulationstation/es_systems.cfg'
ES_SYSTEMS_CFG_BACKUP_PATH="$ES_SYSTEMS_CFG_PATH.r36s-bioinformatics.bak"
DEPS_LINUX='autoconf build-essential bzip2 cmake g++ git libbz2-dev libc6-dev libcurl4-openssl-dev liblzma-dev libstdc++-9-dev linux-libc-dev make ninja-build python3 python3-pip wget zlib1g-dev'
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

# install htslib
echo "Installing htslib..."
wget -qO- "https://github.com/samtools/htslib/releases/download/1.21/htslib-1.21.tar.bz2" | tar -xj
cd htslib-*
autoreconf -i
./configure --prefix=/usr
make
sudo make install
cd ..
rm -rf htslib-*

# install Minimap2
echo "Installing Minimap2..."
wget -qO- "https://github.com/lh3/minimap2/archive/refs/tags/v2.28.tar.gz" | tar -zx
cd minimap2-*
make arm_neon=1 aarch64=1
chmod a+x minimap2
sudo mv minimap2 /usr/bin/minimap2
cd ..
rm -rf minimap2-*

# install samtools
echo "Installing samtools..."
wget -qO- "https://github.com/samtools/samtools/releases/download/1.21/samtools-1.21.tar.bz2" | tar -xj
cd samtools-*
./configure --prefix=/usr --without-curses
make
sudo make install
cd ..
rm -rf samtools-*

# install ViralConsensus
echo "Installing ViralConsensus..."
wget -qO- "https://github.com/niemasd/ViralConsensus/archive/refs/tags/0.0.6.tar.gz" | tar -zx
cd ViralConsensus-*
make
sudo mv viral_consensus /usr/bin/viral_consensus
cd ..
rm -rf ViralConsensus-*

# install ViralMSA
echo "Installing ViralMSA..."
sudo wget -q -O /usr/bin/ViralMSA.py "https://github.com/niemasd/ViralMSA/releases/download/1.1.44/ViralMSA.py"
sudo chmod a+x /usr/bin/ViralMSA.py

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
