#!/usr/bin/python
# by Pedro Arilla

import time
import sys
import os

def masthead():
    print "========================================"
    print "|               POMOTHON               |"
    print "========================================"

tomato = "\U0001F345"
clock = "\U000023F3"
help = "\U0001F4A1"
bye = "\U0001F44B"
tgreen = "\033[32m"
tdefault = "\033[m"
i = 0
n = 0
log = []

os.system("cls" if os.name == "nt" else "clear")
masthead()
print("\r")
while True:
    pomodoro = raw_input("Start a new pomodoro (Y/N)? ").lower()
    if pomodoro in "n":
        break
    if pomodoro in "y":
        task = raw_input("Task name: ")
        os.system("cls" if os.name == "nt" else "clear")
        t = 1500
        i += 1
        masthead()
        print("\r")
        print tomato.decode("unicode-escape") + " Pomodoro #%s:" %i + " " + task
        print help.decode("unicode-escape") + " (Ctrl+C to finish)"
        try:
            while t:
                sys.stdout.write("\r")
                mins, secs = divmod(t, 60)
                timer = clock.decode("unicode-escape") + " Time left: {:02d}:{:02d}".format(mins, secs)
                sys.stdout.write(timer)
                sys.stdout.flush()
                time.sleep(1)
                t -= 1
                result = True
        except KeyboardInterrupt:
            why = raw_input("\n\nFinished or Aborted (F/A)? ").lower()
            if why in "f":
                result = True
            if why in "a":
                result = False
            pass
        log.append([result,i,task,1500-t])
        os.system("cls" if os.name == "nt" else "clear")
        masthead()
        print("\a")
        if result:
            n += 1
            print "Pomodoro #%s completed!" %i
            print "Take a break no longer than 5 minutes.\n"
os.system("cls" if os.name == "nt" else "clear")
masthead()
print("\a")
print "You've completed %s pomodori today.\n" %n
time = 0
print "#\tMin\tTask"
print "----------------------------------------"
for row in log:
    if row[0]:
        minutes = row[3]/60
        print tgreen + "%s" %row[1] + "\t" + "%s" %minutes + "\t" + row[2] + tdefault
        time += row[3]
    else:
        minutes = row[3]/60
        print "%s" %row[1] + "\t" + "%s" %minutes + "\t" + row[2]
m, s = divmod(time, 60)
h, m = divmod(m, 60)
print "\nEffective working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
print "See you later!" + bye.decode("unicode-escape") + "\n"
