#!/usr/bin/env bash
# execute Hello World app
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python3 "$SCRIPT_DIR/hello_world.py"
