#!/usr/bin/python
# Pomothon v2.51 -- r20200222
# by Pedro Arilla

import sys
import os
import json
import time
class emoji:
    tomato = "\U0001F345"
    clock = "\U000023F3"
    help = "\U0001F4A1"
    file = "\U0001F4C2"
    nap = "\U0001F4A4"
    bye = "\U0001F44B"
class colour:
    green = "\033[32m"
    red = "\033[031m"
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
pomothon = " POMOTHON " + colour.grey + "v2.51  " + colour.default

def checkFiles():
    # Checking that files exist and creating them if necessary
    if not os.path.exists("data"):
        os.makedirs("data")
        with open(os.path.join("data", "personal.json"), "wb") as temp_file:
            temp_file.write(json_default)
        with open(os.path.join("data", "work.json"), "wb") as temp_file:
            temp_file.write(json_default)
        with open(os.path.join("data", "archive.json"), "wb") as temp_file:
            temp_file.write("{}")

def masthead(escape):
    # App masthead and clean the screen
    os.system("cls" if os.name == "nt" else "clear")
    print "========================================"
    print "|           " + pomothon + "           |"
    print "========================================"
    if escape:
        print "\r"
    else:
        print "\a"

def pomodoro(i,j,log,project):
    # Pomodoro timer
    while True:
        pomodoro = raw_input("Start a pomodoro in this project (Y/N)? ").lower()
        if pomodoro in "n":
            masthead(True)
            break
        if pomodoro in "y":
            # Preparing
            task = raw_input("Task name: ")
            t = pomotime
            i += 1
            # Initiating
            masthead(True)
            print emoji.tomato.decode("unicode-escape") + " #%s:" %i + " " + task + " [" + project[2] + "]"
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
                why = raw_input("\n\nFinished or Aborted (F/A)? ").lower()
                if why in "f":
                    result = True
                if why in "a":
                    result = False
                pass
            # Adding to the log
            task_time = pomotime - t
            log.append([result,i,task,task_time,project])
            masthead(False)
            # Pomodoro summary
            if result:
                j += 1
                print emoji.tomato.decode("unicode-escape") + colour.green + " Pomodoro #%s completed!" %i + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]"
                print emoji.nap.decode("unicode-escape") + " Take a break no longer than 5 minutes.\n"
                # Adding to the dictionary
                project[3] = int(project[3]) + task_time
                dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
                # Dumping dictionary into project file
                with open(proj_file, "w") as f:
                    json.dump(dict, f)
            else:
                print emoji.tomato.decode("unicode-escape") + colour.red + " Pomodoro #%s not completed :(" %i + colour.default
                print emoji.file.decode("unicode-escape") + " " + task + " [" + project[2] + "]\n"
    return i, j, log, dict

def archive(dict, proj_sel):
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
    for dot in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(.3)
    return dict

checkFiles()
while True:
    masthead(True)
    # Selection menu
    proj_class = raw_input("(P)ersonal project\n(W)ork project\n(E)xit? ").lower()
    ##### To-do: What if I want to create a new type of project?
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
        ##### To-do: What if there are a lot of projects (+9)?
        print "{:3}{:7}{:20}".format("#", "HH:MM", "Project")
        print "-" * 40
        # Projects list
        x = 1
        while x <= len(dict):
            s = int(dict[str(x)]["time"])
            m, s = divmod(s, 60)
            h, m = divmod(m, 60)
            print "{:1}{:2}{:02d}:{:02d}{:2}{:20}".format(x, "", h, m, "", dict[str(x)]["name"])
            x += 1
        print "\a"
        # Selection menu
        ##### To-do: Add manual record
        proj_option = raw_input("(S)elect an existing project\n(A)rchive an existing project\n(C)reate a new project\n(B)ack? ").lower()
        # Select OR Archive
        if proj_option in "sa":
            print "\r"
            # Selecting a project
            while True:
                proj_sel = raw_input("Select a project (#): ")
                try:
                    int(proj_sel)
                except ValueError:
                    True
                else:
                    if int(proj_sel) <= len(dict):
                        if int(proj_sel) <= 0:
                            break
                        else:
                            # Working on project
                            if proj_option in "s":
                                project = [proj_class, proj_sel, dict[proj_sel]["name"], dict[proj_sel]["time"], False]
                                # Starting pomodoro
                                i, j, log, dict = pomodoro(i,j,log,project)
                                break
                            # Archiving project
                            if proj_option in "a":
                                dict = archive(dict, proj_sel)
                                break
        if proj_option in "c":
            # Creating project
            proj_name = raw_input("\nProject name: ")
            project = [proj_class, len(dict)+1, proj_name, 0, True]
            # Adding project to dictionary and project file
            dict[str(project[1])] = {"name": project[2], "time": str(project[3])}
            with open(proj_file, "w") as f:
                json.dump(dict, f)
            # Showing that the project has been created
            print "Creating project",
            for dot in range(5):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(.3)
            print "\n"
            # Starting pomodoro
            i, j, log, dict = pomodoro(i,j,log,project)
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
        ##### To-do: What if the string got diacritics?
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
print "See you later!" + emoji.bye.decode("unicode-escape") + "\n"
