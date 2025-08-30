from core.settings import *
from core.main_menu import MainMenu
from core.custom_notebook import CustomNotebook

import tkinter as tk

class Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.main_window_config()

        self.surface()

        self.bind('<Control-n>', self.main_menu.menu_opt_cmd.new)
        self.bind('<Control-N>', self.main_menu.menu_opt_cmd.new)
        self.bind('<Control-o>', self.main_menu.menu_opt_cmd.open)
        self.bind('<Control-O>', self.main_menu.menu_opt_cmd.open)
        self.bind('<Control-s>', self.main_menu.menu_opt_cmd.save)
        self.bind('<Control-S>', self.main_menu.menu_opt_cmd.save)
        self.bind('<Control-Alt-s>', self.main_menu.menu_opt_cmd.save_as)
        self.bind('<Control-Alt-S>', self.main_menu.menu_opt_cmd.save_as)
        self.bind('<Control-F4>', self.main_menu.menu_opt_cmd.close)

    def main_window_config(self):
        self.title(MAIN_WINDOW_TITLE)
        self.geometry(MAIN_WINDOW_SIZE)

    def surface(self):
        self.custom_notebook = CustomNotebook(main_window = self)
        self.custom_notebook.pack(fill = 'both', expand = True)

        self.main_menu = MainMenu(nb_obj = self.custom_notebook)
        self.config(menu = self.main_menu)

        self.custom_notebook._new_tab()
