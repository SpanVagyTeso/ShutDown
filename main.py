import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading
import time
import os
import datetime
import ctypes
import platform

class add_popup:
    def __init__(self,master,exac,timer,super_master):
        self.master=master
        self.check=False
        self.exac=exac
        self.timer=timer
        self.super=super_master

        self.label= Label(master,text="P")
        self.button = Button(master,text="Btn",command=self.btn)
        self.checkbutton = Checkbutton(master,text="Timer/Exac(off/on)",command=self.c)
        self.entry= Entry(master,width=10)
        self.label.grid()
        self.entry.grid()
        self.checkbutton.grid()
        self.button.grid()

    def c(self):
        if self.check:
            self.check=False
        else:
            self.check=True67

    def btn(self):
        if self.check:
            a=self.entry.get().split(" ")
            good = True
            for time in self.exac:
                if time == a:
                    good = False
            if good:
                self.exac.append(a)
                f=open("config.txt","a+")
                f.write("0\n")
                b=""
                for l in a:
                    b+=l+" "
                f.write(b+"\n")
                self.super.exac_values_change()
        else:
            a=self.entry.get()
            good = True
            for time in self.timer:
                if time == a:
                    good = False
            if good:
                self.timer.append(a)
                f=open('config.txt',"a+")
                f.write("1\n")
                f.write(a+"\n")
                self.super.timer_values_change()

        print(self.check)
        self.master.destroy()

class del_popup:
    def __init__(self,master,super_master):
        self.super=super_master
        self.master=master
        self.check=False

        self.label = Label(master,text="Mentett idő törlése")
        self.label.grid(row=0)
        self.checkButton = Checkbutton(master, text="Timer/Exac(off/on)",command=self.change)
        self.checkButton.grid(row=1)
        self.listBox= ttk.Combobox(master,values=self.super.saved_timer_values)
        self.listBox.grid(row=2)
        self.button= Button(master,text="Delete",command=self.delete)
        self.button.grid(row=3)

    def file_del(self, item):
        f=open("config.txt","r")
        lines=f.readlines()
        f.close()
        f= open("config.txt","w")
        print(item)
        print(len(lines))
        i=0
        while i<len(lines)-1:
            if lines[i+1].replace("\n","") == item:
                print("a")
                i+=2
            else:
                f.write(lines[i])
                f.write(lines[i+1])
                i+=2
        f.close()

    def delete(self):
        if self.check:
            a=self.listBox.get().split(" ")
            self.super.saved_exac_values.remove(a)
            self.super.exac_values_change()
            self.file_del(a)
        else:
            a=self.listBox.get()
            print(self.listBox.get())
            self.super.saved_timer_values.remove(a)
            self.super.timer_values_change()
            self.file_del(a)
        self.master.destroy()


    def change(self):
        if self.check:
            self.check=False
            self.listBox['values']=self.super.saved_timer_values
            self.listBox.current(0)
        else:
            self.check=True
            self.listBox['values']=self.super.saved_exac_values
            self.listBox.current(0)

class GUI:
    def __init__(self, master):
        self.hour_value = IntVar()
        self.min_value = IntVar()
        self.sec_value = IntVar()
        self.alma = IntVar()
        self.alma.trace('w', lambda *_: self.change())
        self.saved_timer_values = []
        self.saved_exac_values = []
        self.saved_timer_value = IntVar()
        self.saved_exac_value = StringVar()
        self.saved_timer_value.trace('w', lambda *_: self.timer_change())
        self.saved_exac_value.trace('w', lambda *_: self.exac_change())
        #self.mode=StringVar()


        f=open("config.txt","r").readlines()
        i=0
        while i < len(f):
            if f[i]=="1\n":
                i+=1
                self.saved_timer_values.append(f[i].replace("\n",""))
                print("Timer "+f[i])
            if f[i]=="0\n":
                i+=1
                curr = f[i].replace("\n","").split(" ")
                self.saved_exac_values.append(curr)
                print("Exac ",end="")
                print(curr)
            i+=1

        self.master = master
        master.title("ShutDown")

        self.checkButton = Checkbutton(master,
                                       text="Timer",
                                       variable=self.alma)
        self.checkButton.grid(row=0, column=0)

        self.variable = StringVar(master)
        self.variable.set("one")

        hour_values = [i for i in range (24)]

        self.listBox_hour = ttk.Combobox(master, textvariable=self.hour_value,
                                         values=hour_values,
                                         width=3)
        self.listBox_hour.grid(row=3, column=0)
        self.label_hour = Label(master, text="Óra")
        self.label_hour.grid(row=2, column=0)

        min_values = [i for i in range(60)]

        self.listBox_min = ttk.Combobox(master, textvariable=self.min_value,
                                        values=min_values,
                                        width=3)
        self.listBox_min.grid(row=3, column=1)
        self.label_min = Label(master, text="Perc")
        self.label_min.grid(row=2, column=1)

        sec_values = [i for i in range(60)]

        self.listBox_sec = ttk.Combobox(master, textvariable=self.sec_value,
                                        values=sec_values,
                                        width=3)
        self.listBox_sec.grid(row=3, column=2)
        self.label_sec = Label(master, text="Másodperc")
        self.label_sec.grid(row=2, column=2)

        self.button_exactime = Button(master,text="ShutDown", command=self.exacShutdown)
        self.button_exactime.grid(row=4, column=1)

        self.entry_timer = Entry(master,width=15)
        self.entry_timer.grid(row=2,column=0)
        self.entry_timer.grid_remove()

        self.button_timer = Button(master,text="Shutdown",command=self.timerShutdown)
        self.button_timer.grid(row=3,column=0)
        self.button_timer.grid_remove()

        self.button_stop = Button(master,command=self.stopShutdown,
                                 text="Stop Shutdown")
        self.button_stop.grid(row=5, columnspan=2,sticky=W)

        self.label_timer = Label(master,text="")
        self.label_timer.grid(row=6,column=0)

        self.listBox_saved_timer= ttk.Combobox(master,
                                              values=self.saved_timer_values,width=3,
                                              textvariable=self.saved_timer_value)
        self.listBox_saved_timer.grid(column=3,row=0)
        self.listBox_saved_timer.grid_remove()

        self.listBox_saved_exac= ttk.Combobox(master,
                                              values= self.saved_exac_values,width=5,
                                              textvariable=self.saved_exac_value)
        self.listBox_saved_exac.grid(column=6,row=3)

        self.label_saved_exac= Label(master,text="Mentett idők")
        self.label_saved_exac.grid(column=6,row=2)

        self.button_add_time = Button(master,command=self.def_add_popup,text="Add")
        self.button_add_time.grid(row=5,column=7,sticky=W)

        self.button_del_time= Button(master,text="Del",command=self.def_del_popup)
        self.button_del_time.grid(row=6,column=7,sticky=W)

    #    self.listBox_mode= ttk.Combobox(master,values=["shutdown","screen save"],
    #                                    textvariable=self.mode)
    #    self.listBox_mode.grid (row=6,column=1)

    class timer_label(threading.Thread):
        def __init__(self,label,tar):
            super().__init__()
            self.tar=tar
            self.active=True
            self.label=label

        def stop(self):
            self.active=False

        def run(self):
            self.label.grid()
            while self.active and self.tar>= 0:
                self.tar-=1
                date = datetime.time(int(self.tar/3600),int(self.tar/60%60),int(self.tar%60))
                self.label['text']=date
                time.sleep(1)
            self.label.grid_remove()

    def exac_values_change(self):
        self.listBox_saved_exac['values']=self.saved_exac_values

    def timer_values_change(self):
        self.listBox_saved_timer['values']=self.saved_timer_values

    def def_del_popup(self):
        base=Tk()
        pop=del_popup(base,self)
        base.mainloop()

    def def_add_popup(self):
        base=Tk()
        pop=add_popup(base,self.saved_exac_values,self.saved_timer_values,self)
        print(self.saved_timer_values)
        print("")
        base.mainloop()

    def hideExacThings(self):
        self.listBox_hour.grid_remove()
        self.listBox_min.grid_remove()
        self.listBox_sec.grid_remove()
        self.label_hour.grid_remove()
        self.label_min.grid_remove()
        self.label_sec.grid_remove()
        self.button_exactime.grid_remove()
        self.listBox_saved_exac.grid_remove()
        self.label_saved_exac.grid_remove()

    def showExacThings(self):
        self.listBox_hour.grid()
        self.listBox_min.grid()
        self.listBox_sec.grid()
        self.label_hour.grid()
        self.label_min.grid()
        self.label_sec.grid()
        self.button_exactime.grid()
        self.listBox_saved_exac.grid()
        self.label_saved_exac.grid()

    def hideTimerThings(self):
        self.entry_timer.grid_remove()
        self.button_timer.grid_remove()
        self.listBox_saved_timer.grid_remove()

    def showTimerThings(self):
        self.entry_timer.grid()
        self.button_timer.grid()
        self.listBox_saved_timer.grid()

    def exac_change(self):
        a=self.saved_exac_value.get().split(" ")
        self.listBox_hour.current(a[0])
        self.listBox_min.current(a[1])
        self.listBox_sec.current(a[2])

    def timer_change(self):
        self.entry_timer.delete(0,END)
        self.entry_timer.insert(0,self.saved_timer_value.get())
        print(self.saved_timer_value.get())

    def change(self):
        if self.alma.get() == 1:
            self.checkButton['text'] = "Pontos idő"
            self.hideExacThings()
            self.showTimerThings()
        else:
            self.checkButton['text'] = "Timer"
            self.hideTimerThings()
            self.showExacThings()

    def timerShutdown(self):
        seconds = int(self.entry_timer.get())*60
        self.shutDown(seconds)

    def stopShutdown(self):
        self.timer.cancel()
        self.timer_label.stop()
        del self.timer_label
        print("Done")

    def shutDown(self, seconds):
        def sd():
            # ctypes.windll.user32.LockWorkStation()
            os.system('shutdown -s')
        print(seconds)
        self.timer_label = self.timer_label(self.label_timer,seconds)
        self.timer = threading.Timer(seconds, sd)
        self.timer_label.start()
        self.timer.start()

    def exacShutdown(self):
        hour = (self.hour_value.get())
        min = (self.min_value.get())
        sec = (self.sec_value.get())
        current_time = datetime.datetime.now()
        current_seconds = current_time.second + current_time.minute*60 + current_time.hour * 3600
        asked_seconds = sec + min*60 + hour * 3600

        if asked_seconds <= current_seconds:
            asked_seconds += 24*3600

        self.shutDown(asked_seconds-current_seconds)

if platform.system() == "Windows":
    root = Tk()
    root.geometry("350x250")
    root.resizable(0, 0)

    my_gui = GUI(root)
    root.mainloop()
else:
    print("Ez az alkalmazás csak windowsra érhető el jelenleg :sadface:")
