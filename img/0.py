#!/usr/bin/python3

import tkinter as tk
from PIL import ImageTk, Image

#This creates the main window of an application
window = tk.Tk()
window.title("Join")
window.geometry("300x300")
window.configure(background='grey')
img = ImageTk.PhotoImage(Image.open('bar.png'))
panel = tk.Label(window, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

def Laduj(self):
    path = "0.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    panel.configure(image=img)
    panel.image=img

window.bind("<Return>", Laduj)
window.mainloop()
