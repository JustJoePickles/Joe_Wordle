from tkinter import *
import requests
print(11%4)

t=[["a","b"],"c","d","e","f","g"]
print(t[1:1+3])
if "a" in t:
    print("Works")
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

enter.after(200, lambda: enter.configure(background="white"))
enter.after(400, lambda: enter.configure(background="yellow"))
mainloop()

















