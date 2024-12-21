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
ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY = "\t<system>\n\t\t<name>Bioinformatics</name>\n\t\t<fullname>Bioinformatics</fullname>\n\t\t<path>{roms_dir}/bioinformatics/</path>\n\t\t<extension>.sh .SH</extension>\n\t\t<command>sudo chmod 666 /dev/tty1; %ROM% 2>&1 > /dev/tty1; printf \"\\033c\" >> /dev/tty1</command>\n\t\t<platform>bioinformatics</platform>\n\t\t<theme>bioinformatics</theme>\n\t</system>"
DEPS_LINUX = ['cmake', 'g++', 'git', 'libc6-dev', 'libsdl2-dev', 'libsdl2-ttf-dev', 'libstdc++-9-dev', 'linux-libc-dev', 'make', 'ninja-build', 'python3', 'python3-pip']
DEPS_PYTHON = ['prompt_toolkit', 'pysdl2', 'pysdl2-dll']

# print to log
def print_log(s='', end='\n', file=stdout):
    print(s, end=end, file=file); file.flush()

# print greeting message
def greet():
    print_log("=== R36S-Bioinformatics Configure v%s ===" % VERSION)

# print an error message and exit
def error(s='', end='\n', returncode=1):
    print_log('ERROR: %s' % s, end=end); exit(returncode)

# get the size of a `Path`
def get_path_size(path):
    if not path.exists():
        return 0
    elif path.is_file():
        return path.stat().st_size
    else:
        total = 0
        for p in path.rglob('*'):
            if p.is_file():
                total += p.stat().st_size
        return total

# search for roms directory (either `/roms` or `/roms2`)
def find_roms_path():
    print_log("Searching for roms directory...", end=' ')
    roms_path_size, roms_path = max((get_path_size(path), path) for path in [Path('/roms'), Path('/roms2')])
    if roms_path_size == 0:
        error("Both `/roms` and `/roms2` are empty or non-existent")
    print_log("done")
    return roms_path

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
def update_es_systems_cfg(roms_path):
    print_log("Checking if %s needs to be updated..." % ES_SYSTEMS_CFG_PATH, end=' ')
    with open(ES_SYSTEMS_CFG_PATH) as f:
        cfg_data = f.read()
    if ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY in cfg_data:
        print_log("No updates needed.")
    else:
        with open(ES_SYSTEMS_CFG_BACKUP_PATH, 'w') as f:
            f.write(cfg_data)
        with open(ES_SYSTEMS_CFG_PATH, 'w') as f:
            f.write(cfg_data.replace('</systemList>','%s\n</systemList>' % ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY.replace('{roms_dir}',str(roms_path))))
        print_log("Updated successfully.")

# install dependencies
def install_deps():
    print_log("Installing Linux dependencies...")
    proc = run(['sudo', 'apt-get', 'update', '-y'])
    proc = run(['sudo', 'apt-get', 'install', '--reinstall', '-y'] + DEPS_LINUX)
    if proc.returncode == 0:
        print_log("Successfully installed Linux dependencies.")
    else:
        error("Failed to install Linux dependencies!")
    print_log("Installing Python dependencies...")
    proc = run(['python3', '-m', 'pip', 'install', '--upgrade', '--no-cache-dir'] + DEPS_PYTHON)
    if proc.returncode == 0:
        print_log("Successfully installed Python dependencies.")
    else:
        error("Failed to install Python dependencies!")

# set up `/roms` (or `/roms2`) directory
def setup_roms_dir(roms_path):
    bioinformatics_path = roms_path / 'bioinformatics'
    print_log("Setting up `%s`..." % bioinformatics_path, end=' ')
    bioinformatics_path.mkdir(parents=False, exist_ok=True)
    with open(bioinformatics_path / 'configure.sh', 'w') as f:
        f.write("python3 %s\n" % Path(__file__).resolve())
    print_log("done")

# reboot system
def reboot_system():
    run(['sudo', 'reboot'])

# main program logic
def main():
    greet()
    args = parse_args()
    if not args.skip_update:
        pull_latest()
    install_deps()
    roms_path = find_roms_path()
    update_es_systems_cfg(roms_path)
    setup_roms_dir(roms_path)
    if not args.skip_reboot:
        reboot_system()

# run program
if __name__ == "__main__":
    main()
