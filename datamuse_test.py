from tkinter import *
import requests

window = Tk()
window.title("Joedle")
window.geometry("500x700")
window.configure(background="#59ADAD")

def search():
    query=topic.get()
    print("https://api.datamuse.com/words?ml="+query)
    request=requests.get("https://api.datamuse.com/words?topics="+query)
    words = request.json()
    print(words)
    t=[]
    for i in words[0:10]:
        t.append(i['word'])
    result["text"]="\n".join(t)

topic=Entry(window)
topic.pack()
enter=Button(window, width=5, height=1, command=search, text="Enter")
enter.pack(expand=True)
result=Label(window, width=30,height=20)
result.pack(pady=50)
mainloop()

















