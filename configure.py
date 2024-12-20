#! /usr/bin/env python3
'''
Configure R36S-Bioinformatics
'''

# imports
from pathlib import Path
from subprocess import run
from sys import stdout
import argparse

# constants
VERSION = '0.0.1'
ES_SYSTEMS_CFG_PATH = Path('/etc/emulationstation/es_systems.cfg')
ES_SYSTEMS_CFG_BACKUP_PATH = ES_SYSTEMS_CFG_PATH.parent / (ES_SYSTEMS_CFG_PATH.name + '.r36s-bioinformatics.bak')
ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY = "\t<system>\n\t\t<name>Bioinformatics</name>\n\t\t<fullname>Bioinformatics</fullname>\n\t\t<path>{roms_dir}/bioinformatics/</path>\n\t\t<extension>.py</extension>\n\t\t<command>python3 %ROM%</command>\n\t\t<platform>bioinformatics</platform>\n\t\t<theme>bioinformatics</theme>\n\t</system>"
DEPS_LINUX = ['cmake', 'g++', 'git', 'libc6-dev', 'libsdl2-dev', 'libsdl2-ttf-dev', 'libstdc++-9-dev', 'linux-libc-dev', 'make', 'ninja-build', 'python3']
DEPS_PYTHON = ['prompt_toolkit', 'pysdl2', 'pysdl2-dll']

# print to log
def print_log(s='', end='\n', file=stdout):
    print(s, end=end, file=file); file.flush()

# print greeting message
def greet():
    print_log("=== R36S-Bioinformatics Configure v%s ===" % VERSION)

# print an error message and exit
def error(s='', end='\n', returncode=1):
    print_log(s, end=end); exit(returncode)

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--skip_update', action='store_true', help="Skip Update (git pull)")
    parser.add_argument('--skip_reboot', action='store_true', help="Skip System Reboot")
    args = parser.parse_args()
    return args

# pull the latest updates from GitHub
def pull_latest():
    print_log("Checking for updates...", end=' ')
    proc = run(['git', 'pull'], capture_output=True)
    if proc.returncode != 0:
        error("Failed to check for updates via `git pull`. Make sure your R36S has internet connection.")
    if 'Updating' in proc.stdout.decode():
        print_log("Updated successfully. Rerunning...\n")
        run(['python3', __file__, '--skip_update'])
        exit()
    else:
        print_log("No updates available.")

# update the `/etc/emulationstation/es_systems.cfg` file
def update_es_systems_cfg():
    print_log("Checking if %s needs to be updated..." % ES_SYSTEMS_CFG_PATH, end=' ')
    with open(ES_SYSTEMS_CFG_PATH) as f:
        cfg_data = f.read()
    if ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY in cfg_data:
        print_log("No updates needed.")
    else:
        with open(ES_SYSTEMS_CFG_BACKUP_PATH, 'w') as f:
            f.write(cfg_data)
        with open(ES_SYSTEMS_CFG_PATH, 'w') as f:
            f.write(cfg_data.replace('</systemList>','%s\n</systemList>' % ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY))
        print_log("Updated successfully.")

# install dependencies
def install_deps():
    print_log("Installing Linux dependencies...", end=' ')
    proc = run(['sudo', 'apt-get', 'install', '--reinstall'] + DEPS_LINUX, capture_output=True)
    if proc.returncode == 0:
        print_log("done")
    else:
        error("FAILED!")
    print_log("Installing Python dependencies...", end=' ')
    proc = run(['python3', '-m', 'pip', 'install', '--upgrade', '--no-cache-dir'] + DEPS_PYTHON, capture_output=True)
    if proc.returncode == 0:
        print_log("done")
    else:
        error("FAILED!")

# get the size of a `Path`
def get_path_size(path):
    if not path.exists():
        return 0
    elif path.is_file():
        return path.stat().st_size
    else:
        total = 0
        for p in path.rglob('*'):
            if fn.is_file():
                total += p.stat().st_size
        return total

# set up `/roms` (or `/roms2`) directory
def setup_roms_dir():
    roms_path_size, roms_path = max((get_path_size(path), path) for path in [Path('/roms'), Path('/roms2')])
    if roms_path_size == 0:
        error("Both `/roms` and `/roms2` are empty or non-existent")
    print_log(roms_path)
    exit() # TODO

# reboot system
def reboot_system():
    run(['sudo', 'reboot'])

# main program logic
def main():
    greet()
    args = parse_args()
    if not args.skip_update:
        pull_latest()
    update_es_systems_cfg()
    setup_roms_dir()
    if not args.skip_reboot:
        reboot_system()

# run program
if __name__ == "__main__":
    main()
