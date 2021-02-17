# Florian Fruehwirth
# Main GUI for the app with different pages for different functions
# Last change: 04.02.2021
# Frame-switching based on:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# Menubar-switching: https://stackoverflow.com/questions/37621071/tkinter-add-menu-bar-in-frames

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import SetMarkers as mk
from PIL import ImageTk, Image
import shelve
from Atlas import *
from Astrolabe import *
from threading import Thread, Event
from os import path


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # List of all used frames
        # They're NOT strings but actual classes.
        frames = [
            StartPage,
            UserMapPage,
            StarMapPage,
            AstrolabePage
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
        self.c_background = '#02385C'
        self.c_label = "#02385C"
        self.c_button = "#024977"
        tk.Frame.__init__(self, location, bg=self.c_background)

        # title = tk.Label(self, text='Start page', bg=self.c_label)

        usermap_lable = tk.Label(self, text='Create a pattern map from an image', bg=self.c_label)
        usermap_button = tk.Button(self, text='User Map', command=lambda: controller.show_frame('UserMapPage'), bg=self.c_button)

        starmap_lable = tk.Label(self, text='Calculate a star map for a given position and time', bg=self.c_label)
        starmap_button = tk.Button(self, text='Star Map', command=lambda: controller.show_frame('StarMapPage'), bg=self.c_button)

        astrolabe_lable = tk.Label(self, text='Search for a specific pattern in the stars', bg=self.c_label)
        astrolabe_button = tk.Button(self, text='Astrolabe', command=lambda: controller.show_frame('AstrolabePage'), bg=self.c_button)

        # title.grid(row=0, pady=20)
        usermap_lable.grid(row=1, pady=(20, 0))
        usermap_button.grid(row=2, pady=(0, 20))
        starmap_lable.grid(row=3, pady=5)
        starmap_button.grid(row=4, pady=(0, 20))
        astrolabe_lable.grid(row=5, pady=5)
        astrolabe_button.grid(row=6, pady=(0, 20))

        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Start Page")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMapPage'))
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMapPage'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('AstrolabePage'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


class UserMapPage(tk.Frame):

    def __init__(self, location, controller):
        self.markers = mk.Markers()

        self.c_background = '#E1DEC6'
        self.c_label = "#E1DEC6"
        self.c_button = "#D7D2B2"
        self.c_text = "black"

        tk.Frame.__init__(self, location, bg=self.c_background)
        # label = tk.Label(self, text='This is the User Map creation screen')
        # label.grid(row=0)

        self.import_button = tk.Button(self, text='Import Image', command=lambda: self.import_image(), bg=self.c_button, fg=self.c_text)
        self.save_button = tk.Button(self, text='Save Pattern', command=lambda: self.save_pattern(), bg=self.c_button, fg=self.c_text)
        self.load_button = tk.Button(self, text='Load Pattern', command=lambda: self.load_pattern(), bg=self.c_button, fg=self.c_text)
        self.clear_button = tk.Button(self, text='Clear Canvas', command=lambda: self.markers.clear_all(self.canvas), bg=self.c_button, fg=self.c_text)

        self.canvas = tk.Canvas(self, width=900, height=900, cursor='crosshair', bd=5, relief='groove')
        self.canvas.bind('<Button-1>', lambda event: self.markers.add_marker(event.x, event.y, self.canvas, "white"))
        self.canvas.bind('<Button-3>', lambda event: self.markers.delete_marker(event, self.canvas))

        self.import_button.grid(row=0, column=0)
        self.save_button.grid(row=0, column=1)
        self.load_button.grid(row=0, column=2)
        self.clear_button.grid(row=0, column=3)
        self.canvas.grid(row=1, columnspan=4, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)

        current_menu = tk.Menu(menubar, tearoff=0)
        # current_menu.add_command(label='Import Image', command=lambda: self.import_image())
        # current_menu.add_command(label='Save Pattern', command=lambda: self.save_pattern())
        # current_menu.add_command(label='Load Pattern', command=lambda: self.load_pattern())
        # current_menu.add_command(label='Clear Canvas', command=lambda: self.markers.clear_all(self.canvas))
        menubar.add_cascade(label='User Map', menu=current_menu)

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Start Page", command=lambda: root.show_frame('StartPage'))
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMapPage'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('AstrolabePage'))
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
            ratio = x / y

            if x > y:
                x = int(max_size)
                y = int(max_size / ratio)
            if y > x:
                y = int(max_size)
                x = int(max_size * ratio)
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


class StarMapPage(tk.Frame):

    def __init__(self, location, controller):

        self.c_background = '#04003F'
        self.c_label = "#04003F"
        self.c_button = "#06005D"
        self.c_text = "white"

        self.stop_calculations = Event()
        tk.Frame.__init__(self, location, bg=self.c_background)
        # label = tk.Label(self, text='This is the Star Map creation screen')
        # label.grid(row=0)

        self.mag_scale = tk.Scale(self, label='Magnitude', from_=1.0, to=6.5, resolution=0.5, orient='horizontal')
        self.mag_scale.set(4.5)
        self.mag_scale.grid(row=1, pady=20)

        self.timescale = tk.Label(self, text='Timescale', bg=self.c_label, fg=self.c_text)
        self.start_scale = tk.Scale(self, label='Initial Year', from_=0, to=60000, resolution=1000, orient='horizontal', command=self.update_start)
        self.end_scale = tk.Scale(self, label='Final Year', from_=0, to=60000, resolution=1000, orient='horizontal', command=self.update_end)
        self.end_scale.set(60000)
        self.step_scale = tk.Scale(self, label='Step Size', from_=500, to=60000, resolution=500, orient='horizontal')

        self.position = tk.Label(self, text='Position in °N (int)', bg=self.c_label, fg=self.c_text)
        vpos = (self.register(self.validate_latitude), "%P")
        self.position_entry = tk.Entry(self, validate="key", validatecommand=vpos)

        self.neighbors = tk.Label(self, text='Number of nearest neighbours for each star to check', bg=self.c_label, fg=self.c_text)
        vnei = (self.register(self.validate_neighbors), "%P")
        self.ngh = tk.StringVar()
        self.ngh.set(100)
        self.neighbors_entry = tk.Entry(self, validate="key", validatecommand=vnei, textvariable=self.ngh)

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=100, mode='indeterminate')
        self.label_complete = tk.Label(self, text='Complete!', fg='green')

        button_test = tk.Button(self, text="Start", command=self.commence, bg=self.c_button, fg=self.c_text)
        # button_stop = tk.Button(self, text="Stop", command=self.stop_calculations.set)
        # button_stop.grid(row=12, pady=5)

        self.timescale.grid(row=2)
        self.start_scale.grid(row=3)
        self.end_scale.grid(row=4)
        self.step_scale.grid(row=5)
        self.position.grid(row=6, pady=(20, 0))
        self.position_entry.grid(row=7)
        self.neighbors.grid(row=8, pady=(20, 0))
        self.neighbors_entry.grid(row=9)
        button_test.grid(row=11, pady=5)


        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Star Map")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Start Page", command=lambda: root.show_frame('StartPage'))
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMapPage'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('AstrolabePage'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar

    def commence(self):
        if (self.position_entry.get() == ""):
            messagebox.showwarning("Missing Latitude", "Please input a position between 0°N and 90°N")
        elif (int(self.neighbors_entry.get()) > 100):
            neighbors_warning = messagebox.askyesno("Large Number", "The number of nearest neighbours you set may result in excessively large file sizes and little additional benefit over a value of 100. Continue?")
            if neighbors_warning is True:
                Thread(target=self.calculate_atlas).start()
            # else:
            #     print('halt')
        else:
            total_size = int((self.end_scale.get() - self.start_scale.get()) / (self.step_scale.get() + 1) * 150)
            print(total_size)
            start = messagebox.askyesno("Commence?", f"Start the calculated with the parameters specified? Calculations may take several minutes to complete. \nThe total file size may be {total_size} MB or more. Make sure enough space is available.")
            if start is True:
                Thread(target=self.calculate_atlas).start()
            # else:
            #     print('halt')

    def calculate_atlas(self):
        # self.stop_calculations.clear()
        self.label_complete.grid_forget()
        self.progress_bar.grid(row=10, pady=10)
        self.progress_bar.start(10)
        self.Atlas = Atlas(int(self.position_entry.get()), self.start_scale.get(), self.step_scale.get(), self.end_scale.get(), self.mag_scale.get(), int(self.neighbors_entry.get()))
        self.Atlas.createAtlas()
        print("Testing:")
        print(f"Magnitude: {self.Atlas.mag_limit}")
        print(f"Time Scale: From {self.Atlas.ybp_min} to {self.Atlas.ybp_max} with {self.Atlas.step_size}-year steps")
        print(f"Position: {self.Atlas.latitude}°N")
        print(f"Neighbors: {self.Atlas.neighbours}")
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.label_complete.grid(row=10, pady=10)

    def update_start(self, x):
        self.end_scale.config(from_=x)
        year_diff = self.end_scale.get() - int(x)
        self.step_scale.config(to=year_diff)
        if (year_diff == 0):
            self.step_scale.config(from_=0)

    def update_end(self, x):
        self.start_scale.config(to=x)
        year_diff = int(x) - self.start_scale.get()
        self.step_scale.config(to=year_diff)
        if (year_diff == 0):
            self.step_scale.config(from_=0)

    def validate_latitude(self, input):
        if input.isnumeric() and int(input) <= 90 or input == "":
            return True
        else:
            return False

    def validate_neighbors(self, input):
        if input.isnumeric() and int(input) <= 5000 or input == "":
            return True
        else:
            return False


class AstrolabePage(tk.Frame):

    def __init__(self, location, controller):

        self.c_background = '#867245'
        self.c_label = "#867245"
        self.c_button = "#7D6B40"
        self.c_text = "white"

        self.pattern_set = False
        self.map_set = False

        tk.Frame.__init__(self, location, bg=self.c_background)
        # self.label = tk.Label(self, text='This is the calculation screen')
        self.pattern_label = tk.Label(self, text='Choose a user pattern', bg=self.c_label, fg=self.c_text)
        self.pattern_button = tk.Button(self, text='Choose', command=self.choose_pattern, bg=self.c_button, fg=self.c_text)
        self.map_label = tk.Label(self, text='Choose a star map', bg=self.c_label, fg=self.c_text)
        self.map_button = tk.Button(self, text='Choose', command=self.choose_map, bg=self.c_button, fg=self.c_text)
        self.precision_label = tk.Label(self, text="Adjust the search precision.\n (Changing these values is not recommended)", bg=self.c_label, fg=self.c_text)
        self.dist_dev = tk.Entry(self)
        self.dist_dev.insert(0, "3.9")
        self.ang_dev = tk.Entry(self)
        self.ang_dev.insert(0, "0.4")

        self.checkbool = tk.BooleanVar()
        self.checkbool.set(False)
        self.debug_check = tk.Checkbutton(self, text='Create debug file?', variable=self.checkbool)

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=100, mode='indeterminate')
        self.label_complete = tk.Label(self, text='Complete!', fg='green')

        self.start_button = tk.Button(self, text='Start', command=self.commence, bg=self.c_button, fg=self.c_text)

        # self.label.grid(row=0, columnspan=2)
        self.pattern_label.grid(row=1, columnspan=2, pady=(10, 0))
        self.pattern_button.grid(row=2, columnspan=2)
        self.map_label.grid(row=3, columnspan=2, pady=(10, 0))
        self.map_button.grid(row=4, columnspan=2, pady=(0, 10))
        self.precision_label.grid(row=5, columnspan=2)
        self.dist_dev.grid(row=6, column=0, sticky="E")
        self.ang_dev.grid(row=6, column=1, sticky="W")
        self.start_button.grid(row=8, columnspan=2, pady=10)
        self.debug_check.grid(row=9, columnspan=2, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def choose_pattern(self):
        file = filedialog.askopenfilename(filetypes=[('Patterns', '*.ptn')])
        self.markers = shelve.open(file)['marker_list']
        self.pattern_label.configure(text=path.basename(file))
        self.pattern_set = True

    def choose_map(self):
        file = filedialog.askopenfilename(filetypes=[('Maps', '*.map')])
        self.map = shelve.open(file)['map']
        self.map_label.configure(text=path.basename(file))
        self.map_set = True

    def commence(self):
        if (self.pattern_set is False):
            messagebox.showwarning("Missing Pattern", "Please select a user pattern")
        elif (self.map_set is False):
            messagebox.showwarning("Missing Map", "Please select a star map")
        else:
            Thread(target=self.calculate_astrolabe).start()

    def calculate_astrolabe(self):
        self.label_complete.grid_forget()
        self.progress_bar.grid(row=7, columnspan=2, pady=10)
        self.progress_bar.start(10)
        self.astrolabe = Astrolabe(self.markers, self.map, float(self.dist_dev.get()), float(self.ang_dev.get()), self.checkbool.get())
        self.astrolabe.calculate_marker_distances()
        self.astrolabe.calculate_marker_bearings()
        self.astrolabe.calculate()
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.label_complete.grid(row=7, columnspan=2, pady=10)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Astrolabe")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Start Page", command=lambda: root.show_frame('StartPage'))
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMapPage'))
        pagemenu.add_command(label="StarMap", command=lambda: root.show_frame('StarMapPage'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


app = App()
app.title("Stoney Skies")
icon = tk.PhotoImage(file='icon.gif')
app.tk.call('wm', 'iconphoto', app._w, icon)
app.geometry('750x500+1400+400')
app.mainloop()
