from tkinter import *
import math
from PIL import Image, ImageTk
import requests
import random
import string
from datetime import datetime, timedelta


class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.root.title("Joedle")
        self.root.geometry("500x700")
        self.root.configure(background="white")
        self.images = ["two_outof_two.png", "one_outof_two.png", "zero_outof_two.png"]

        self.top_layer = "overlay"
        self.games = 0
        self.date = datetime(1900, 1, 1)
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
        self.top_layer = page_name
        self.keybinding()

    def format_image(self, i, size):
        image = Image.open(i)
        image = image.resize(size)
        image = ImageTk.PhotoImage(image)
        return image

    def enter_topic(self):
        query = self.overlay.topic.get()
        now = datetime.now().time()
        query_test = query.split(" ")
        query_test = [x for x in query_test if x != ""]
        if len(query_test) < 1 or len(query_test) > 1:
            self.overlay.topic.delete(0, END)
            self.overlay.topic.insert(0, "Try using one word")
            return None
        if self.overlay.started or datetime(2000, 1, 1, now.hour, now.minute, now.second) < self.date:
            self.change_frame("homepage")
        else:
            self.cursor = 0
            self.row = 1
            request = requests.get("https://api.datamuse.com/words?topics=" + query)
            words = request.json()
            if not words:
                self.overlay.topic.delete(0, END)
                self.overlay.topic.insert(0, "That is not a valid word")
                return None
            self.overlay.topic.config(state=DISABLED)
            self.overlay.topic.config(disabledforeground=self.overlay.topic.cget('foreground'))
            options = []
            for i in words[0:20]:
                if 2 < len(i['word']) < 8 and i["word"].isalpha():
                    options.append(i['word'])
            self.overlay.started = True
            self.choice = random.choice(options)
            self.homepage.grid(len(self.choice))
            self.homepage.topic_label.config(font=self.homepage.font)
            self.homepage.topic_label["text"] = query
            self.change_frame("homepage")

    def keybinding(self):
        keys = string.ascii_lowercase + string.ascii_uppercase
        keys = list(keys)
        if self.top_layer == "overlay" and self.overlay.started:
            for key in keys:
                self.root.unbind(key)
            self.root.unbind("<BackSpace>")
        if self.top_layer == "homepage":
            for key in keys:
                self.root.bind(key, self.key_press)
            self.root.bind("<BackSpace>", self.backspace)
            self.root.bind("<Return>", self.enter)

    def key_press(self, key):
        if not isinstance(key, str):
            key = key.char
        if self.cursor < self.row * len(self.choice):
            self.homepage.grid_objects[self.cursor].config(text=key.upper())
            self.cursor += 1

    def backspace(self, a):
        if self.overlay.started:
            if self.cursor > (self.row - 1) * len(self.choice):
                self.cursor -= 1
            self.homepage.grid_objects[self.cursor].config(text="")

    def enter(self, a):
        if self.overlay.started:
            if self.cursor == self.row * len(self.choice):
                guess = []
                guess_label = []
                for label in self.homepage.grid_objects[self.cursor - len(self.choice):self.cursor]:
                    guess.append(label.cget("text").lower())
                    guess_label.append(label)
                blue = []
                blue_label = []
                for i in range(len(guess)):
                    if guess[i] == self.choice[i]:
                        blue.append(guess[i])
                        blue_label.append(guess_label[i])
                yellow = []
                yellow_label = []
                for i in range(len(guess)):
                    if guess_label[i] not in blue_label and yellow.count(guess[i]) + blue.count(
                            guess[i]) < self.choice.count(guess[i]):
                        yellow.append(guess[i])
                        yellow_label.append(guess_label[i])
                yellow_two = []
                yellow_label_two = []
                for i in range(len(yellow)):
                    if yellow[i] in self.choice:
                        yellow_two.append(yellow[i])
                        yellow_label_two.append(yellow_label[i])
                label_remover = []
                for i in range(len(yellow_two) - 1, -1, -1):
                    if yellow_two[i] in yellow_two[:i]:
                        label_remover.append(yellow_label_two[i])
                yellow_label = [i for i in yellow_label_two if i not in label_remover]
                for item in blue_label:
                    item.configure(background="#3B6D8C")
                    item.update()
                for item in yellow_label:
                    item.configure(background="#F2CC0F")
                    item.update()
                if blue_label == guess_label:
                    self.homepage.topic_label.config(font=("Noto Sans SemiBold", 14))
                    self.homepage.topic_label["text"] = "You Win! Click the info button to start another game."
                    self.game_over()
                elif self.row == 5:
                    self.homepage.topic_label.config(font=("Noto Sans SemiBold", 14))
                    self.homepage.topic_label["text"] = "Game Over. The word was "+self.choice
                    self.game_over()
                else:
                    self.row += 1

    def game_over(self):
        self.overlay.topic.config(state=NORMAL)
        if self.games == 2:
            self.overlay.started = False
            self.keybinding()

            now = datetime.now().time()
            d1 = datetime(2000, 1, 1, now.hour, now.minute, now.second)
            self.date = d1 + timedelta(minutes=1)
            self.homepage.topic_label.config(text="You have reached your limit, play again at " + str(self.date.time()))
            self.games = 0
        else:
            self.overlay.started = False
            self.keybinding()
            self.games += 1
            img = self.format_image(self.images[self.games], (50, 50))
            self.homepage.timer_screen.configure(image=img)
            self.homepage.timer_screen.image = img


class Overlay():
    def __init__(self, root):
        self.reference = "overlay"
        self.window = Frame(root.root, bg="pink", width=0, height=0, highlightbackground="white", highlightthickness=1)
        self.window.grid(row=0, column=0, sticky="nsew", padx=40, pady=15)

        self.font = ("Noto Sans SemiBold", 14)

        self.started = False

        self.window.rowconfigure(0, weight=4)
        self.window.rowconfigure(1, weight=10)
        self.window.rowconfigure(2, weight=1)

        self.window.columnconfigure(0, weight=1)

        title = Frame(self.window, bg="#0D0D13")
        instructions = Frame(self.window, bg="#0D0D13")
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

        self.title_image = root.format_image("joedle.png", (100, 25))
        title_screen = Label(title, image=self.title_image, width=10, height=20, compound="c", bg="#0D0D13")
        title_screen.pack(side=LEFT, expand=True, fill='both')

        self.topic = Entry(topic_frame, font=self.font)
        enter = Button(topic_frame, text="Enter", font=self.font, command=lambda: root.enter_topic())

        self.topic.grid(row=0, column=0, sticky="nsew", pady=(0, 20), padx=10)
        enter.grid(row=0, column=1, sticky="nsew", pady=(0, 20), padx=(20, 30))


class HomePage():
    def __init__(self, root):
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.font = ("Noto Sans SemiBold", 20)
        self.window = Frame(root.root, bg="#0D0D13", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")
        # self.window.pack(side=LEFT, expand=True, fill='both')
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=6)
        self.window.columnconfigure(2, weight=1)

        self.window.rowconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=8)
        self.window.rowconfigure(3, weight=4)

        self.information = Frame(self.window, bg="#0D0D13")
        self.title = Frame(self.window, bg="#0D0D13")
        self.timer = Frame(self.window, bg="#0D0D13")
        self.topic = Frame(self.window, bg="#0D0D13")
        self.letters = Frame(self.window, bg="#0D0D13")
        self.keyboard = Frame(self.window, bg="#0D0D13")

        self.information.grid(row=0, column=0, sticky="nsew")
        self.title.grid(row=0, column=1, sticky="nsew")
        self.timer.grid(row=0, column=2, sticky="nsew")
        self.topic.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.letters.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10)
        self.keyboard.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)

        self.row_zero = Frame(self.keyboard, bg="#0D0D13")
        self.row_one = Frame(self.keyboard, bg="#0D0D13")
        self.row_two = Frame(self.keyboard, bg="#0D0D13")

        self.keyboard.columnconfigure(0, weight=1)
        for i in range(3):
            self.keyboard.rowconfigure(i, weight=1)
        spacer = Label(self.row_one, width=20, height=20, image=self.blank, compound='c', bg="#0D0D13")
        spacer.pack(side="left", fill="both", expand=False, padx=1, pady=1)

        self.row_zero.grid(row=0, column=0, sticky="nsew")
        self.row_one.grid(row=1, column=0, sticky="nsew")
        self.row_two.grid(row=2, column=0, sticky="nsew")

        self.timer_image = root.format_image(root.images[0], (50, 50))
        self.timer_screen = Label(self.timer, image=self.timer_image, width=5, height=5, bg="#0D0D13")
        self.timer_screen.pack(side=LEFT, expand=True, fill='both')

        self.title_image = root.format_image("joedle.png", (400, 90))
        self.title_screen = Label(self.title, image=self.title_image, width=10, height=20, compound="c", bg="#0D0D13")
        self.title_screen.pack(side=LEFT, expand=True, fill='both')

        self.info_image = root.format_image("info.png", (50, 50))
        self.infobutton = Button(self.information, image=self.info_image, width=10, height=10, compound="c",
                                 relief="flat",
                                 borderwidth=0,
                                 bg="#0D0D13", activebackground="#0D0D13", command=lambda: root.change_frame("overlay"))
        self.infobutton.pack(side=LEFT, expand=True, fill='both')

        self.topic_label = Label(self.topic, bg="#0D0D13", fg="white", text="example label",
                                 font=self.font, image=self.blank, compound="c", width=10, height=10)
        self.topic_label.pack(side=LEFT, expand=True, fill='both')

        self.keyboard_maker(root)

    def grid(self, x):
        for widget in self.letters.winfo_children():
            widget.destroy()
        self.grid_objects = []
        z = 5
        for i in range(x * z):
            b = Label(self.letters, width=20, height=20, image=self.blank, font=("Noto Sans SemiBold", 45),
                      text="",
                      compound=TOP, bg="#29292E", fg="white")
            b.grid(row=math.floor(i / x), column=i % x, sticky="nsew", padx=2, pady=1)
            self.grid_objects.append(b)
        for i in range(9):
            self.letters.columnconfigure(i, weight=0)
        for i in range(x):
            self.letters.columnconfigure(i, weight=1)
        for i in range(z):
            self.letters.rowconfigure(i, weight=1)

    def keyboard_maker(self, root):
        def label_maker(type, i):
            b = Button(type, width=20, height=20, image=self.blank, font=self.font,
                       text=letters[i], compound='c', bg="#29292E", fg="white", relief="flat",
                       command=lambda: root.key_press(letters[i]))
            b.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "",
                   "???", "Z", "X", "C", "V", "B", "N", "M", "Enter", ""]

        x, z = 10, 3
        for i in range(x * z):

            if math.floor(i / x) == 0:
                label_maker(self.row_zero, i)

            if math.floor(i / x) == 1:
                if i % x != 9:
                    label_maker(self.row_one, i)

            if math.floor(i / x) == 2:
                if i % x == 0:
                    b = Button(self.row_two, width=50, height=20, image=self.blank, font=("Noto Sans SemiBold", 15),
                               text=letters[i], compound='c', bg="#29292E", fg="white", relief="flat",
                               command=lambda: root.backspace(letters[i]))
                    b.pack(side="left", fill="both", expand=True, padx=1, pady=1)
                elif i % x == 8:
                    b = Button(self.row_two, width=50, height=20, image=self.blank, font=("Noto Sans SemiBold", 15),
                               text=letters[i], compound='c', bg="#29292E", fg="white", relief="flat",
                               command=lambda: root.enter(letters[i]))
                    b.pack(side="left", fill="both", expand=True, padx=1, pady=1)
                elif i % x == 9:
                    pass
                else:
                    label_maker(self.row_two, i)
        spacer = Label(self.row_one, width=20, height=20, image=self.blank, compound='c', bg="#0D0D13")
        spacer.pack(side="left", fill="both", expand=False, padx=1, pady=1)


if __name__ == "__main__":
    MainProgram()
