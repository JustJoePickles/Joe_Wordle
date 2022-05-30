from tkinter import *
import math

window1 = Tk()
window1.title("Joedle")
window1.geometry("400x600")
window1.configure(background="#c7cdd6")

screen = Entry(window1, font=("Arial", 20))
screen.grid(row=0, column=0, columnspan=3)
test_button = Button(text="Reload", command=lambda testing=1: grid())
test_button.grid(row=1, column=0)
canvas = Frame(height=200,width=100)
canvas.grid(row=2, column=0)
def grid():
    for widgets in canvas.winfo_children():
        widgets.destroy()
    x = int(screen.get())
    for i in range(x * 5):
        b = Button(canvas, width=8, height=2)
        b.grid(row=math.floor(i / x) + 1, column=i % x, sticky="nsew", padx=4, pady=4)

    for i in range(x):
        window1.columnconfigure(i, weight=1)
    for i in range(x):
        window1.rowconfigure(i, weight=1)


mainloop()
