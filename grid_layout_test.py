from tkinter import *
import math
window = Tk()
window.title("Joedle")
window.geometry("600x400")
window.configure(background="white")
# window.resizable(0,0)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=4)
window.columnconfigure(2, weight=1)

window.rowconfigure(0,weight=1)
window.rowconfigure(1,weight=1)
window.rowconfigure(2,weight=8)
window.rowconfigure(3,weight=2)

information=Label(window, bg="blue")

title=Label(window, bg="red", text="Title")
timer=Label(window, bg="green", text="T")
information.grid(row=0, column=0, sticky="nsew")
information.grid_propagate(False)
topic=Label(window, bg="yellow", text="Topic")
letters=Label(window, bg="pink", text="Letter grid")
letters.grid(row=2, column=0, columnspan=3, sticky="nsew")
title.grid(row=0, column=1, sticky="nsew")
timer.grid(row=0, column=2, sticky="nsew")
topic.grid(row=1,column=1, sticky="nsew")
keyboard=Label(window, bg="orange", text="Keyboard")
keyboard.grid(row=3,column=0, columnspan=3, sticky="nsew")

mainloop()