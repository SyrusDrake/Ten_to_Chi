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
        self.id = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=color, tag='marker')

    def get_coordinates(self):
        # returns the coordinates of a marker as list
        coordinates = (self.xc, self.yc)
        return(coordinates)
