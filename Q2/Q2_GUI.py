"""
Parth Krishna Sharma : 2017B3A70907H
Siddhi Burse : 2017B3A70972H
Piyush Phatak : 2017B3A70425H
Keshav Pandya : 2017A3PS0399H
"""

from tkinter import *
from tkinter import messagebox as mb 
import json
import subprocess

def fill_states():
    Wb_red.delete(0.0,END)
    Wb_red.insert(END,w_red)
    Wb_blue.delete(0.0,END)
    Wb_blue.insert(END,w_blue)
    Wb_green.delete(0.0,END)
    Wb_green.insert(END,w_green)
    Eb_red.delete(0.0,END)
    Eb_red.insert(END,e_red)
    Eb_blue.delete(0.0,END)
    Eb_blue.insert(END,e_blue)
    Eb_green.delete(0.0,END)
    Eb_green.insert(END,e_green)
    return

def state_change(temp):
    global w_red,w_blue,w_green,e_red,e_blue,e_green
    #print(temp,len(temp))
    if(ind%2==0):
        if(temp[3]=="Red"):
            w_red-=1
            e_red+=1
        elif(temp[3]=="Blue"):
            w_blue-=1
            e_blue+=1
        elif(temp[3]=="Green"):
            w_green-=1
            e_green+=1
        if(temp[4]=="Red"):
            w_red-=1
            e_red+=1
        elif(temp[4]=="Blue"):
            w_blue-=1
            e_blue+=1
        elif(temp[4]=="Green"):
            w_green-=1
            e_green+=1
    else:
        if(temp[3]=="Red"):
            w_red+=1
            e_red-=1
        elif(temp[3]=="Blue"):
            w_blue+=1
            e_blue-=1
        elif(temp[3]=="Green"):
            w_green+=1
            e_green-=1
    fill_states()
    return

def output_ans(x,ind,size):
    if(size==1):
        move.delete(0.0,END)
        move.insert(END,"No Moves Possible!!")
        return
    if(ind==size-1):
        move.delete(0.0,END)
        move.insert(END,"Game over! Success!!")
        final_ans.delete(0.0,END)
        final_ans.insert(END,ind)
        return
    if(ind>size-1):
        move.delete(0.0,END)
        move.insert(END,"Press 'PLAY' to start new game OR Press 'STOP' to end")
        return
    move.delete(0.0,END)
    move.insert(END,x[ind])
    move_num.delete(0.0,END)
    move_num.insert(END,ind+1)
    temp = x[ind].split(' ')
    state_change(temp)
    return

def click():
    s_red=e1.get()
    s_blue=e2.get()
    s_green=e3.get()
    final_ans.delete(0.0,END)
    move.delete(0.0,END)
    move_num.delete(0.0,END)
    global x
    x,y = subprocess.Popen(["/home/siddhi/Documents/4-2/AI/Assignment_1/Q2/AI_Q2.exe "+s_red+" "+s_blue+" "+s_green] , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    x = x.decode()
    x = x.split('\n')
    global ind
    ind = 0
    global size
    size=len(x)
    global w_red,w_blue,w_green,e_red,e_blue,e_green
    w_red = int(s_red)
    w_blue = int(s_blue)
    w_green = int(s_green)
    e_red,e_blue,e_green=0,0,0
    fill_states()

def click_next():
    global ind 
    output_ans(x,ind,size)
    ind+=1
    return
    
master = Tk()
master.geometry("900x550")
backgrnd_colr = "lemon chiffon"
master.configure(background=backgrnd_colr)
master.title('Soldier River Crossing Puzzle')

#label
Label (master,text="Enter number of soldiers on West bank:",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=40,y=50)
Label (master,text="Red",bg=backgrnd_colr,fg="red",font="none 13 bold").place(x=510,y=25)
Label (master,text="Blue",bg=backgrnd_colr,fg="blue",font="none 13 bold").place(x=510,y=50)
Label (master,text="Green",bg=backgrnd_colr,fg="green",font="none 13 bold").place(x=510,y=75)

Label (master,text="West Bank",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=200,y=150)
Label (master,text="Red",bg=backgrnd_colr,fg="red",font="none 13 bold").place(x=170,y=190)
Label (master,text="Blue",bg=backgrnd_colr,fg="blue",font="none 13 bold").place(x=170,y=220)
Label (master,text="Green",bg=backgrnd_colr,fg="green",font="none 13 bold").place(x=170,y=250)

Label (master,text="East Bank",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=600,y=150)
Label (master,text="Red",bg=backgrnd_colr,fg="red",font="none 13 bold").place(x=570,y=190)
Label (master,text="Blue",bg=backgrnd_colr,fg="blue",font="none 13 bold").place(x=570,y=220)
Label (master,text="Green",bg=backgrnd_colr,fg="green",font="none 13 bold").place(x=570,y=250)

Label (master,text="Move soldiers:",bg=backgrnd_colr,fg="black",font="none 13 bold").place(x=100,y=330)
Label (master,text="Move number :",bg=backgrnd_colr,fg="black",font="none 13 bold").place(x=100,y=380)
Label (master,text="Minimum number of moves needed:",bg=backgrnd_colr,fg="black",font="none 13 bold").place(x=100,y=430)

#Text Entry
e1 = Entry(master,font="none 13 bold",width=5)
e1.place(x=575,y=25)
e2 = Entry(master,font="none 13 bold",width=5)
e2.place(x=575,y=50)
e3 = Entry(master,font="none 13 bold",width=5)
e3.place(x=575,y=75)

#Button
bttn_clr = "tan1"
Button (master,text="PLAY",bg=bttn_clr,fg="black",font="none 13 bold",width=10,height=1,command=click).place(x=700,y=40)
Button (master,text="NEXT",bg=bttn_clr,fg="black",font="none 13 bold",width=10,height=1,command=click_next).place(x=400,y=480)
Button (master,text="STOP",bg=bttn_clr,fg="black",font="none 13 bold",width=10,height=1,command=master.destroy).place(x=720,y=470)

#Textbox
Wb_red = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Wb_red.place(x=240,y=190)
Wb_blue = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Wb_blue.place(x=240,y=220)
Wb_green = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Wb_green.place(x=240,y=250)

Eb_red = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Eb_red.place(x=660,y=190)
Eb_blue = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Eb_blue.place(x=660,y=220)
Eb_green = Text (master,fg="black",font="none 13 bold",width=4,height=1)
Eb_green.place(x=660,y=250)

move = Text (master,fg="black",font="none 13 bold",width=50,height=2)
move.place(x=270,y=320)
move_num = Text (master,fg="black",font="none 13 bold",width=7,height=1)
move_num.place(x=270,y=380)
final_ans = Text(master,fg="black",font="none 13 bold",width=7,height=1)
final_ans.place(x=460,y=430)

mainloop()
