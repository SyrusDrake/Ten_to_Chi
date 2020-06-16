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


# <cf> Classes


# </cf> Classes

# <cf> Functions

def place_marker(event):
    # Funuction to add the marker. Adds it to marker_list.
    global marker_ID
    global marker_list
    # marker_list.append(mk.Marker(canvas, event.x, event.y, 'white'))
    mk.Marker(canvas, event.x, event.y, 'white')
    # newMarker = {}
    # newMarker['ID'] = marker_ID
    # newMarker['x'] = event.x
    # newMarker['y'] = event.y
    # marker_list.append(newMarker)
    handle = canvas.find_withtag('marker')[-1]
    marker_list[handle] = {'ID': marker_ID, 'x': event.x, 'y': event.y}
    marker_ID += 1
    print(marker_list)


def clear_canvas():
    global marker_ID
    global marker_list
    # Function to clear the entire canvas of all markers
    canvas.delete('marker')
    marker_ID = 1
    marker_list = {}


def delete_marker(event):
    global marker_ID
    global marker_list
    # Function to delete the current marker under the mouse pointer.
    object_id = (canvas.find_withtag('current')[0])  # object ID under cursor
    del marker_list[object_id]
    canvas.delete(object_id)  # deletes the object under cursor


def import_image():
    # function to import the reference image
    global img
    filename = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.png *.jpeg')])     # The explorer window to let the user pick the file
    img = ImageTk.PhotoImage(Image.open(filename))
    canvas.create_image(0, 0, anchor='nw', image=img)


def save_pattern():
    print(marker_list)
    save_list = {}
    filename = filedialog.asksaveasfilename(filetypes=[('Pattern', '*.ptn')])
    for i in marker_list:
        save_list[str(i)] = marker_list[i]
    print(save_list)
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
canvas.bind('<Button-1>', place_marker)
canvas.bind('<Button-3>', delete_marker)
canvas.pack(fill='both', expand=True)
# img = ImageTk.PhotoImage(Image.open('/mnt/DATA/OneDrive/Personal Files/Programming/Python/Stoney_Skies/image.jpg'))
# canvas.create_image(0, 0, anchor='nw', image=img)

menubar = tk.Menu(root)

m_canvas = tk.Menu(menubar)
menubar.add_cascade(label='File', menu=m_canvas)
m_canvas.add_command(label='Import Image', command=import_image)
m_canvas.add_command(label='Save Pattern', command=save_pattern)
m_canvas.add_command(label='Clear Canvas', command=clear_canvas)

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
