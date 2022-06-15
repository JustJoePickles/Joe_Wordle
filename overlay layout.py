from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("overlay")
window.geometry("500x700")
window.configure(background="white")

window.rowconfigure(0, weight=2)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=8)

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

blank=PhotoImage()
w,h=500,419
instructions.rowconfigure(0, weight=1)
instructions.columnconfigure(0, weight=1)
instructions_image= format_image("cos_instructions.png", (w,h))
instructions_label=Label(instructions, image=instructions_image, bg="#0D0D13")
instructions_label.grid(row=0, column=0, sticky="nsew")



mainloop()
