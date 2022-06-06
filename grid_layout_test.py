from tkinter import *
import math
from PIL import Image, ImageTk

window = Tk()
window.title("Joedle")
window.geometry("500x700")
window.configure(background="white")
info_image = Image.open("info.png")
info_image = info_image.resize((50, 50))
info_image2= info_image.resize((200, 10))
info_image = ImageTk.PhotoImage(info_image)
info_image2 = ImageTk.PhotoImage(info_image2)
blank = PhotoImage()


def grid():
    x = 6
    z = 5
    for i in range(x * z):
        b = Label(letters, width=20, height=20, image=blank, font=("Noto Sans SemiBold", 45), text=str(i)[0],
                  compound='c')
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
topic = Frame(window, bg="yellow")
letters = Frame(window, bg="pink")
keyboard = Frame(window, bg="orange")

information.grid(row=0, column=0, sticky="nsew")
title.grid(row=0, column=1, sticky="nsew")
timer.grid(row=0, column=2, sticky="nsew")
topic.grid(row=1, column=1, sticky="nsew")
letters.grid(row=2, column=0, columnspan=3, sticky="nsew")
keyboard.grid(row=3, column=0, columnspan=3, sticky="nsew")

infobutton = Button(information, image=info_image, width=10,height=10,compound="c", relief="flat", borderwidth=0)
infobutton.pack(side=LEFT, expand=True, fill='both')


grid()
mainloop()
