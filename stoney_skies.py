# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 07.08.2019

import tkinter as tk

marker_ID = 1

# <cf> Classes


class Marker:
    def __init__(self, canvas, xc, yc):
        self.radius = 7
        self.x1 = xc - self.radius
        self.y1 = yc - self.radius
        self.x2 = xc + self.radius
        self.y2 = yc + self.radius
        self.id = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill='blue')

# </cf> Classes

# <cf> Functions


def place_marker(event):
    global marker_ID
    Marker(canvas, event.x, event.y)
    marker_ID += 1


def clear_canvas():
    canvas.delete('all')

# </cf> Functions

# <cf> drawing the interface


root_width = 1120   # width of the main window
root_height = 700   # height of the main window

root = tk.Tk()

control = tk.Frame(bg='green')
control.place(relheight=0.9, relwidth=0.18, rely=0.05, relx=0.01)

canvas = tk.Canvas(cursor='crosshair', bd=5, relief='groove')
canvas.bind("<Button-1>", place_marker)
canvas.place(relheight=0.90, relwidth=0.75, rely=0.05, relx=0.2)

b_undo = tk.Button(control, text="Undo", font=30)
b_undo.pack(pady=5, fill='x')

b_redo = tk.Button(control, text="Redo", font=30)
b_redo.pack(pady=5, fill='x')

b_clear = tk.Button(control, text="Clear canvas", font=30, command=clear_canvas)
b_clear.pack(pady=5, fill='x')

b_clear = tk.Button(control, text="Test", font=30)
b_clear.pack(pady=5, fill='x')

# </cf> drawing the interface

root.geometry(f'{root_width}x{root_height}+100+100')
root.mainloop()
