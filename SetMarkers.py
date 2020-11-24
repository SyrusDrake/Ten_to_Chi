class Markers:
    # The class for the user-added markers. Take center coordinates. Color
    # will be unnecessary in the future and is only used for development.

    def __init__(self):
        self.current_ID = 1  # For assigning IDs to the markers. Necessary becausue canvas object count starts at
        self.marker_list = {}  # The "collection" of all markers.
        self.radius = 7     # Radius is fixed. Might be an option later.

    def add_marker(self, event, canvas, color):
        xCoord = event.x
        yCoord = event.y
        x1 = xCoord - self.radius  # Because the oval takes coordinates of the
        # bounding box, that has to be calculates from given center coords.
        y1 = yCoord - self.radius
        x2 = xCoord + self.radius
        y2 = yCoord + self.radius
        self.id = canvas.create_oval(x1, y1, x2, y2, fill=color, tag='marker')
        handle = canvas.find_withtag('marker')[-1]
        self.marker_list[handle] = {'ID': self.current_ID, 'x': xCoord, 'y': yCoord}
        self.current_ID += 1
        print(self.marker_list)

    def delete_marker(self, event, canvas):
        # Function to delete the current marker under the mouse pointer.
        object_id = (canvas.find_withtag('current')[0])  # object ID under cursor
        del self.marker_list[object_id]
        canvas.delete(object_id)  # deletes the object under cursor

    def clear_all(self, canvas):
        canvas.delete('marker')
        self.current_ID = 1
        self.marker_list = {}
