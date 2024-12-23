#!/usr/bin/env bash
# app to update dependencies
VERSION='1.0.0'
echo "                            = Update System v$VERSION ="
echo "Updating Linux dependencies..."
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get autoremove -y && sudo apt-get clean
echo "Updating Python dependencies..."
python3 -m pip list --outdated | awk 'NR>2 {print $1}' | xargs -n1 python3 -m pip install --upgrade --no-cache-dir
echo "Rebooting system in 5 seconds..."
sleep 5
sudo reboot
