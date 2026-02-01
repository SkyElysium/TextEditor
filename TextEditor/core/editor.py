from core.config import *
from core.main_menu import MainMenu
from core.custom_notebook import CustomNotebook

import tkinter as tk

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(MAIN_WINDOW_TITLE)
        self.geometry(MAIN_WINDOW_SIZE)

        self.surface()

        self.bind('<Control-n>', self.custom_notebook.add_tab)
        self.bind('<Control-N>', self.custom_notebook.add_tab)
        self.bind('<Control-o>', self.custom_notebook.open)
        self.bind('<Control-O>', self.custom_notebook.open)
        self.bind('<Control-s>', self.custom_notebook.save)
        self.bind('<Control-S>', self.custom_notebook.save)
        self.bind('<Control-Alt-s>', self.custom_notebook.save_as)
        self.bind('<Control-Alt-S>', self.custom_notebook.save_as)
        self.bind('<Control-F4>', self.custom_notebook.remove_tab)

    def surface(self):
        self.custom_notebook = CustomNotebook(main_window = self)
        self.custom_notebook.pack(fill = 'both', expand = True)

        self.main_menu = MainMenu(nb_obj = self.custom_notebook)
        self.config(menu = self.main_menu)

        self.custom_notebook.add_tab()
