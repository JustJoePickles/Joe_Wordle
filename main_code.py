from tkinter import *
import math
from PIL import Image, ImageTk
import requests
import random
import string
from datetime import datetime, timedelta


# MainProgram is the class that initialises other classes and does the bulk
# of the logic, essentially everything leads back to it

class MainProgram:
    def __init__(self):

        # Setting up the game window, changing the title and size
        self.root = Tk()
        self.root.title("Joedle")
        self.root.geometry("500x700")

        # These are the image files for the timer, depending on how many
        # games the user has played a different one will be referenced
        self.images = ["two_outof_two.png", "one_outof_two.png",
                       "zero_outof_two.png"]
        # The top_layer method controls which class will be raised to the
        # top essentially determining whether the overlay is active or not
        self.top_layer = "overlay"
        self.games = 0  # The number of games the user has played
        self.date = datetime(1900, 1, 1)  # The date and time that has to be
        # reached before the user can play more games, by default it is set
        # to 1st of January 1900 to ensure it doesn't have any effect until
        # it is actually set later on

        self.homepage = HomePage(self)  # Initialising the homepage class,
        # creating it as a variable so it can be referenced later
        self.overlay = Overlay(self)  # Same thing for the overlay class

        # The next section is creating a dictionary that pairs a reference
        # term like "overlay" with it's corresponding variable (in this case
        # self.overlay . This is used to raise frames easily
        # without having to pass in the class object
        self.frames = {}
        for f in (self.homepage, self.overlay):
            page_name = f.reference
            frame = f.window
            self.frames[page_name] = frame

        # The changing of frames works by gridding both the overlay and
        # homepage frames to the same row and column so they're on top of
        # each other, consequently only row 0 and column 0 need to be given
        # weightings
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.mainloop()  # Calls the Tkinter event loop

    # The method for changing the visible frame. It works by taking the
    # reference passed through and raising the corresponding frame,
    # additionally it changes the top_layer variable so other methods can
    # know what is on top and then rebinds the keys depending on whether the
    # overlay or homepage is on top
    def change_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.top_layer = page_name
        self.keybinding()

    # A method used by both homepage and overlay, simply takes a file name
    # and a desired resolution and returns a PhotoImage object (widgets
    # cannot just take file paths) of the desired size
    def format_image(self, i, size):
        image = Image.open(i)
        image = image.resize(size)
        image = ImageTk.PhotoImage(image)
        return image

    # The method that is run when the user clicks the enter button in the
    # overlay window. This method is responsible for starting a new game as
    # well as checking whether the user is within their cooldown timer period
    def enter_topic(self):
        query = self.overlay.topic.get()  # Gets the users chosen topic
        now = datetime.now().time()  # Saves the current time for cooldown
        # checking

        # This part checks if the user's input is the required word length
        # (one word) and gives a prompt accordingly
        query_test = query.split(" ")  # Split the input at each space into a
        # list
        query_test = [x for x in query_test if x != ""]  # Remove blank
        # items (these are created through trailing whitespaces or an empty
        # entry box)
        if len(query_test) < 1 or len(query_test) > 1:  # If the length is
            # above or below the boundaries, clear the Entry box and prompt
            # the user to enter one word
            self.overlay.topic.delete(0, END)
            self.overlay.topic.insert(0, "Try using one word")
            return None  # Leaves the method without running the rest of the
            # code

        # This if statement checks whether the game has already started and
        # the user is just checking the overlay for the rules or whether the
        # user is still within their cooldown period, either way, clicking
        # the enter button should return them to the homepage without
        # generating a new word
        if self.overlay.started or datetime(2000, 1, 1, now.hour, now.minute,
                                            now.second) < self.date:
            self.change_frame("homepage")

        # This else statement is responsible for setting up a new game
        else:
            self.cursor = 0  # This is the tile on the word grid where the
            # user's next letter will go, whenever a new game is started,
            # this will return it back to the first tile
            self.row = 1  # As with the cursor, the row is used in typing
            # placement, by default it is the first row

            request = requests.get(
                "https://api.datamuse.com/words?topics=" + query)  # Calls
            # the datamuse api with the user's query, there are many
            # potential search functions, but topics= chooses words related
            # to the topic
            words = request.json()  # Converts the response object to a json
            # object which is easily readable

            # If the user's entry is one word but isn't a valid word and
            # therefore doesn't return any options, variable words will be
            # None and therefore the user will be prompted that their input
            # isn't a valid word
            if not words:
                self.overlay.topic.delete(0, END)
                self.overlay.topic.insert(0, "That is not a valid word")
                return None  # Exits the method early like before

            # Disables the topic Entry box and sets the disabled foreground
            # to look the same as the active one so the user doesn't notice
            # a change. This is because without this, even though the
            # overlay might not be visible, the user's cursor will still be
            # active in the Entry box and anything they type will go in there.
            self.overlay.topic.config(state=DISABLED)
            self.overlay.topic.config(
                disabledforeground=self.overlay.topic.cget('foreground'))

            # Chooses the first 20 words returned from datamuse and ensures
            # that they are within a character range (too short or too long
            # makes the game unplayable). Additionally, isalpha() ensures
            # the word only uses letters which provides a level of security
            # as the user wouldn't be able to guess words with special
            # characters or numbers
            options = []
            for i in words[0:20]:
                if 2 < len(i['word']) < 8 and i["word"].isalpha():
                    options.append(i['word'])

            self.overlay.started = True  # Records that the game has
            # started, used by other methods to determine specific actions
            self.choice = random.choice(options)  # Chooses a random word
            # from the list generated
            self.homepage.grid(len(self.choice))  # Creates a letter grid with
            # an x length the number of characters in the generated word and
            # a y length the number of guesses available (5)
            self.homepage.topic_label.config(font=self.homepage.font)  # This
            # changes the font to the default font and fontsize defined in
            # homepage, using a variable rather than hardcoding makes the code
            # more flexible
            self.homepage.topic_label["text"] = query  # Changes the topic
            # label to the user's entered topic so they can reference it
            # during the game
            self.change_frame("homepage")  # Changes frame from the overlay
            # to the homepage

    # Method used to bind/unbind letter keys plus backspace and enter
    def keybinding(self):
        keys = string.ascii_lowercase + string.ascii_uppercase  # Keybinding
        # is case sensitive in tkinter so this creates a string with every
        # uppercase and lowercase letter that can be iterated through for
        # binding
        keys = list(keys)

        # If the overlay is the top frame then unbind every key so the
        # user's actions don't translate onto the homepage
        if self.top_layer == "overlay" and self.overlay.started:
            for key in keys:
                self.root.unbind(key)
            self.root.unbind("<BackSpace>")

        # If the homepage is the top layer then bind the letter keys to the
        # key_press method and the backspace and enter keys to their
        # respective methods
        if self.top_layer == "homepage":
            for key in keys:
                self.root.bind(key, self.key_press)
            self.root.bind("<BackSpace>", self.backspace)
            self.root.bind("<Return>", self.enter)

    # Method for when a letter key is pressed or a letter button on the
    # on-screen keyboard
    def key_press(self, key):
        if not isinstance(key, str):  # Key will either be a keypress object
            # or a string depending on what called the method, this converts
            # key_press objects to a string containing the key that was pressed
            key = key.char

        # If statement to check if the user has reached the end of their
        # line. To explain this, it is probably important to define how the
        # cursor works: the 3D array of labels creating the letter grid is
        # placed in a 2D list meaning that the cursor simply needs one
        # variable to be able to reference any label. Thus, the cursor must
        # be less than the product of the length of the generated word and
        # the current row in order to still be on the same line as self.row
        # and to enter the user's keypress.
        if self.cursor < self.row * len(self.choice):
            # Changes the text of the label at cursor to be the user's
            # keypress (in uppercase)
            self.homepage.grid_objects[self.cursor].config(text=key.upper())
            self.cursor += 1

    # Method to be called to delete a letter
    def backspace(self, a):  # Calling methods through keybinding passes in
        # a (in this case unneeded) keypress object, hence the unused 'a' in
        # order to prevent errors
        if self.overlay.started:
            # This ensures the cursor isn't at the first tile in the row (
            # which would then delete into the previous guess
            if self.cursor > (self.row - 1) * len(self.choice):
                self.cursor -= 1
            self.homepage.grid_objects[self.cursor].config(text="")

    # Method that's responsible for checking a user's guess and calling
    # the game_over method as necessary
    def enter(self, a):  # 'a' serves the same purpose as in backspace
        if self.overlay.started:
            if self.cursor == self.row * len(self.choice):  # Ensures that
                # the user has typed up until the end of the line so they're
                # entering a full completed guess
                guess = []  # List that will store the letters in the guess
                guess_label = []  # List that will store the corresponding
                # label objects in the guess

                # Appends the letters and objects from every label in the
                # current row to the necessary lists
                for label in self.homepage.grid_objects[
                             self.cursor - len(self.choice):self.cursor]:
                    guess.append(label.cget("text").lower())
                    guess_label.append(label)

                blue = []  # List to store the letters that are correct in the
                # correct position (these will be coloured blue)
                blue_label = []  # Store the corresponding label objects

                # Checks if the letter in the users guess is the same as the
                # letter in the same position in the word and if so appends
                # the information to the necessary blue lists
                for i in range(len(guess)):
                    if guess[i] == self.choice[i]:
                        blue.append(guess[i])
                        blue_label.append(guess_label[i])

                yellow = []  # List to store the letters that are correct in
                # the wrong position (these will be coloured yellow)
                yellow_label = []  # Store the corresponding label objects

                # Iterates through the guess and adds all the label
                # objects/letters that aren't already confirmed blue;
                # however if the number of these letters exceeds the number
                # in the generated word, no more will be added. For example
                # if the word was swede and the user guessed soils,
                # the first s will have already been coloured blue, but the
                # second s wont be coloured yellow as that would imply to
                # the user that there are two s tiles in the word, thus it
                # won't be added to the list
                for i in range(len(guess)):
                    if guess_label[i] not in blue_label and yellow.count(
                            guess[i]) + blue.count(
                            guess[i]) < self.choice.count(guess[i]):
                        yellow.append(guess[i])
                        yellow_label.append(guess_label[i])

                # The information in the initial yellow lists needs to be
                # iterated through and saved whilst also extracting certain
                # items, the easiest way to do this is to create another list
                yellow_two = []
                yellow_label_two = []

                # Iterates through the letters in yellow and checks if
                # they're in the word, if they are it adds them and their
                # corresponding label to their respective lists
                for i in range(len(yellow)):
                    if yellow[i] in self.choice:
                        yellow_two.append(yellow[i])
                        yellow_label_two.append(yellow_label[i])

                label_remover = []  # List to store labels that need to be
                # removed, at this point we're removing duplicate letters so
                # the only way to distinguish them is using their
                # corresponding labels

                # This loop removes duplicate yellow tiles, meaning that if
                # the user entered three ‘w’ tiles in swede for example,
                # only one would be highlighted (note it's counting down
                # in order to ensure the highlighted tile is the first
                # relevant occurrence)
                for i in range(len(yellow_two) - 1, -1, -1):
                    if yellow_two[i] in yellow_two[:i]:
                        label_remover.append(yellow_label_two[i])

                # Creates a list of all the items that are in yellow_two and
                # not in label_remover, essentially removes the labels in
                # label_remover from the list
                yellow_label = [i for i in yellow_label_two if
                                i not in label_remover]

                # These loop change the background colours of the labels in
                # yellow_label and blue_label to their respective colours
                for item in blue_label:
                    item.configure(background="#3B6D8C")
                    item.update()
                for item in yellow_label:
                    item.configure(background="#F2CC0F")
                    item.update()

                # If blue_label equals guess_label then the user's guess is
                # correct
                if blue_label == guess_label:
                    # Changes the topic label to read You win!... and calls
                    # the game_over method
                    self.homepage.topic_label.config(
                        font=("Noto Sans SemiBold", 14))
                    self.homepage.topic_label[
                        "text"] = \
                        "You Win! Click the info button to start another game."
                    self.game_over()
                elif self.row == 5:  # If they're on the 5th row they're out
                    # of guesses and so the word will be revealed and game
                    # over calles
                    self.homepage.topic_label.config(
                        font=("Noto Sans SemiBold", 14))
                    self.homepage.topic_label[
                        "text"] = "Game Over. The word was " + self.choice
                    self.game_over()
                else:  # Otherwise they still have guess remaining so they
                    # move to typing a row down
                    self.row += 1

    # Method in charge of handling new games and game limits
    def game_over(self):
        self.overlay.topic.config(state=NORMAL)  # Make the topic box
        # editable so the user can enter a new topic

        # If the user has used up their three games unbind the keys, get the
        # current time and set their time to the current time plus 20 minutes
        if self.games == 2:
            self.overlay.started = False
            self.keybinding()

            now = datetime.now().time()
            d1 = datetime(2000, 1, 1, now.hour, now.minute, now.second)
            self.date = d1 + timedelta(minutes=20)

            # Updates the topic label to tell the user the word along with
            # when they can play again
            self.homepage.topic_label.config(
                text="The word was " + self.choice + ", play again at " + str(
                    self.date.time()))
            self.games = 0  # resets the number of games

        else:  # If the user has games remaining, unbind the keys and change
            # the timer image to the next one (note the timer image is
            # labelled according to the remaining games, so 0,1,2 rather
            # than 1,2,3)
            self.overlay.started = False
            self.keybinding()
            self.games += 1
            img = self.format_image(self.images[self.games], (50, 50))
            self.homepage.timer_screen.configure(image=img)
            self.homepage.timer_screen.image = img  # As the image is being
            # changed within a method, this line is necessary in order to
            # prevent the new image being lost to garbage collection


# Sets up everything needed for the overlay gui
class Overlay:
    def __init__(self, root):
        self.reference = "overlay"  # The reference that will be used in the
        # frames dictionary to link with this class' frame

        # Setting up the frame, gridding it and setting the font
        self.window = Frame(root.root, bg="pink", width=0, height=0,
                            highlightbackground="white", highlightthickness=1)
        self.window.grid(row=0, column=0, sticky="nsew", padx=40, pady=15)
        self.font = ("Noto Sans SemiBold", 14)

        self.started = False  # The overlay is initialised at the beginning
        # so the game hasn't started

        # Configuring the necessary rows and columns with the required weights
        self.window.rowconfigure(0, weight=4)
        self.window.rowconfigure(1, weight=10)
        self.window.rowconfigure(2, weight=1)

        self.window.columnconfigure(0, weight=1)

        # Defining the frames to hold the widgets
        title = Frame(self.window, bg="#0D0D13")
        instructions = Frame(self.window, bg="#0D0D13")
        topic_frame = Frame(self.window, bg="#0D0D13")

        # Gridding the frames
        title.grid(row=0, column=0, sticky="nsew")
        instructions.grid(row=1, column=0, sticky="nsew")
        topic_frame.grid(row=2, column=0, sticky="nsew")

        w, h = 400, 528  # The width and height of the instructions image,
        # set as variables for the sake of flexibility
        instructions.rowconfigure(0, weight=1)
        instructions.columnconfigure(0, weight=1)
        self.instructions_image = root.format_image("cos_instructions.png",
                                                    (w, h))  # Formatting
        # the image

        # Creating and then gridding the instructions
        instructions_label = Label(instructions, image=self.instructions_image,
                                   bg="#0D0D13", borderwidth=0)
        instructions_label.grid(row=0, column=0, sticky="nsew")

        # Configuring the columns for the topic frame, this will hold the
        # entry box and enter button
        topic_frame.columnconfigure(0, weight=5)
        topic_frame.columnconfigure(1, weight=1)
        topic_frame.rowconfigure(0, weight=1)

        # Creating the title, topic, and entry button and then putting all
        # three onto their respective frames
        self.title_image = root.format_image("joedle.png", (100, 25))
        title_screen = Label(title, image=self.title_image, width=10,
                             height=20, compound="c", bg="#0D0D13")
        title_screen.pack(side=LEFT, expand=True, fill='both')

        self.topic = Entry(topic_frame, font=self.font)
        enter = Button(topic_frame, text="Enter", font=self.font,
                       command=lambda: root.enter_topic())

        self.topic.grid(row=0, column=0, sticky="nsew", pady=(0, 20), padx=10)
        enter.grid(row=0, column=1, sticky="nsew", pady=(0, 20), padx=(20, 30))


# Sets up everything required for the homepage gui
class HomePage:
    def __init__(self, root):
        self.reference = "homepage"
        self.blank = PhotoImage()  # Creates a blank 1px by 1px image,
        # used later in the letters grid
        self.font = ("Noto Sans SemiBold", 20)

        # Creating the frame and configuring the columns/rows
        self.window = Frame(root.root, bg="#0D0D13", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=6)
        self.window.columnconfigure(2, weight=1)

        self.window.rowconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=8)
        self.window.rowconfigure(3, weight=4)

        # Creating the frames within the main frame in which the widgets
        # will be placed
        self.information = Frame(self.window, bg="#0D0D13")
        self.title = Frame(self.window, bg="#0D0D13")
        self.timer = Frame(self.window, bg="#0D0D13")
        self.topic = Frame(self.window, bg="#0D0D13")
        self.letters = Frame(self.window, bg="#0D0D13")
        self.keyboard = Frame(self.window, bg="#0D0D13")

        # Gridding these frames onto their respective cells
        self.information.grid(row=0, column=0, sticky="nsew")
        self.title.grid(row=0, column=1, sticky="nsew")
        self.timer.grid(row=0, column=2, sticky="nsew")
        self.topic.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.letters.grid(row=2, column=0, columnspan=3, sticky="nsew",
                          padx=10)
        self.keyboard.grid(row=3, column=0, columnspan=3, sticky="nsew",
                           padx=20, pady=10)

        # As the keyboard isn't a uniform grid but a series of three offset
        # rows, three frames are needed within the keyboard frame
        self.row_zero = Frame(self.keyboard, bg="#0D0D13")
        self.row_one = Frame(self.keyboard, bg="#0D0D13")
        self.row_two = Frame(self.keyboard, bg="#0D0D13")

        self.row_zero.grid(row=0, column=0, sticky="nsew")
        self.row_one.grid(row=1, column=0, sticky="nsew")
        self.row_two.grid(row=2, column=0, sticky="nsew")

        # Configuring the columns in the keyboard
        self.keyboard.columnconfigure(0, weight=1)
        for i in range(3):
            self.keyboard.rowconfigure(i, weight=1)

        # Creating a spacer for the second line in the keyboard as there are
        # ten keys in the first row and only 9 in the second, so padding is
        # needed either side
        spacer = Label(self.row_one, width=20, height=20, image=self.blank,
                       compound='c', bg="#0D0D13")
        spacer.pack(side="left", fill="both", expand=False, padx=1, pady=1)

        # Creating the timer which requires a formatted PhotoImage and a
        # label to hold it
        self.timer_image = root.format_image(root.images[0], (50, 50))
        self.timer_screen = Label(self.timer, image=self.timer_image, width=5,
                                  height=5, bg="#0D0D13")
        self.timer_screen.pack(side=LEFT, expand=True, fill='both')

        # Creating the title image which has the same requirements
        self.title_image = root.format_image("joedle.png", (400, 90))
        self.title_screen = Label(self.title, image=self.title_image, width=10,
                                  height=20, compound="c", bg="#0D0D13")
        self.title_screen.pack(side=LEFT, expand=True, fill='both')

        # Creating the infobutton which has the same requiremnts once again
        # except this time its a button. Note that the borderwidth, relief,
        # and activebackground components are all set so that pressing the
        # button doesn't show the button's rectangular shape but rather
        # makes it look like the circular info_image displaces slightly
        self.info_image = root.format_image("info.png", (50, 50))
        self.infobutton = Button(self.information, image=self.info_image,
                                 width=10, height=10, compound="c",
                                 relief="flat",
                                 borderwidth=0,
                                 bg="#0D0D13", activebackground="#0D0D13",
                                 command=lambda: root.change_frame("overlay"))
        self.infobutton.pack(side=LEFT, expand=True, fill='both')

        # Creating the topic label in which the topic and other messages to
        # the user will be displayed
        self.topic_label = Label(self.topic, bg="#0D0D13", fg="white",
                                 text="example label",
                                 font=self.font, image=self.blank,
                                 compound="c", width=10, height=10)
        self.topic_label.pack(side=LEFT, expand=True, fill='both')

        # Creates the keyboard, root is passed through so that the methods
        # from the MainProgram class can be bound to keys
        self.keyboard_maker(root)

    # Method to create the letter grid
    def grid(self, x):
        # Destroy the previous set of widgets so that if the grid is being
        # created to a different size in the second game then they wont show
        for widget in self.letters.winfo_children():
            widget.destroy()

        # It is important that the grid_objects list is reset every time
        # this method is run, otherwise the key_press method will write the
        # letters onto the preexisting labels, whether they exist or not
        self.grid_objects = []

        z = 5  # The vertical height of the grid, essentially the number of
        # guesses

        #  Loop to create the grid, creates a Label of desired arguments,
        #  grids it into the appropriate row and column using some maths and
        #  then adds the label to a masterlist for later reference
        for i in range(x * z):
            b = Label(self.letters, width=20, height=20, image=self.blank,
                      font=("Noto Sans SemiBold", 45),
                      text="",
                      compound=TOP, bg="#29292E", fg="white")
            b.grid(row=math.floor(i / x), column=i % x, sticky="nsew", padx=2,
                   pady=1)
            self.grid_objects.append(b)

        # Resets the column weighting, so if the second guess is a shorter
        # word that requires less columns then it will still fill the entire
        # frame, the word cannot be 8 or more letters so resetting up to
        # column 8 is suitable
        for i in range(8):
            self.letters.columnconfigure(i, weight=0)

        # Then weight the rows and columns according to how many letters
        # there are
        for i in range(x):
            self.letters.columnconfigure(i, weight=1)
        for i in range(z):
            self.letters.rowconfigure(i, weight=1)

    # Method to create the keyboard
    def keyboard_maker(self, root):
        # Function to create a label in frame(type) and of text determined by
        # position i. This button is linked up to the keypress method
        def label_maker(type, i):
            b = Button(type, width=20, height=20, image=self.blank,
                       font=self.font,
                       text=letters[i], compound='c', bg="#29292E", fg="white",
                       relief="flat",
                       command=lambda: root.key_press(letters[i]))
            b.pack(side="left", fill="both", expand=True, padx=1, pady=1)

        # The keyboard letters, used to determine which letter based on the
        # iteration of the loop
        letters = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S",
                   "D", "F", "G", "H", "J", "K", "L", "",
                   "⌫", "Z", "X", "C", "V", "B", "N", "M", "Enter", ""]

        x, z = 10, 3  # Defining the dimensions of the keyboard as if t was
        # a grid
        for i in range(x * z):

            # This is row zero, as it has 10 keys in no extra logic is needed
            if math.floor(i / x) == 0:
                label_maker(self.row_zero, i)

            # This is row one, it only has 9 keys so the last iteration of
            # the loop for this row will be ignored (note the blank element
            # after L in the letters list in order to keep the correct index)
            if math.floor(i / x) == 1:
                if i % x != 9:
                    label_maker(self.row_one, i)

            # This is the final row, along with having only 7 letter keys,
            # it also contains the backspace and enter keys which come with
            # their own set of unique requirements
            if math.floor(i / x) == 2:

                # This is the first key which is the backspace and so is
                # hooked up to the backspace method
                if i % x == 0:
                    b = Button(self.row_two, width=50, height=20,
                               image=self.blank,
                               font=("Noto Sans SemiBold", 15),
                               text=letters[i], compound='c', bg="#29292E",
                               fg="white", relief="flat",
                               command=lambda: root.backspace(letters[i]))
                    b.pack(side="left", fill="both", expand=True, padx=1,
                           pady=1)

                # This is the 9th key and will be the enter key, hooked up
                # to the enter method. Also note the different widths and font
                # sizes of these two buttons
                elif i % x == 8:
                    b = Button(self.row_two, width=50, height=20,
                               image=self.blank,
                               font=("Noto Sans SemiBold", 15),
                               text=letters[i], compound='c', bg="#29292E",
                               fg="white", relief="flat",
                               command=lambda: root.enter(letters[i]))
                    b.pack(side="left", fill="both", expand=True, padx=1,
                           pady=1)

                # The loop is running for a 10x3 grid, however this row only
                # contains 9 keys so it will pass on the 10th
                elif i % x == 9:
                    pass

                # Create the letters in between
                else:
                    label_maker(self.row_two, i)
        # Creates the final spacer for the other side to make things
        # symmetrical
        spacer = Label(self.row_one, width=20, height=20, image=self.blank,
                       compound='c', bg="#0D0D13")
        spacer.pack(side="left", fill="both", expand=False, padx=1, pady=1)


# Initialises the MainProgram class and begins the code
if __name__ == "__main__":
    MainProgram()
