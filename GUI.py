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
            SecondPage
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


# class Menu:
#
#     def __init__(self, master, controller):
#         self.menubar = tk.Menu(master)
#         master.config(menu=self.menubar)
#         self.menubar.add_command(label='Start Page', command=lambda: controller.show_frame('SecondPage'))


class StartPage(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='blue')
        label = tk.Label(self, text='This is the start page')
        label.grid(row=0)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Go to page 2", command=lambda: root.show_frame('SecondPage'))
        return menubar


class SecondPage(tk.Frame):

    def __init__(self, location, controller):
        tk.Frame.__init__(self, location, bg='green')
        label = tk.Label(self, text='This is the second page')
        label.grid(row=0)

    def menubar(self, root):
        menubar = tk.Menu(root)
        menubar.add_command(label="Go to page 1", command=lambda: root.show_frame('StartPage'))
        return menubar


app = App()
app.title("Stoney Skies")
icon = tk.PhotoImage(file='icon.gif')
app.tk.call('wm', 'iconphoto', app._w, icon)
app.geometry('500x500+1400+400')
app.mainloop()
