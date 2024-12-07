#!/usr/bin/env python
# Prepare a menu for CP operations

import sys
import subprocess

from .config import config


# getch-like function taken from
# https://code.activestate.com/recipes/134892/
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
        
getch=_GetchUnix()

help_message="""CPUTILS
1-\tTest
2-\tSubmit
3-\tGit add
d-\tDownload problem data
e-\tOpen in editor
p-\tChange active problem
l-\tChange active language
q-\tLeave
!-\tCustom command
h-\tDisplay help
"""

def main():
    problem = sys.argv[1] if len(sys.argv)>=2 else None
    language = sys.argv[2] if len(sys.argv)>=3 else "py"
    
    option="-"
    print(help_message)
    
    while (option not in "qQ" and option!="\0"):
        print("\n>", end='')
        sys.stdout.flush()
        option=getch()
        
        if option == "1":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Testing")
            subprocess.Popen(
                ["cptest", "--verbose", f"{config['problem_dir']}/{problem}/{problem}.{language}"]
            ).wait()

        elif option == "2":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Submitting")
            subprocess.Popen(
                ["cpsubmit", f"{config['problem_dir']}/{problem}/{problem}.{language}"]
            ).wait()

        elif option == "3":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Adding to git")
            subprocess.Popen(
                ["git", "add", f"{problem}.{language}"], cwd=f"{config['problem_dir']}/{problem}"
            ).wait()
            print("ok")

        elif option in "pP":
            print("New problem name?")
            problem = input()
            print("ok")
        
        elif option in "lL":
            print("New language (extension only)?")
            language = input()
            print("ok")

        elif option in "dD":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Downloading data")
            subprocess.Popen(["mkdir", "-p", f"{config['problem_dir']}/{problem}"]).wait()
            subprocess.Popen(
                ["cpsamples", problem], cwd=config["problem_dir"]
            ).wait()

        elif option in "eE":
            if problem is None:
                print("No problem set. Use 'p' to choose it")
                continue
            print("Opening editor")
            subprocess.Popen(
                [config["editor"], f"{problem}/{problem}.{language}"], cwd=config["problem_dir"]
            ).wait()

        elif option == "!":
            print("Enter command: ")
            cmd = input()
            subprocess.Popen(cmd, cwd=f"{config['problem_dir']}/{problem}", shell=True).wait()

        elif option in "hH":
            print(help_message)
            print(f"Problem: {problem}\nLanguage: {language}")

        elif option in "qQ":
            pass

        else:
            print("Invalid option")
    
    
if __name__ == '__main__':
    main()
