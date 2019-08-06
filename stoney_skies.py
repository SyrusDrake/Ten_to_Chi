# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 06.08.2019

import tkinter as tk

root_width = 1120   # width of the main window
root_height = 700   # height of the main window

root = tk.Tk()

control = tk.Frame(bg='green')
control.place(relheight=0.9, relwidth=0.18, rely=0.05, relx=0.01)

canvas = tk.Frame(cursor='crosshair', bd=5, relief='groove')
canvas.place(relheight=0.90, relwidth=0.75, rely=0.05, relx=0.2)

b_undo = tk.Button(control, text="Undo", font=30)
b_undo.pack(pady=5, fill='x')

b_redo = tk.Button(control, text="Redo", font=30)
b_redo.pack(pady=5, fill='x')

b_clear = tk.Button(control, text="Clear canvas", font=30)
b_clear.pack(pady=5, fill='x')


root.geometry(f'{root_width}x{root_height}+100+100')
root.mainloop()
