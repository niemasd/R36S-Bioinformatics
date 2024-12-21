#!/usr/bin/env bash
# app to run install.sh
echo "Finding install script in home directory (~)..."
INSTALL_SH=$(find ~ -name 'install.sh' 2> /dev/null | grep 'R36S-Bioinformatics/install.sh' | head -1)
if [[ -z "${INSTALL_SH}" ]] ; then
    echo "Install script not found. Cloning into home directory (~)..."
    cd ~
    git clone https://github.com/niemasd/R36S-Bioinformatics.git
    INSTALL_SH="$(realpath ~/R36S-Bioinformatics/install.sh)"
fi
echo "Running install script: $INSTALL_SH" && echo "" && cd "$(echo $INSTALL_SH | rev | cut -d'/' -f2- | rev)" && git pull && "$INSTALL_SH"
