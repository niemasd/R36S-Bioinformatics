#! /usr/bin/env python3
'''
Configure R36S-Bioinformatics
'''

# imports
from subprocess import run
import argparse

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
    command = ['git', 'pull']
    print("Checking for updates...", end=' ')
    proc = run(command, capture_output=True)
    if proc.returncode != 0:
        error("Failed to check for updates via `git pull`. Make sure your R36S has internet connection.")
    if 'Updating' in proc.stdout.decode():
        print("Updated successfully. Rerunning...")
    else:
        print("No updates available.")

# main program logic
def main():
    args = parse_args()
    if not args.skip_update:
        pull_latest()

# run program
if __name__ == "__main__":
    main()
