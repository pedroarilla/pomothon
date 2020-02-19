#!/usr/bin/python
# Pomothon v2.0
# by Pedro Arilla

import sys
import os
import json
import time
class emoji:
    tomato = "\U0001F345"
    clock = "\U000023F3"
    help = "\U0001F4A1"
    bye = "\U0001F44B"
class colour:
    green = "\033[32m"
    grey = "\033[2m"
    default = "\033[m"
i = 0 # Number of pomodori
j = 0 # Number of completed pomodori
log = [] # [pomodoro1, pomodoro2, pomodoro3...]
         # where pomodoro is:
         # [finished/aborted, position, name, time, project]
project = [] # [personal/work, position, name, time, new/existing]
pomotime = 1500 # Set in seconds -- can be customised
json_default = "{\"1\": {\"name\": \"Miscellaneous\", \"time\": 0}}"

def checkFiles():
    if not os.path.exists("data"):
        os.makedirs("data")
        with open(os.path.join("data", "personal.json"), "wb") as temp_file:
            temp_file.write(json_default)
        with open(os.path.join("data", "work.json"), "wb") as temp_file:
            temp_file.write(json_default)

def masthead(escape):
    os.system("cls" if os.name == "nt" else "clear")
    print "========================================"
    print "|               POMOTHON               |"
    print "========================================"
    if escape:
        print "\r"
    else:
        print "\a"

def pomodoro(i,j,log,project):
    while True:
        pomodoro = raw_input("Start a pomodoro in this project (Y/N)? ").lower()
        if pomodoro in "n":
            masthead(True)
            break
        if pomodoro in "y":
            task = raw_input("Task name: ")
            t = pomotime
            i += 1
            masthead(True)
            print emoji.tomato.decode("unicode-escape") + " Pomodoro #%s:" %i + " " + task + " [" + project[2] + "]"
            print emoji.help.decode("unicode-escape") + " (Ctrl+C to finish)"
            try:
                while t:
                    sys.stdout.write("\r")
                    mins, secs = divmod(t, 60)
                    timer = emoji.clock.decode("unicode-escape") + " Time left: {:02d}:{:02d}".format(mins, secs)
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
            task_time = pomotime - t
            log.append([result,i,task,task_time,project])
            masthead(False)
            if result:
                j += 1
                print "Pomodoro #%s completed!" %i
                print "Take a break no longer than 5 minutes.\n"
                task_time = task_time / 60
                proj_time = int(project[3]) + task_time
                dict[str(project[1])] = {"name": project[2], "time": proj_time}
    return i, j, log, dict

while True:
    checkFiles()
    masthead(True)
    proj_class = raw_input("(P)ersonal project\n(W)ork project\n(E)xit? ").lower()
    if proj_class in "p":
        proj_file = "data/personal.json"
        proj_message = "> PERSONAL FILE\n"
    elif proj_class in "w":
        proj_file = "data/work.json"
        proj_message = "> WORK FILE\n"
    elif proj_class in "e":
        break
    else:
        continue
    with open(proj_file) as f:
        dict = json.load(f)
    while True:
        masthead(True)
        print proj_message
        proj_option = raw_input("(S)elect an existing project\n(C)reate a new project\n(B)ack? ").lower()
        if proj_option in "s":
            masthead(True)
            ### To-do: What if there are a lot of projects?
            print "{:3}{:5}{:20}".format("#", "Min", "Project")
            print "-" * 40
            print colour.grey + "{:1}{:2}{:3}{:2}{:20}".format(0, "", "---", "", "[Press 0 to go back]") + colour.default
            x = 1
            while x <= len(dict):
                 print "{:1}{:2}{:03d}{:2}{:20}".format(x, "", int(dict[str(x)]["time"]), "", dict[str(x)]["name"])
                 x += 1
            print "\a"
            while True:
                ### To-do: What if I want to delete a project?
                proj_sel = raw_input("Select a project: ")
                try:
                    int(proj_sel)
                except ValueError:
                    True
                else:
                    if int(proj_sel) <= len(dict):
                        if int(proj_sel) == 0:
                            break
                        else:
                            project = [proj_class, proj_sel, dict[proj_sel]["name"], dict[proj_sel]["time"], False]
                            i, j, log, dict = pomodoro(i,j,log,project)
                            break
        if proj_option in "c":
            proj_name = raw_input("\nProject name: ")
            project = [proj_class, len(dict)+1, proj_name, 0, True]
            i, j, log, dict = pomodoro(i,j,log,project)
        if proj_option in "b":
            break
    with open(proj_file, "w") as f:
        json.dump(dict, f)
masthead(False)
print "You've completed %s pomodori today.\n" %j
if j > 0:
    session_time = 0
    print "{:4}{:5}{:20}{:24}".format("##", "Min", "Project", "Task")
    print "-" * 50
    for row in log:
        minutes = row[3]/60
        ### To-do: What if the string got diacritics?
        log_summary = "{:02d}{:2}{:03d}{:2}{:20}{:24}".format(row[1], "", minutes, "", row[4][2], row[2])
        if row[0]:
            print colour.green + log_summary + colour.default
            session_time += row[3]
        else:
            print log_summary
    m, s = divmod(session_time, 60)
    h, m = divmod(m, 60)
    print "\nEffective working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
print "See you later!" + emoji.bye.decode("unicode-escape") + "\n"
