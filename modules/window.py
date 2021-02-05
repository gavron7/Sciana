#!/usr/bin/python3

import tkinter as tk
import time
import requests, io
import funkcje as funkcje
from PIL import Image, ImageTk

class Startup():
    def __init__(self):
        self.startupscreen = tk.Tk()
        self.startupscreen.title('Ściana')
        self.startupscreen.configure(background='black')
        self.welcometext = tk.Label(self.startupscreen, font = ('caviar dreams', 40), bg='black', fg='white')
        self.welcometext.config(text='Uruchamianie...')
        self.welcometext.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.logtext = tk.Label(self.startupscreen, font=('caviar dreams',8), bg='black', fg='black')
        self.logtext.config(text='')
        self.logtext.pack(side=tk.BOTTOM, padx=(10,10))
        self.windowWidth = self.startupscreen.winfo_reqwidth()
        self.windowHeight = self.startupscreen.winfo_reqheight()
        self.positionRight = int(self.startupscreen.winfo_screenwidth()/2 - self.windowWidth)
        self.positionDown = int(self.startupscreen.winfo_screenheight()/2 - self.windowHeight/2)
        self.startupscreen.attributes("-fullscreen", True)
        self.startupscreen.update()

class Sciana():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('ŚCIANA')
        self.root.withdraw()
        self.root.attributes("-fullscreen", True)
        self.root.configure(background='black')

        self.f_logs = tk.Label(self.root, borderwidth=0, font = ('URW Chancery L', 10), bg='black', fg='grey')
        self.f_logs.pack(anchor=tk.N, side=tk.TOP)

        self.f_gora=tk.Label(self.root, borderwidth=0)
        self.f_gora.pack(anchor=tk.N, fill=tk.BOTH, expand = tk.TRUE)

        self.f_lewa=tk.Label(self.f_gora)
        self.f_lewa.pack(anchor=tk.SW, side=tk.LEFT, fill = tk.BOTH)
        self.f_lewa.configure(background='black')

        self.f_srodek=tk.Label(self.f_gora)
        self.f_srodek.pack(anchor=tk.SW,side=tk.LEFT, fill = tk.BOTH, expand=tk.TRUE)
        self.f_srodek.configure(background='black')

        self.f_prawa=tk.Label(self.f_gora)
        self.f_prawa.pack(anchor=tk.SW, side=tk.LEFT, fill = tk.BOTH)
        self.f_prawa.configure(background='black')

        self.newstitle = tk.Label(self.root, borderwidth=0, font = ('URW Chancery L', 18), bg='black', fg='grey')
        self.newstitle.pack()

        self.masterclock = tk.Label(self.f_lewa)
        self.masterclock.pack(anchor=tk.NW, padx=45)
        self.masterclock.configure(background='black')

        self.date_frame = tk.Label(self.masterclock, font = ('Gentium Basic', 14), bg='black', fg='white')
        self.date_frame.pack(side=tk.TOP, anchor = tk.W)
        self.clock_frame = tk.Label(self.masterclock, font = ('Gentium Basic', 70), bg='black', fg='white')
        self.clock_frame.pack(side=tk.LEFT, anchor = tk.W)
        self.clock_frame2 = tk.Label(self.masterclock, font = ('Gentium Basic', 20), bg='black', fg='grey')
        self.clock_frame2.pack(side=tk.LEFT, anchor = tk.N, ipady=15)

        self.calendar_frame = tk.Label(self.f_lewa, font = ('FreeMono', 13), bg='black', fg='grey')
        self.calendar_frame.pack(anchor=tk.N, padx=45, pady=20)

        self.w_img = tk.Label(self.f_prawa, bg='black', image='')
        self.w_img.pack(anchor=tk.N, fill=tk.Y, padx=(0,45))

        self.energia = tk.Label(self.f_srodek, font =('FreeMono',25), bg='black')
        self.energia.pack(side=tk.TOP, anchor = tk.N)
        self.inne = tk.Label(self.f_srodek, bg='black', fg='yellow')
        self.inne.pack(side=tk.TOP, anchor = tk.N)
        self.info = tk.Label(self.f_srodek, bg='black', fg='grey')
        self.info.pack(side=tk.BOTTOM, anchor = tk.N)

    def kalendarz(self):
        self.img_data1 = requests.get('http://localhost/img/cal.php').content
        self.img1 = ImageTk.PhotoImage(Image.open(io.BytesIO(self.img_data1)), master=self.root)
        self.calendar_frame.config(image=self.img1)

    def getweather(self):
        self.img_data = requests.get('http://localhost/img/0.php').content
        self.img = ImageTk.PhotoImage(Image.open(io.BytesIO(self.img_data)), master=self.root)
        self.w_img.config(image=self.img)

