#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pomothon v2.60 -- r20200223
# Pedro Arilla -- pedroarilla.com

# Import modules
import sys
import os
import json
import time
from app.functions import *
from app.classes import *

# Variables
i = 0 # Number of pomodori
j = 0 # Number of completed pomodori
log = [] # [pomodoro1, pomodoro2, pomodoro3...]
         # where pomodoro is:
         # [finished/aborted, position, name, time, project]
project = [] # [personal/work, position, name, time, new/existing]

# Main
##### To-do: Solve problem with diacritics
checkFiles()
while True:
    masthead(True)
    # Selection menu
    ##### To-do: What if I want to create a new type of project?
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
    # Dumping JSON file into dictioanry
    with open(proj_file) as f:
        dict = json.load(f)
    while True:
        masthead(True)
        print proj_message
        # Projects list
        ##### To-do: What if there are a lot of projects (+9)?
        print "{:3}{:7}{:20}".format("#", "HH:MM", "Project")
        print "-" * 40
        x = 1
        while x <= len(dict):
            s = int(dict[str(x)]["time"])
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)
            print "{:1}{:2}{:02d}:{:02d}{:2}{:20}".format(x, "", h, m, "", dict[str(x)]["name"])
            x += 1
        print "\a"
        # Selection menu
        proj_option = raw_input("(W)ork on an existing project\n(A)rchive an existing project\n(C)reate a new project\n(B)ack? ").lower()
        # Working on project
        if proj_option in "w":
            # Selecting a project
            proj_sel = selectProject(len(dict))
            project = [proj_class, proj_sel, dict[proj_sel]["name"], dict[proj_sel]["time"], False]
            # Starting pomodoro
            i, j, log, dict, project = pomodoro(i, j, log, dict, project, proj_file)
        # Archiving project
        if proj_option in "a":
            # Selecting a project
            proj_sel = selectProject(len(dict))
            # Archiving the project
            dict = archive(dict, proj_sel, proj_class, proj_file)
        # Creating project
        if proj_option in "c":
            proj_name = raw_input("\nProject name: ")
            project = [proj_class, len(dict)+1, proj_name, 0, True]
            # Adding project to dictionary and project file
            dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
            with open(proj_file, "w") as f:
                json.dump(dict, f)
            # Showing that the project has been created
            print "Creating project",
            dotdotdot()
        if proj_option in "b":
            break
# Closing session
masthead(False)
print "You've completed %s pomodori today.\n" %j
if j > 0:
    # Pomodori summary from the log
    session_time = 0
    print "{:4}{:4}{:20}{:24}".format("##", "MM", "Project", "Task")
    print "-" * 39
    for row in log:
        minutes = row[3]/60
        log_summary = "{:02d}{:2}{:02d}{:2}{:20}{:24}".format(row[1], "", minutes, "", row[4][2], row[2])
        if row[0]:
            print colour.green + log_summary + colour.default
            session_time += row[3]
        else:
            print colour.grey + log_summary + colour.default
    # Total working time
    m, s = divmod(session_time, 60)
    h, m = divmod(m, 60)
    print "\nEffective working time: " + "{:d}:{:02d}:{:02d}".format(h, m, s)
##### To-do: What if I want to see a comprenhensive summary?
##### > Total time: XX hours (YY% personal; ZZ% work) -- green
##### > Time on active projects: XX hours on X projects -- default
##### > Longest active project: Book (XX hours) -- default
##### > Time on archived projects: XX hours on X projects -- grey
##### > Longest project ever: Pomothon (XX hours) -- grey
print "See you later!" + emoji.bye.decode("unicode-escape") + "\n"
