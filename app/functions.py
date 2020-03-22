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
appVersion = " v2.82 " # r20200322

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
    if not os.path.exists("logs"):
        os.makedirs("logs")

# Cleans the screen and prints app masthead
def masthead(escape):
    os.system("cls" if os.name == "nt" else "clear")
    pomothon = " POMOTHON" + colour.grey + appVersion + colour.default
    print "========================================"
    print "|           " + pomothon + "           |"
    print "========================================"
    if escape:
        print "\r"
    else:
        print "\a"

# Prints a simple dot animation (loading)
def dotdotdot(x):
    for dot in range(x):
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
def pomodoro(i,log,dict,project,proj_file):
    masthead(True)
    while True:
        option = raw_input("In this project [" + project[2] + "]:\n\n(P)omodoro\n(T)imer\n(M)anual record\n(B)ack? ").lower()
        if option in "b":
            break
        elif option in "t":
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
                ##### To-do: Repeat when another key different to F or A is pressed
                if why in "f":
                    result = True
                if why in "a":
                    result = False
                pass
            # Pomodoro summary
            masthead(False)
            if result:
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
            # Adding to the log
            log.append([result,i,task,t,project,project[3]])
            session_time = 0
            for row in log:
                if row[0]:
                    session_time += row[3]
            m, s = divmod(session_time, 60)
            h, m = divmod(m, 60)
            print "Today's working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
        elif option in "m":
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
            # Adding to the dictionary
            task_time = int(t) * 60
            project[3] = int(project[3]) + task_time
            dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
            # Dumping dictionary into project file
            with open(proj_file, "w") as f:
                json.dump(dict, f)
            # Updating log
            log.append([True,i,task,task_time,project,project[3]])
            # Showing that the project has been updated
            print "Updating project",
            dotdotdot(5)
            masthead(True)
            print emoji.file.decode("unicode-escape") + colour.green + " " + task + " added to " + project[2] + "!\n"  + colour.default
            session_time = 0
            for row in log:
                if row[0]:
                    session_time += row[3]
            m, s = divmod(session_time, 60)
            h, m = divmod(m, 60)
            print "Today's working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
        elif option in "p":
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
            # Pomodoro summary
            masthead(False)
            task_time = pomotime - t
            if result:
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
                print emoji.tomato.decode("unicode-escape") + colour.red + " Pomodoro not completed :(" + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]\n"
            # Adding to the log
            log.append([result,i,task,task_time,project,project[3]])
            session_time = 0
            for row in log:
                if row[0]:
                    session_time += row[3]
            m, s = divmod(session_time, 60)
            h, m = divmod(m, 60)
            print "Today's working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
        else:
            masthead(True)
    return i, log, dict, project

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
    dotdotdot(5)
    return dict

# Makes the log prettier for a more readable archiving
def cleanLog(log):
    cleanlog = []
    for row in log:
        if row[4][0] in "p":
            type = "personal"
        elif row[4][0] in "w":
            type = "work"
        if row[0]:
            logitem = str(row[1]) + ": " + row[2] + " [" + type + ", " + row[4][2] + "], " + str(int(row[3])/60) + " minutes -- total in the project: " + str(int(row[5])/60) + " minutes."
        else:
            logitem = str(row[1]) + ": " + row[2] + " [" + row[4][2] + "] aborted."
        cleanlog.append(logitem)
    return cleanlog
