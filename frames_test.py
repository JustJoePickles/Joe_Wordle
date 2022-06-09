from tkinter import *
import math
import time
import random

class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.root.title("Joedle")
        self.root.geometry("500x700")
        self.root.configure(background="white")
        self.homepage=HomePage(self)
        self.overlay=Overlay(self)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.mainloop()



# class FrameManager():
#     def __init__(self):

class Overlay():
    def __init__(self,root):
        self.window = Frame(root.root, bg="pink", width=0, height=0)
        self.window.grid(row=0,column=0, sticky="nsew", padx=40, pady=15)
        self.change(root)
    def change(self,root):
        number=random.randint(1,2)
        if number==1:
            root.homepage.window.tkraise()
        if number==2:
            self.window.tkraise()
        self.window.after(100, self.change(root))

class HomePage():
    def __init__(self, root):
        self.blank = PhotoImage()
        self.window=Frame(root.root, bg="red", width=0, height=0)
        self.window.grid(row=0,column=0, sticky="nsew")
        # self.window.pack(side=LEFT, expand=True, fill='both')
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=8)
        self.window.columnconfigure(2, weight=1)

        self.window.rowconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=5)
        self.window.rowconfigure(3, weight=4)

        self.information = Frame(self.window, bg="blue")
        self.title = Frame(self.window, bg="red")
        self.timer = Frame(self.window, bg="green")
        self.topic = Frame(self.window, bg="yellow")
        self.letters = Frame(self.window, bg="pink")
        self.keyboard = Frame(self.window, bg="orange")

        self.information.grid(row=0, column=0, sticky="nsew")
        self.title.grid(row=0, column=1, sticky="nsew")
        self.timer.grid(row=0, column=2, sticky="nsew")
        self.topic.grid(row=1, column=1, sticky="nsew")
        self.letters.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.keyboard.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.grid()


    def grid(self):
        x = 6
        z = 5
        for i in range(x * z):
            b = Label(self.letters, width=20, height=20, image=self.blank, font=("Noto Sans SemiBold", 45), text=str(i)[0],
                      compound='c')
            b.grid(row=math.floor(i / x), column=i % x, sticky="nsew", padx=1, pady=1)
        for i in range(x):
            self.letters.columnconfigure(i, weight=1)
        for i in range(x + (z - x)):
            self.letters.rowconfigure(i, weight=1)

if __name__=="__main__":
    MainProgram()