#!/usr/bin/python

import time
import sys
import os

def masthead(extraline):
    print "========================================"
    print "| POMOTHON, a Pomodoro timer in Python |"
    if extraline:
        print "========================================\n"
    else:
        print "========================================"

i = 0
os.system("cls" if os.name == "nt" else "clear")
masthead(True)
while True:
    pomodoro = raw_input("Do you want to start a pomodoro (Y/N)? ").lower()
    if pomodoro in "n":
        break
    if pomodoro in "y":
        os.system("cls" if os.name == "nt" else "clear")
        t = 1500
        i += 1
        masthead(True)
        print "Pomodoro #%s" %i
        while t:
            sys.stdout.write("\r")
            mins, secs = divmod(t, 60)
            timer = ">>>>> {:02d}:{:02d} <<<<<".format(mins, secs)
            sys.stdout.write(timer)
            sys.stdout.flush()
            time.sleep(1)
            t -= 1
        os.system("cls" if os.name == "nt" else "clear")
        masthead(False)
        print("\a")
        print "Pomodoro #%s completed!" %i
        print "\rTake a break no longer than 5 minutes."
    print "----------------------------------------"
print "\rWell done, you completed %s pomodoros.\nSee you later!\n" %i
