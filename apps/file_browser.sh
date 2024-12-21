#!/usr/bin/env bash
# execute file browser app
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo python3 "$SCRIPT_DIR/file_browser.py"
sleep 5
