#! /usr/bin/env python3
'''
Configure R36S-Bioinformatics
'''

# imports
from subprocess import run

# pull the latest updates from GitHub
def pull_latest():
    command = ['git', 'pull']
    print("Checking for updates...")
    proc = run(command, capture_output=True)
    print(proc.returncode)

# main program logic
def main():
    print("Hello, world!")
    pull_latest()

# run program
if __name__ == "__main__":
    main()
