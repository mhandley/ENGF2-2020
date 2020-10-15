from tkinter import *

def key(event):
    if event.char == 'q':
        rootwindow.destroy()

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 200

rootwindow = Tk();
rootwindow.bind_all('<Key>', key)
canvas = Canvas(rootwindow, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(side = LEFT, fill=BOTH, expand=TRUE)
textwidget = canvas.create_text(150, 100, anchor="c")
version = rootwindow.tk.call("info", "patchlevel")
canvas.itemconfig(textwidget, text="Success! Tk version: "  + version)
textwidget2 = canvas.create_text(150, 130, anchor="c")
canvas.itemconfig(textwidget2, text="Press q to exit")

while True:
    rootwindow.update()

