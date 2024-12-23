#!/usr/bin/env bash
# app to update dependencies + apps
VERSION='1.0.0'

# greet user
echo "                             = Update Apps v$VERSION ="

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
echo "R36S-Bioinformatics apps successfully updated :-)"

# reboot system
echo "Rebooting system in 5 seconds..."
sleep 5
sudo reboot
