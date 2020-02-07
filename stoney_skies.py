# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 03.02.2020

import tkinter as tk
from tkinter import filedialog
# from PIL import ImageTk, Image (# Temporarily disabled because not installed on MF and I can't be bothered to install it)
import SetMarkers as mk
import pickle
import math as m

marker_ID = 1   # For assigning IDs to the markers. Necessary becausue canvas object count starts at
marker_list = []    # The "collection" of all markers.
distances = {}
version = " alpha"

# <cf> Star coordinates

# Loads star list from Starmap save file
load_file = open('save.dat', 'rb')
star_list = pickle.load(load_file)
load_file.close()


# </cf> Star coordinates

# <cf> Classes


# </cf> Classes

# <cf> Functions

def place_marker(event):
    # Funuction to add the marker. Adds it to marker_list.
    global marker_ID
    global marker_list
    # marker_list.append(mk.Marker(canvas, event.x, event.y, 'white'))
    mk.Marker(canvas, event.x, event.y, 'white')
    newMarker = {}
    newMarker['ID'] = marker_ID
    newMarker['x'] = event.x
    newMarker['y'] = event.y
    marker_list.append(newMarker)
    marker_ID += 1
    print(marker_list)


def clear_canvas():
    global marker_ID
    global marker_list
    # Function to clear the entire canvas of all markers but not the grid
    canvas.delete('marker')
    marker_ID = 1
    marker_list = []


def delete_marker(event):
    global marker_ID
    global marker_list
    # Function to delete the current marker under the mouse pointer.
    object_id = (canvas.find_withtag('current')[0])  # object ID under cursor
    marker_list = [i for i in marker_list if not (i['ID'] == object_id)]  # deletes the corresponding marker list entry by searching
    # for an item whose ID matches the object ID
    canvas.delete(object_id)  # deletes the object under cursor


# Temporarily disabled because not installed on MF and I can't be bothered to install it
# def import_image():
#     # function to import the reference image
#     global img
#     filename = filedialog.askopenfilename()     # The explorer window to let the user pick the file
#     img = ImageTk.PhotoImage(Image.open(filename))
#     canvas.create_image(0, 0, anchor='nw', image=img)


def test():
    distances = calculate_marker_distances()
    print(distances)
    normalized_distances = normalize()
    print(normalized_distances)
    # Function for testing. Gets called by button of same name.
    # pass


def calculate_marker_distances():
    master = marker_list[0]
    x1 = master['x']
    y1 = master['y']
    for marker in marker_list[1:]:
        x2 = marker['x']
        y2 = marker['y']
        dis = m.sqrt((x2-x1)**2+(y2-y1)**2)  # calculates the distances
        distances[f"dis_{marker['ID']}"] = dis
    return distances


# Normalizes all distances so that one is 1.0 and all others are fractions of that
def normalize():
    normalized_distances = {}
    ref_distance = list(distances.values())[0]  # Takes the first entry in the list of distances. Any other would work too.
    for i in distances:  # Iterates through the entire list and divides all distances by the chosen reference distance.
        normalized_distances[i] = (distances[i]/ref_distance)
    return normalized_distances  # returns a new list of normalized distances


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
# canvas.bind("<Configure>", draw_grid)
canvas.bind('<Button-1>', place_marker)
canvas.bind('<Button-3>', delete_marker)
canvas.pack()
# img = ImageTk.PhotoImage(Image.open('D:\Dropbox\Programmieren\Python\Stoney_Skies\image.jpg'))
# canvas.create_image(0, 0, anchor='nw', image=img)


b_clear = tk.Button(control, text="Clear canvas", font=30, command=clear_canvas)
b_clear.pack(pady=5, fill='x')

# b_test = tk.Button(control, text="Import", font=30, command=import_image)
# b_test.pack(pady=5, fill='x')

b_test = tk.Button(control, text="Test", font=30, command=test)
b_test.pack(pady=5, fill='x')

b_quit = tk.Button(control, text="Quit", font=30, command=root.quit)
b_quit.pack(pady=5, fill='x')


# </cf> drawing the interface

root.geometry(f'{root_width}x{root_height}+100+100')
root.mainloop()
