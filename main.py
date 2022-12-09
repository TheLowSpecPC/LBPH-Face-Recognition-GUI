from tkinter import *
import traning
import load_model_video
import sys
import os
import cv2
import shutil
import threading

root = Tk()
root.geometry("1000x600")
root.title("Face Recognition (Made By: The Low Spec PC)")
root.config(bg="gray")
cwd = os.getcwd()

def save():
    if l.get()==None or n.get()==None:
        os._exit(0)

    if os.path.exists(cwd + "/Info/"+l.get()+".txt"):
        os.remove(cwd + "/Info/"+l.get()+".txt")

    with open(cwd + "/Info/"+l.get()+".txt", "w") as a:
        a.write(n.get())
        a.close()

    cpt = 0

    directory = l.get()
    parent_dir = cwd+"/images"
    path = os.path.join(parent_dir, directory)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    vidStream=cv2.VideoCapture(0)
    while cpt<=1000:
        ret, frame=vidStream.read()
        cv2.imshow("test window", frame)
        cv2.imwrite(cwd+"/images/"+directory+"/image%04i.jpg" %cpt,frame)
        cpt +=1
        if cv2.waitKey(10)==ord('q'):
            break

def delete():
    if os.path.exists(cwd + "/Info/"+l1.get()+".txt"):
        os.remove(cwd + "/Info/"+l1.get()+".txt")
    if os.path.exists(cwd+"/images/"+l1.get()):
        shutil.rmtree(cwd+"/images/"+l1.get())

def train():
    print(traning.tran())

def start():
    print(load_model_video.str())

def exit():
    sys.exit(1)

Label(root, text="Image Upload", font=("Raleway", 20), bg="black", fg="white", height="1").place(x=150, y=1)

Label(root, text="Lable", font=("Raleway", 20), bg="black", fg="white", height="1").place(x=150, y=70)
l = Entry(root, width="10")
l.place(x=155, y=120)
l1 = Entry(root, width="10")
l1.place(x=155, y=150)

Label(root, text="Name", font=("Raleway", 20), bg="black", fg="white", height="1").place(x=250, y=70)
n = Entry(root, width="20")
n.place(x=225, y=120)
n1 = Entry(root, width="20")
n1.place(x=225, y=150)

Button(root,text="Save", command=threading.Thread(target=save).start, width="10", height="1").place(x=375, y=120)
Button(root,text="Delete", command=delete, width="10", height="1").place(x=375, y=150)

Button(root, text="Training Data Upload", command=threading.Thread(target=train).start, width="20", height="2").place(x=185, y=250)
Button(root, text="Start", command=threading.Thread(target=start).start, width="20", height="2").place(x=600, y=250)

root.wm_protocol("WM_DELETE_WINDOW", exit)

key=[]
value=[]

for i in os.listdir(cwd+"/Info"):
    key.append(int(i[:len(i)-4]))

for j in os.listdir(cwd+"/Info"):
    with open(cwd+"/Info/"+j, "r")as b:
        value.append(b.readline())
        b.close()

name = dict(zip(key,value))

cmd = Text(root, width="60", height="17")
cmd.place(x=10, y=300)
for i in range(len(key)):
    #i=int(i)
    cmd.insert(END, str(key[i]) +": "+ str(value[i]) + "\n")

root.mainloop()