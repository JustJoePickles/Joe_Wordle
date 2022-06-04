from tkinter import *
import math

window = Tk()
window.title("Joedle")
window.geometry("500x700")
window.configure(background="white")

blank = PhotoImage()

def grid():
    x = 5
    z = 5
    for i in range(x * z):
        b = Label(letters, width=20, height=20, image=blank, font=("Noto Sans SemiBold", 45), text=str(i)[0], compound='c')
        b.grid(row=math.floor(i / x), column=i % x, sticky="nsew", padx=1, pady=1)
    for i in range(x):
        letters.columnconfigure(i, weight=1)
    for i in range(x + (z - x)):
        letters.rowconfigure(i, weight=1)


window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=8)
window.columnconfigure(2, weight=1)

window.rowconfigure(0, weight=2)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=5)
window.rowconfigure(3, weight=4)

information = Frame(window, bg="blue")
title = Frame(window, bg="red")
timer = Frame(window, bg="green")
information.grid(row=0, column=0, sticky="nsew")
topic = Frame(window, bg="yellow")
letters = Frame(window, bg="pink")
letters.grid(row=2, column=0, columnspan=3, sticky="nsew")
title.grid(row=0, column=1, sticky="nsew")
timer.grid(row=0, column=2, sticky="nsew")
topic.grid(row=1, column=1, sticky="nsew")
keyboard = Frame(window, bg="orange")
keyboard.grid(row=3, column=0, columnspan=3, sticky="nsew")

grid()
mainloop()
