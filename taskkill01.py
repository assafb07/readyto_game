import subprocess
import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox

answer01 = subprocess.run(["tasklist"], capture_output=True)
global tasklist
tasklist = answer01.stdout.decode()

def task_list():
    found_it = ""
    proccess_to_kill = task_name.get()
    if proccess_to_kill == "":
        answer = "Enter proccess name to kill"
        insert_answer(answer, 1)
    print(proccess_to_kill)
    answer01 = subprocess.run(["tasklist"], capture_output=True)
    with open("tasks.txt", "w") as file:
        file.write(answer01.stdout.decode())

    with open("tasks.txt", "r") as file:
        for line in file:
            if proccess_to_kill.lower() in line and proccess_to_kill != "":
                proccess_number = re.findall(r"\d+", line)
                try:
                    answer = f"found it [{proccess_number[0]}]"
                    insert_answer(answer, 1)
                    task_kill(proccess_number, proccess_to_kill)
                    found_it = "yes"
                except: load_frame()
            else:
                continue
        if found_it != "yes":
            answer = "Didn't found proccess by that name"
            insert_answer(answer, 1)



def show_list():
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
        for i in names:
            count[i] = count.get(i, 0) + 1
        print (count)
        for key,value in count.items():
            if value > 1:
                continue
            else:
                insert_answer(key, 0)


def task_kill(proccess_number, proccess_to_kill):
    kill = subprocess.run(["taskkill", "/PID", proccess_number[0]], capture_output=True)
    answer = "kill command was sent"

    insert_answer(answer, 1)
    is_it_dead(proccess_number, proccess_to_kill)


def is_it_dead(proccess_number, proccess_to_kill):
    answer = "checking if proccess is dead"
    insert_answer(answer, 1)
    answer01 = subprocess.run(["tasklist"], capture_output=True)
    with open("tasks.txt", "w") as file:
        file.write(answer01.stdout.decode())
    with open("tasks.txt", "r") as file:
        for line in file:
            if proccess_to_kill.lower() in line:
                answer = "proccess still running\n need to Force it"
                insert_answer(answer, 1)
                force(proccess_number, proccess_to_kill)
            else: continue
        answer = "proccess is dead"
        insert_answer(answer, 1)
        load_frame()


def force(proccess_number, proccess_to_kill):
    answer = "Force kill territory\n You can Force Kill the proccess"
    insert_answer(answer, 1)
    answer = messagebox.askquestion("Proccess nedd FORCE KILL", "Are you sure?")

    if answer == "yes":
        print (proccess_number[0])
        kill = subprocess.run(["taskkill", "/PID", proccess_number[0], "/F"], capture_output=True)
        insert_answer("OK, it is dead", 1)
    elif answer == "no":
        answer = "As you wish. Proccess is running"
        insert_answer(answer, 1)

def what_to__kill():
    proccess_to_kill = input("Name the proccess you wand to kill\n or \"List\" for proccess list: ")
    task_list()

def insert_answer(answer, x):
    print (x)
    if x == 1:
        text_box.delete("1.0", END)

    text_box.insert("1.0", f"{answer}\n")
    text_box.tag_add("left", "1.0", "end")
    text_box.grid(row=5,column=1, columnspan=2)


def load_frame():
    label01 = Label(root, text='         Task Killer :-|      ')
    label01.grid(row=0, columnspan=2)
    global task_name
    task_name = tk.StringVar()
    ip_2 = tk.StringVar()
    ip1 = Entry(root, textvariable = task_name).grid(row=1,column=1)
    point1 = Label(root, text="Task Name").grid(row=1,column=0)
    ip2 = Entry(root, textvariable = ip_2).grid(row=2,column=1)
    point2 = Label(root, text = "Return").grid(row=2,column=0)

    bt10 = Button(root,text="Kill It!!", command=lambda:task_list())
    bt10.grid(row=3,column=1)
    bt11 = Button(root,text="Tasts List", command=lambda:show_list())
    bt11.grid(row=3,column=2)


root = Tk()
root.title("Kill Windlows Tasks")
root.geometry('507x250+350+50')
text_box = Text(root, height=20, width=50)
text_box.insert(1.0, f'\ncoded by abmail07@gmail.com')
text_box.tag_add("left", 1.0, "end")
text_box.grid(row=5,column=1, columnspan=2)

load_frame()
root.mainloop()
