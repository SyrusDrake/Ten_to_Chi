# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 09.06.2020

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import SetMarkers as mk
import shelve

marker_ID = 1   # For assigning IDs to the markers. Necessary becausue canvas object count starts at
marker_list = {}   # The "collection" of all markers.
distances = {}
version = "alpha"
max_size = 1024
markers = mk.Markers()


# <cf> Functions


def import_image():
    # function to import the reference image
    global img
    global max_size
    # The explorer window to let the user pick the file
    filename = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.png *.jpeg')])
    img = Image.open(filename)
    x = img.size[0]
    y = img.size[1]

    if x > max_size or y > max_size:
        ratio = x/y

        if x > y:
            x = int(max_size)
            y = int(max_size/ratio)
        if y > x:
            y = int(max_size)
            x = int(max_size*ratio)
        if x == y:
            x = y = 1024

    img = img.resize((x, y), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(10, 10, anchor='nw', image=img)


def save_pattern():
    print(marker_list)
    save_list = {}
    filename = filedialog.asksaveasfilename(filetypes=[('Pattern', '*.ptn')])
    x = 1
    for i in marker_list:
        ID = str(x)
        save_list[ID] = {}
        save_list[ID]['x'] = marker_list[i]['x']
        save_list[ID]['y'] = marker_list[i]['y']
        x += 1
    print(f'Saved list: {save_list}')
    save_file = shelve.open(filename, "n")
    save_file['marker_list'] = save_list
    save_file.close()


def test():
    print(canvas.find_withtag('marker')[-1])


# </cf> Functions

# <cf> drawing the interface


root_width = 1000   # width of the main window
root_height = 700   # height of the main window

root = tk.Tk()
root.title(f"Stoney Skies v.{version}")
root.geometry(f'{root_width}x{root_height}+100+100')
root.option_add('*tearOff', False)

# control = tk.Frame(height=150)
# control.pack(fill='x')
canvas = tk.Canvas(cursor='crosshair', bd=5, relief='groove')
# canvas.bind("<Configure>", draw_grid)
canvas.bind('<Button-1>', lambda event: markers.add_marker(event, canvas, "white"))
canvas.bind('<Button-3>', lambda event: markers.delete_marker(event, canvas))
canvas.pack(fill='both', expand=True)
# img = ImageTk.PhotoImage(Image.open('/mnt/DATA/OneDrive/Personal Files/Programming/Python/Stoney_Skies/image.jpg'))
# canvas.create_image(0, 0, anchor='nw', image=img)

menubar = tk.Menu(root)

m_canvas = tk.Menu(menubar)
menubar.add_cascade(label='File', menu=m_canvas)
m_canvas.add_command(label='Import Image', command=import_image)
m_canvas.add_command(label='Save Pattern', command=save_pattern)
m_canvas.add_command(label='Clear Canvas', command=lambda: markers.clear_all(canvas))

menubar.add_command(label="Test", command=test)

menubar.add_command(label="Quit!", command=root.quit)

# b_clear = tk.Button(control, text="Clear canvas", font=30, command=clear_canvas)
# b_clear.pack(padx=5, fill='x', side='left')
#
# # b_test = tk.Button(control, text="Import", font=30, command=import_image)
# # b_test.pack(pady=5, fill='x')
#
# b_test = tk.Button(control, text="Test", font=30, command=save_pattern)
# b_test.pack(padx=5, fill='x', side='left')
#
# b_quit = tk.Button(control, text="Quit", font=30, command=root.quit)
# b_quit.pack(padx=5, fill='x', side='left')


# </cf> drawing the interface

root.config(menu=menubar)
root.mainloop()
