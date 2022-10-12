import subprocess
import re
import json
import sys
import os
import win32com.shell.shell as shell
import time
import threading



def admin_pre():
    ASADMIN = 'asadmin'

    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

def find_pid(proccess_name):

    proccess_many = []
    found_it = ""
    with open("tasks.txt", "r") as file:
        for line in file:
            if proccess_name.lower() in line and proccess_name != "":
                proccess_number = re.findall(r"\d+", line)
                try:
                    #print(f"found it [{proccess_number[0]}]")
                    found_it = "yes"
                    proccess_many.append(proccess_number[0])

                except:
                    found_it = "no"
            else:
                continue
        if found_it == "yes":
            print(proccess_many)
            return proccess_many
        else:
            return None

def make_list():
    answer01 = subprocess.run(["tasklist"], capture_output=True)
    with open("tasks.txt", "w") as file:
        file.write(answer01.stdout.decode())


def show_list():
    print("The list")
    names = []
    with open("tasks.txt", "r") as file:
        for line in file:
            if line == "\n":
                continue
            task_name = line.split()
            names.append(task_name[0])
# print only one time proccesses that
# apear multiple time in task list
        count = {}
        key_list = []
        for i in names:
            count[i] = count.get(i, 0) + 1
        for key,value in count.items():
            if value > 1:
                continue
            else:
                key_list.append(key)

        for name in sorted(key_list):
            print(name)


def kill_proccess(proccess_number):
    print (proccess_number)
    kill = subprocess.run(["taskkill", "/PID", proccess_number], capture_output=True)
    answer = "kill command was sent"

def is_it_dead(proccess_pid):
    make_list()
    found = []
    with open("tasks.txt", "r") as file:
        for line in file:
            if proccess_pid.lower() in line:
                found.append(1)
            else:
                pass
        if found == []:

            return "DEAD"
        else:
            print("Still running")
            return "still running"

def force(proccess_number):
    print ("Force Kill", proccess_number)
    kill = subprocess.run(["taskkill", "/PID", proccess_number[0], "/F"], capture_output=True)
    print("Force kill sent")

def kill_this(pid_to_kill):
    try:
        for pid in pid_to_kill:
            print (pid)
            kill_proccess(pid)
    except:
        print("oops")


def execute_list(proccess_name):

#    show_list()
#    for name in proccesses_list:
    pid_to_kill = find_pid(proccess_name)
    print(pid_to_kill)
#    if pid_to_kill != None:
#        kill_this(pid_to_kill)
#        if (is_it_dead(proccess_name)) == "still running":
#            force(pid_to_kill[0])
#        else:
#            print ("NOT FOUND")

def proccess_instr(proccess):

    to_run = []
    strip01 = proccess.lstrip("game = open : ")
    strip02 = strip01.lstrip("game = close : ")
    strip03 = strip02.rstrip("\n")

    to_run = strip03.split("|")
    print (to_run)
    return to_run



def run_threads(val01):
    thread = threading.Thread(target = run_this, args=(val01,))
    thread.start()

def run_task(run_this01):
    for item in run_this01:
        item02 = item.lstrip()
        run_threads(item02)

def kill_task(kill_this01):
    print ("Kill")
    make_list()
    for item in kill_this01:
        item01 = item.lstrip()
        item02 = item01.rstrip()
        print(item02)
        pid_to_kill = find_pid(item02)
        print (pid_to_kill)
        print(kill_this(pid_to_kill))
        if (is_it_dead(item02)) == "still running":
            force(pid_to_kill)
            print(item, "is", is_it_dead(item02))
        else: print (item, "is", is_it_dead(item02))

def run_this(item02):
    print(item02)
    try:
        answer01 = subprocess.run(item02, capture_output=True)
        print(answer01.stdout.decode())
        return "Done"
    except OSError:
        "need administraor previsions"

def instractions():
    print ("Go!")
    items_list = []
    with open("actions01.txt", "r") as f:
        data = f.readlines()
        for line in data:

#            if "start" in line and "open" in line:
#                run_task(line)
#            elif "start" in line and "close" in line:
#                print (line)
#                execute_list(line[2:])
            if "game" in line and "close" in line:
                print("close")
                kill_this01 = proccess_instr(line)
                kill_task(kill_this01)
            elif "game" in line and "open" in line:
                print("open")
                run_this01 = proccess_instr(line)
                run_task(run_this01)




try:
    admin_pre()
except:
    "OK"
make_list()

instractions()
