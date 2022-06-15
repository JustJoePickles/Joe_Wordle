from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("overlay")
window.geometry("500x700")
window.configure(background="white")

font=("Noto Sans SemiBold", 14)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=4)
window.rowconfigure(2, weight=1)

window.columnconfigure(0, weight=1)


def format_image(i, size):
    image = Image.open(i)
    image = image.resize(size)
    image = ImageTk.PhotoImage(image)
    return image


title = Frame(window, bg="Green")
instructions = Frame(window, bg="Blue")
topic_frame = Frame(window, bg="Orange")

title.grid(row=0, column=0, sticky="nsew")
instructions.grid(row=1, column=0, sticky="nsew")
topic_frame.grid(row=2, column=0, sticky="nsew")

blank = PhotoImage()
w, h = 500, 419
instructions.rowconfigure(0, weight=1)
instructions.columnconfigure(0, weight=1)
instructions_image = format_image("cos_instructions.png", (w, h))
instructions_label = Label(instructions, image=instructions_image, bg="#0D0D13")
instructions_label.grid(row=0, column=0, sticky="nsew")

topic_frame.columnconfigure(0, weight=5)
topic_frame.columnconfigure(1,weight=1)
topic_frame.rowconfigure(0,weight=1)
topic=Entry(topic_frame, font=font)
enter=Button(topic_frame, text="Enter", font=font)

topic.grid(row=0, column=0, sticky="nsew", pady=20,padx=10)
enter.grid(row=0, column=1, sticky="nsew", pady=20, padx=50)

mainloop()
