#!/usr/bin/env bash
# execute file browser app
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python3 "$SCRIPT_DIR/hello_world.py"
sleep 5
