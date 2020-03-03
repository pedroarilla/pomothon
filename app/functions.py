#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules
import os
import sys
import json
import time
from app.classes import *

# Variables
pomotime = 1500 # Set in seconds -- can be customised

# Checks that files exist and creates them if necessary
def checkFiles():
    if not os.path.exists("data"):
        os.makedirs("data")
        json_default = "{\"1\": {\"name\": \"Miscellaneous\", \"time\": 0}}"
        with open(os.path.join("data", "personal.json"), "wb") as temp_file:
            temp_file.write(json_default)
        with open(os.path.join("data", "work.json"), "wb") as temp_file:
            temp_file.write(json_default)
        with open(os.path.join("data", "archive.json"), "wb") as temp_file:
            temp_file.write("{}")

# Cleans the screen and prints app masthead
def masthead(escape):
    os.system("cls" if os.name == "nt" else "clear")
    pomothon = " POMOTHON" + colour.grey + " v2.70 " + colour.default
    print "========================================"
    print "|           " + pomothon + "           |"
    print "========================================"
    if escape:
        print "\r"
    else:
        print "\a"

# Prints a simple dot animation (loading)
def dotdotdot():
    for dot in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(.3)

# Selecs a project
def selectProject(len_dict):
    print "\r"
    while True:
        proj_sel = raw_input("Select a project (#): ")
        try:
            int(proj_sel)
        except ValueError:
            True
        else:
            if int(proj_sel) <= len_dict:
                if int(proj_sel) <= 0:
                    True
                else:
                    return proj_sel

# Pomodoro timer
def pomodoro(i,j,log,dict,project,proj_file):
    masthead(True)
    while True:
        option = raw_input("In this project [" + project[2] + "]:\n(P)omodoro\n(T)imer\n(M)anual record\n(B)ack? ").lower()
        if option in "b":
            masthead(True)
            break
        if option in "t":
            # Preparing
            task = raw_input("\nTask name: ")
            t = 0
            i += 1
            # Initiating
            masthead(True)
            print emoji.tomato.decode("unicode-escape") + " " + task + " [" + project[2] + "]"
            print emoji.help.decode("unicode-escape") + " (Ctrl+C to finish)"
            try:
                while t >= 0:
                    # Timer
                    sys.stdout.write("\r")
                    mins, secs = divmod(t, 60)
                    timer = emoji.clock.decode("unicode-escape") + " Time spent: {:02d}:{:02d}".format(mins, secs)
                    sys.stdout.write(timer)
                    sys.stdout.flush()
                    time.sleep(1)
                    t += 1
                    result = True
            # Time stop
            except KeyboardInterrupt:
                why = raw_input("\n\n(F)inished or (A)borted? ").lower()
                if why in "f":
                    result = True
                if why in "a":
                    result = False
                pass
            # Adding to the log
            log.append([result,i,task,t,project])
            # Pomodoro summary
            masthead(False)
            if result:
                j += 1
                print emoji.tomato.decode("unicode-escape") + colour.green + " Task completed!" + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]"
                print emoji.nap.decode("unicode-escape") + " Take a break.\n"
                # Adding to the dictionary
                project[3] = int(project[3]) + t
                dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
                # Dumping dictionary into project file
                with open(proj_file, "w") as f:
                    json.dump(dict, f)
            else:
                print emoji.tomato.decode("unicode-escape") + colour.red + " Task not completed :(" + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]\n"
        if option in "m":
            # Preparing
            i += 1
            task = raw_input("\nTask name: ")
            # Getting time value
            while True:
                t = raw_input("Time to add (in minutes): ")
                try:
                    int(t)
                except ValueError:
                    True
                else:
                    if int(t) <= 0:
                        True
                    else:
                        break
            # Updating log
            task_time = int(t) * 60
            log.append([True,i,task,task_time,project])
            # Adding to the dictionary
            t = int(t)*60
            project[3] = int(project[3]) + t
            dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
            # Dumping dictionary into project file
            with open(proj_file, "w") as f:
                json.dump(dict, f)
            # Showing that the project has been updated
            print "Updating project",
            dotdotdot()
            masthead(True)
            print emoji.file.decode("unicode-escape") + colour.green + " " + task + " added to " + project[2] + "!\n"  + colour.default
        if option in "p":
            # Preparing
            task = raw_input("\nTask name: ")
            t = pomotime
            i += 1
            # Initiating
            masthead(True)
            print emoji.tomato.decode("unicode-escape") + " " + task + " [" + project[2] + "]"
            print emoji.help.decode("unicode-escape") + " (Ctrl+C to finish)"
            try:
                while t:
                    # Timer
                    sys.stdout.write("\r")
                    mins, secs = divmod(t, 60)
                    timer = emoji.clock.decode("unicode-escape") + " Time left: {:02d}:{:02d}".format(mins, secs)
                    sys.stdout.write(timer)
                    sys.stdout.flush()
                    time.sleep(1)
                    t -= 1
                    result = True
            # Early stop
            except KeyboardInterrupt:
                why = raw_input("\n\n(F)inished or (A)borted? ").lower()
                if why in "f":
                    result = True
                if why in "a":
                    result = False
                pass
            # Adding to the log
            task_time = pomotime - t
            log.append([result,i,task,task_time,project])
            # Pomodoro summary
            masthead(False)
            if result:
                j += 1
                print emoji.tomato.decode("unicode-escape") + colour.green + " Pomodoro completed!" + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]"
                print emoji.nap.decode("unicode-escape") + " Take a break no longer than 5 minutes.\n"
                # Adding to the dictionary
                project[3] = int(project[3]) + task_time
                dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
                # Dumping dictionary into project file
                with open(proj_file, "w") as f:
                    json.dump(dict, f)
            else:
                print emoji.tomato.decode("unicode-escape") + colour.red + " Pomodoro not completed :(" %i + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]\n"
    return i, j, log, dict, project

# Archives selected project
def archive(dict, proj_sel, proj_class, proj_file):
    # Getting archive file into archive dictionary
    with open("data/archive.json") as f:
        archive = json.load(f)
    # Appending project to archive dictionary
    archive[str(len(archive) + 1)] = {"type": proj_class, "name": dict[proj_sel]["name"], "time": dict[proj_sel]["time"]}
    # Dumping archive dictionary into archive file
    with open("data/archive.json", "w") as f:
        json.dump(archive, f)
    # Deleting project from projects dictionary
    len_dict = len(dict)
    del dict[proj_sel]
    # Renumber all the projects
    proj_sel = int(proj_sel)
    while proj_sel < len_dict:
        dict[str(proj_sel)] = {"name": dict[str(proj_sel+1)]["name"], "time": dict[str(proj_sel+1)]["time"]}
        proj_sel += 1
        del dict[str(proj_sel)]
    # Dump dictionary into projects file
    with open(proj_file, "w") as f:
        json.dump(dict, f)
    # Showing that the project has been archived
    print "Archiving project",
    dotdotdot()
    return dict
