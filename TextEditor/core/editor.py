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

        # Format: the shortcuts and then method.
        binding_dict = {
            '<Control-n>'    : self.custom_notebook.add_tab,
            '<Control-o>'    : self.custom_notebook.open,
            '<Control-s>'    : self.custom_notebook.save,
            '<Control-Alt-s>': self.custom_notebook.save_as,
            '<Control-F4>'   : self.custom_notebook.remove_tab,
        }

        for shortcut, method in binding_dict.items():
            # If not the first letter each word is upper,
            # that means two kinds of a shortcut: upper and lower.
            if not shortcut.istitle(): self.bind(shortcut.title(), method)

            self.bind(shortcut, method)

    def surface(self):
        self.custom_notebook = CustomNotebook(main_window = self)
        self.custom_notebook.pack(fill = 'both', expand = True)

        self.main_menu = MainMenu(main_notebook = self.custom_notebook)
        self.config(menu = self.main_menu)

        self.custom_notebook.add_tab()
