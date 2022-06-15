from tkinter import *
import math
from PIL import Image, ImageTk


class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.root.title("Joedle")
        self.root.geometry("500x700")
        self.root.configure(background="white")
        self.homepage = HomePage(self)
        self.overlay = Overlay(self)
        self.frames = {}
        for f in (self.homepage, self.overlay):
            page_name = f.reference
            frame = f.window
            self.frames[page_name] = frame

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.mainloop()

    def change_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def format_image(self, i, size):
        image = Image.open(i)
        image = image.resize(size)
        image = ImageTk.PhotoImage(image)
        return image


class Overlay():
    def __init__(self, root):
        self.reference = "overlay"
        self.window = Frame(root.root, bg="pink", width=0, height=0, highlightbackground="white", highlightthickness=1)
        self.window.grid(row=0, column=0, sticky="nsew", padx=40, pady=15)

        self.font = ("Noto Sans SemiBold", 14)

        self.window.rowconfigure(0, weight=4)
        self.window.rowconfigure(1, weight=10)
        self.window.rowconfigure(2, weight=1)

        self.window.columnconfigure(0, weight=1)



        title = Frame(self.window, bg="orange")
        instructions = Frame(self.window, bg="Blue")
        topic_frame = Frame(self.window, bg="#0D0D13")

        title.grid(row=0, column=0, sticky="nsew")
        instructions.grid(row=1, column=0, sticky="nsew")
        topic_frame.grid(row=2, column=0, sticky="nsew")

        w, h = 400, 528
        instructions.rowconfigure(0, weight=1)
        instructions.columnconfigure(0, weight=1)
        self.instructions_image = root.format_image("cos_instructions.png", (w, h))
        instructions_label = Label(instructions, image=self.instructions_image, bg="#0D0D13", borderwidth=0)
        instructions_label.grid(row=0, column=0, sticky="nsew")

        topic_frame.columnconfigure(0, weight=5)
        topic_frame.columnconfigure(1, weight=1)
        topic_frame.rowconfigure(0, weight=1)
        topic = Entry(topic_frame, font=self.font)
        enter = Button(topic_frame, text="Enter", font=self.font, command=lambda: root.change_frame("homepage"))

        topic.grid(row=0, column=0, sticky="nsew", pady=20, padx=10)
        enter.grid(row=0, column=1, sticky="nsew", pady=20, padx=50)
        instructions.update()
        print(instructions.winfo_width(), instructions.winfo_height())

class HomePage():
    def __init__(self, root):
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.window = Frame(root.root, bg="red", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")
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
        self.info_image = root.format_image("info.png", (50, 50))

        self.infobutton = Button(self.information, image=self.info_image, width=10, height=10, compound="c",
                                 relief="flat",
                                 borderwidth=0,
                                 bg="white", activebackground="white", command=lambda: root.change_frame("overlay"))
        self.infobutton.pack(side=LEFT, expand=True, fill='both')
        self.grid()

    def grid(self):
        x = 6
        z = 5
        for i in range(x * z):
            b = Label(self.letters, width=20, height=20, image=self.blank, font=("Noto Sans SemiBold", 45),
                      text=str(i)[0],
                      compound='c')
            b.grid(row=math.floor(i / x), column=i % x, sticky="nsew", padx=1, pady=1)
        for i in range(x):
            self.letters.columnconfigure(i, weight=1)
        for i in range(x + (z - x)):
            self.letters.rowconfigure(i, weight=1)


if __name__ == "__main__":
    MainProgram()
