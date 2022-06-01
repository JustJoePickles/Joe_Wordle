from tkinter import *
import math
window1 = Tk()
window1.title("Joedle")
window1.geometry("400x600")
window1.configure(background="white")

information=Frame(bg="blue")
title=Frame(bg="red")
timer=Frame(bg="green")
information.grid(row=0, column=0)
title.grid(row=0, column=1)
timer.grid(row=0, column=2)
topic=Frame(bg="yellow")
topic.grid(row=1,column=1)

mainloop()