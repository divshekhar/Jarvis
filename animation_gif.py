from tkinter import *
import time
import os


root = Tk()
# root.configure(background='black')

frames = [PhotoImage(file='./img/loading.gif', format='gif -index %i' % (i))
          for i in range(57)]


def update(ind):
    frame = frames[ind]
    if ind == 56:
        ind = 0
    ind += 1
    label.configure(background='black')
    label.configure(image=frame)
    root.after(100, update, ind)


label = Label(root)
label.pack()
root.after(100, update, 0)
root.mainloop()
