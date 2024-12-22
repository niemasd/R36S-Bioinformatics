#!/usr/bin/env bash
# execute Hello World app
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "HELLO WORLD START"
python3 "$SCRIPT_DIR/hello_world.py"
echo "HELLO WORLD END"
sleep 5
