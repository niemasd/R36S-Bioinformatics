#! /usr/bin/env python3
'''
Configure R36S-Bioinformatics
'''

# imports
from subprocess import run

# print an error message and exit
def error(s='', end='\n', returncode=1):
    print(s, end=end); exit(returncode)

# pull the latest updates from GitHub
def pull_latest():
    command = ['git', 'pull']
    print("Checking for updates...")
    proc = run(command, capture_output=True)
    if proc.returncode != 0:
        error("Failed to check for updates via `git pull`. Make sure your R36S has internet connection.")
    print(proc.returncode)

# main program logic
def main():
    pull_latest()

# run program
if __name__ == "__main__":
    main()
