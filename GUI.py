# Florian Fruehwirth
# Main GUI for the app with different pages for different functions
# Last change: 05.11.2020
# Frame-switching based on:
# https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
# Menubar-switching: https://stackoverflow.com/questions/37621071/tkinter-add-menu-bar-in-frames

import tkinter as tk


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
        label = tk.Label(self, text='This is the start page')
        label.grid(row=0)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="User Map")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="User Map", command=lambda: root.show_frame('UserMap'))
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMap'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('Astrolabe'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


class UserMap(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='yellow')
        label = tk.Label(self, text='This is the User Map creation screen')
        label.grid(row=0)

        canvas = tk.Canvas(self, width=900, height=900, cursor='crosshair', bd=5, relief='groove')
        canvas.grid(row=1, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="User Map")

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Star Map", command=lambda: root.show_frame('StarMap'))
        pagemenu.add_command(label="Astrolabe", command=lambda: root.show_frame('Astrolabe'))
        menubar.add_cascade(label='Pages', menu=pagemenu)

        return menubar


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
        menubar.add_command(label="Star Map")

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
