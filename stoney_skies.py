# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 13.08.2019

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import SetMarkers as mk
import pickle

marker_ID = 1   # For assigning IDs to the markers. Necessary becausue canvas object count starts at
marker_list = []    # The "collection" of all markers.
version = " alpha"

# <cf> Star coordinates

# Loads star list from Starmap save file
load_file = open('save.dat', 'rb')
star_list = pickle.load(load_file)
load_file.close()

# For testing purposes only. Star coordinates will be imported from external file in the future.

stretch = 20.9

star_list_test = {'star1': (43.54361, 52.82556),
                  'star2': (50.63028, 55.22028),
                  'star3': (51.04972, 58.82917),
                  'star4': (59.89667, 60.15667),
                  'star5': (55.4325, 64.61861)}

z1, a1 = star_list_test['star1']
z2, a2 = star_list_test['star2']
z3, a3 = star_list_test['star3']
z4, a4 = star_list_test['star4']
z5, a5 = star_list_test['star5']

v2 = (round(z2-z1, 2)*stretch, round(a2-a1, 2)*stretch)
v3 = (round(z3-z1, 2)*stretch, round(a3-a1, 2)*stretch)
v4 = (round(z4-z1, 2)*stretch, round(a4-a1, 2)*stretch)
v5 = (round(z5-z1, 2)*stretch, round(a5-a1, 2)*stretch)


# </cf> Star coordinates

# <cf> Classes


# </cf> Classes

# <cf> Functions

def place_marker(event):
    # Funuction to add the marker. Adds it to marker_list.
    global marker_ID
    global marker_list
    marker_list.append(mk.Marker(canvas, event.x, event.y, 'white'))
    print(marker_list[-1].get_coordinates())
    marker_ID += 1


def clear_canvas():
    # Function to clear the entire canvas of all markers but not the grid
    canvas.delete('marker')


def delete_marker(event):
    # Function to delete the current marker under the mouse pointer.
    object_id = (canvas.find_withtag('current')[0])  # object ID under cursor
    canvas.delete(object_id)  # deletes the object under cursor
    del marker_list[object_id-1]  # deletes the relevant marker object


def draw_grid(event):
    # Creates a grid over the canvas. Not sure if it will remain necessary.
    canvas.delete("grid")   # Deletes grid so it doesn't "smear" when resizing
    w = event.width     # Passes the currenz size of the canvas
    h = event.height
    r = 20  # Determines the size of the grid. The bigger this number the smaller the grid.
    for x in range(0, r):
        canvas.create_line((w/r)*x, 0, (w/r)*x, h, tag=('grid'))
    for y in range(0, r):
        canvas.create_line(0, (h/r)*y, w, (h/r)*y, tag=('grid'))


def import_image():
    # function to import the reference image
    global img
    filename = filedialog.askopenfilename()     # The explorer window to let the user pick the file
    img = ImageTk.PhotoImage(Image.open(filename))
    canvas.create_image(0, 0, anchor='nw', image=img)


def set_scale(event):
    # Creates a selector to let the user define the area of interest
    canvas.delete('scale')
    canvas.create_line(p_middle.get()-(p_width.get()/2), 0, p_middle.get()-(p_width.get()/2), canvas_height, tag=('scale'))
    canvas.create_line(p_middle.get()+(p_width.get()/2), 0, p_middle.get()+(p_width.get()/2), canvas_height, tag=('scale'))
    canvas.create_line(p_middle.get(), 0, p_middle.get(), canvas_height, fill='red', tag=('scale'))


def test():

    c1 = marker_list[0].get_coordinates()
    c2 = (c1[0]+v2[0], c1[1]-v2[1])
    c3 = (c1[0]+v3[0], c1[1]-v3[1])
    c4 = (c1[0]+v4[0], c1[1]-v4[1])
    c5 = (c1[0]+v5[0], c1[1]-v5[1])

    mk.Marker(canvas, *c1, 'blue')
    mk.Marker(canvas, *c2, 'red')
    mk.Marker(canvas, *c3, 'red')
    mk.Marker(canvas, *c4, 'red')
    mk.Marker(canvas, *c5, 'red')
    # Function for testing function. Gets called by button of same name.
    # pass


# </cf> Functions

# <cf> drawing the interface


root_width = 1120   # width of the main window
root_height = 700   # height of the main window
control_width = root_width*0.18     # Width of the control panel on the left
control_height = root_height*0.9
canvas_width = root_width*0.75  # Width of the canvas
canvas_height = root_height*0.9

root = tk.Tk()
root.title(f"Stoney Skies v.{version}")

control = tk.Frame()
control.pack(side='left')
canvas = tk.Canvas(height=canvas_height, width=canvas_width, cursor='crosshair', bd=5, relief='groove')
#canvas.bind("<Configure>", draw_grid)
canvas.bind('<Button-1>', place_marker)
canvas.bind('<Button-3>', delete_marker)
canvas.pack()
#img = ImageTk.PhotoImage(Image.open('D:\Dropbox\Programmieren\Python\Stoney_Skies\image.jpg'))
#canvas.create_image(0, 0, anchor='nw', image=img)


b_clear = tk.Button(control, text="Clear canvas", font=30, command=clear_canvas)
b_clear.pack(pady=5, fill='x')

b_test = tk.Button(control, text="Import", font=30, command=import_image)
b_test.pack(pady=5, fill='x')

b_test = tk.Button(control, text="Test", font=30, command=test)
b_test.pack(pady=5, fill='x')

b_quit = tk.Button(control, text="Quit", font=30, command=root.quit)
b_quit.pack(pady=5, fill='x')

p_width = tk.Scale(control, from_=0, to=canvas_width, orient='horizontal', label="Area width", command=set_scale)
p_width.pack()

p_middle = tk.Scale(control, from_=0, to=canvas_width, orient='horizontal', label="Area center", command=set_scale)
p_middle.set(canvas_width/2)
p_middle.pack()


# </cf> drawing the interface

root.geometry(f'{root_width}x{root_height}+100+100')
root.mainloop()
