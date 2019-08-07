# Florian Fruehwirth
# Stoney Skies Alpha
# This version is non-functional and used for the design and development of
# the GUI.
# Last change: 07.08.2019

import tkinter as tk

marker_ID = 0   # For assigning IDs to the markers. Probably unnecessary.
list_of_markers = []    # The "collection" of all markers.

# <cf> Classes


class Marker:
    # The class for the user-added markers. Take center coordinates. Color
    # will be unnecessary in the future and is only used for development.
    def __init__(self, canvas, xc, yc, color):
        self.radius = 7     # Radius is fixed. Might be an option later.
        self.xc = xc
        self.yc = yc
        self.x1 = xc - self.radius  # Because the oval takes coordinates of the
        # bounding box, that has to be calculates from given center coords.
        self.y1 = yc - self.radius
        self.x2 = xc + self.radius
        self.y2 = yc + self.radius
        self.id = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=color)

    def return_coordinates(self):
        # returns the coordinates of a marker as list
        coordinates = [self.xc, self.yc]
        return(coordinates)

# </cf> Classes

# <cf> Functions


def place_marker(event):
    # Funuction to add the marker. Adds it to list_of_markers. marker_ID
    # probably unnecessary.
    global marker_ID
    global list_of_markers
    list_of_markers.append(Marker(canvas, event.x, event.y, 'red'))
    marker_ID += 1


def clear_canvas():
    # Function to clear the entire canvas of all markers
    canvas.delete('all')


def undo():
    # Undo function deletes the marker itself as well as its object held
    # in the list_of_markers.
    canvas.delete(list_of_markers[-1].id)
    del list_of_markers[-1]

def test():
    # Function for testing function. Gets called by button of same name.
    pass


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

b_undo = tk.Button(control, text="Undo", font=30, command=undo)
b_undo.pack(pady=5, fill='x')

b_redo = tk.Button(control, text="Redo", font=30)
b_redo.pack(pady=5, fill='x')

b_clear = tk.Button(control, text="Clear canvas", font=30, command=clear_canvas)
b_clear.pack(pady=5, fill='x')

b_test = tk.Button(control, text="Test", font=30, command=test)
b_test.pack(pady=5, fill='x')

b_quit = tk.Button(control, text="Quit", font=30, command=root.quit)
b_quit.pack(pady=5, fill='x')

# </cf> drawing the interface

testMarker = canvas.create_oval(50, 50, 100, 100, fill='yellow')
root.geometry(f'{root_width}x{root_height}+100+100')
root.mainloop()
