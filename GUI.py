# Florian Fruehwirth
# Main GUI for the app with different pages for different functions
# Last change: 05.11.2020
# Frame-switching based on:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# Menubar-switching: https://stackoverflow.com/questions/37621071/tkinter-add-menu-bar-in-frames

import tkinter as tk
from tkinter import filedialog
import SetMarkers as mk
from PIL import ImageTk, Image
import shelve


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # List of all used frames
        # They're NOT strings but actual classes.
        frames = [
            StartPage,
            UserMap,
            StarMap,
            Astrolabe
        ]

        # Creates a container for all the pages (should never be visible)
        frame_container = tk.Frame(self, bg='red')
        frame_container.pack(side='top', fill='both', expand=True)
        frame_container.grid_rowconfigure(0, weight=1)
        frame_container.grid_columnconfigure(0, weight=1)

        # Initiates a dictionary of frames
        self.framedict = {}

        # Fills the dictionary. Keys=names defined above; values=instances of the classes below
        for frame in (frames):
            name = frame.__name__  # The name of the class currently being called
            new_frame = frame(location=frame_container, controller=self)
            self.framedict[name] = new_frame
            new_frame.grid(row=0, column=0, sticky='nsew')

        # Starts the app with the start page
        self.show_frame('StartPage')

    # Function that calls up any frame in the dictionary
    def show_frame(self, page_name):
        frame = self.framedict[page_name]
        frame.tkraise()

        menubar = frame.menubar(self)
        self.configure(menu=menubar)


class StartPage(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='blue')
        title = tk.Label(self, text='This is the start page')
        title.grid(row=0, pady=20)

        usermap_lable = tk.Label(self, text='Create a pattern map from an image')
        usermap_lable.grid(row=1, pady=5)
        usermap_button = tk.Button(self, text='User Map', command=lambda: controller.show_frame('UserMap'))
        usermap_button.grid(row=2, pady=(0, 20))

        usermap_lable = tk.Label(self, text='Calculate a star map for a given position and time')
        usermap_lable.grid(row=3, pady=5)
        usermap_button = tk.Button(self, text='Star Map', command=lambda: controller.show_frame('StarMap'))
        usermap_button.grid(row=4, pady=(0, 20))

        usermap_lable = tk.Label(self, text='Search for a specific pattern in the stars')
        usermap_lable.grid(row=5, pady=5)
        usermap_button = tk.Button(self, text='Astrolabe', command=lambda: controller.show_frame('Astrolabe'))
        usermap_button.grid(row=6, pady=(0, 20))


        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Start Page")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMap'))
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMap'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('Astrolabe'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


class UserMap(tk.Frame):

    def __init__(self, location, controller):
        self.markers = mk.Markers()

        tk.Frame.__init__(self, location, bg='yellow')
        label = tk.Label(self, text='This is the User Map creation screen')
        label.grid(row=0)

        self.canvas = tk.Canvas(self, width=900, height=900, cursor='crosshair', bd=5, relief='groove')
        self.canvas.bind('<Button-1>', lambda event: self.markers.add_marker(event.x, event.y, self.canvas, "white"))
        self.canvas.bind('<Button-3>', lambda event: self.markers.delete_marker(event, self.canvas))
        self.canvas.grid(row=1, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)

        current_menu = tk.Menu(menubar, tearoff=0)
        current_menu.add_command(label='Import Image', command=lambda: self.import_image())
        current_menu.add_command(label='Save Pattern', command=lambda: self.save_pattern())
        current_menu.add_command(label='Load Pattern', command=lambda: self.load_pattern())
        current_menu.add_command(label='Clear Canvas', command=lambda: self.markers.clear_all(self.canvas))
        menubar.add_cascade(label='User Map', menu=current_menu)

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMap'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('Astrolabe'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar

    def import_image(self):
        # function to import the reference image
        max_size = 1024
        # The explorer window to let the user pick the file
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.png *.jpeg')])
        self.img = Image.open(filename)
        self.img_save = None
        x = self.img.size[0]
        y = self.img.size[1]

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

        self.img = self.img.resize((x, y), Image.ANTIALIAS)
        self.img_save = self.img
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(10, 10, anchor='nw', image=self.img)

    def save_pattern(self):
        print(self.markers.marker_list)
        save_list = {}
        filename = filedialog.asksaveasfilename(filetypes=[('Pattern', '*.ptn')])
        x = 1
        for i in self.markers.marker_list:
            ID = str(x)
            save_list[ID] = {}
            save_list[ID]['x'] = self.markers.marker_list[i]['x']
            save_list[ID]['y'] = self.markers.marker_list[i]['y']
            x += 1
        print(f'Saved list: {save_list}')
        save_file = shelve.open(filename, "n")
        save_file['marker_list'] = save_list
        if self.img_save is not None:
            print("image")
            save_file['image'] = self.img_save
        save_file.close()

    def load_pattern(self):
        loadfile = filedialog.askopenfilename(filetypes=[('Patterns', '*.ptn')])
        self.img = shelve.open(loadfile)['image']
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(10, 10, anchor='nw', image=self.img)
        marker_list = shelve.open(loadfile)['marker_list']
        for m in marker_list:
            self.markers.add_marker(marker_list[m]['x'], marker_list[m]['y'], self.canvas, 'white')


class StarMap(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='black')
        label = tk.Label(self, text='This is the Star Map creation screen')
        label.grid(row=0)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Star Map")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMap'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('Astrolabe'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


class Astrolabe(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='green')
        label = tk.Label(self, text='This is the calculation screen')
        label.grid(row=0)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Astrolabe")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMap'))
        pagemenu.add_command(label="StarMap", command=lambda: root.show_frame('StarMap'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


app = App()
app.title("Stoney Skies")
icon = tk.PhotoImage(file='icon.gif')
app.tk.call('wm', 'iconphoto', app._w, icon)
app.geometry('1000x1000+1400+400')
app.mainloop()
