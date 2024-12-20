#! /usr/bin/env python3
'''
Configure R36S-Bioinformatics
'''

# imports
from pathlib import Path
from subprocess import run
import argparse

# constants
VERSION = '0.0.1'
ES_SYSTEMS_CFG_PATH = Path('/etc/emulationstation/es_systems.cfg')
ES_SYSTEMS_CFG_BACKUP_PATH = ES_SYSTEMS_CFG_PATH.with_suffix('.r36s-bioinformatics.bak')
ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY = ""

# print greeting message
def greet():
    print("=== R36S-Bioinformatics Configure v%s ===" % VERSION)

# print an error message and exit
def error(s='', end='\n', returncode=1):
    print(s, end=end); exit(returncode)

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--skip_update', action='store_true', help="Skip Update (git pull)")
    args = parser.parse_args()
    return args

# pull the latest updates from GitHub
def pull_latest():
    print("Checking for updates...", end=' ')
    proc = run(['git', 'pull'], capture_output=True)
    if proc.returncode != 0:
        error("Failed to check for updates via `git pull`. Make sure your R36S has internet connection.")
    if 'Updating' in proc.stdout.decode():
        print("Updated successfully. Rerunning...\n")
        run(['python3', __file__, '--skip_update'])
        exit()
    else:
        print("No updates available.")

# update the `/etc/emulationstation/es_systems.cfg` file
def update_es_systems_cfg():
    print("Checking if %s needs to be updated..." % ES_SYSTEMS_CFG_PATH, end=' ')
    with open(ES_SYSTEMS_CFG_PATH) as f:
        cfg_data = f.read()
    if '<name>R36S-Bioinformatics</name>' in cfg_data:
        print("No updates needed.")
    else:
        with open(ES_SYSTEMS_CFG_BACKUP_PATH, 'w') as f:
            f.write(cfg_data)
        with open(ES_SYSTEMS_CFG_PATH, 'w') as f:
            f.write(cfg_data.replace('</systemList>','%s</systemList>' % ES_SYSTEMS_CFG_BIOINFORMATICS_SYSTEM_ENTRY))
        print("Updated successfully.")

# main program logic
def main():
    greet()
    args = parse_args()
    if not args.skip_update:
        pull_latest()
    update_es_systems_cfg()

# run program
if __name__ == "__main__":
    main()
