#!/usr/bin/env bash
# test app
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
python3 "$SCRIPT_DIR/test.py"
