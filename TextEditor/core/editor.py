import tkinter as tk

from core.config import *
from core.main_menu import MainMenu
from core.custom_notebook import CustomNotebook


class Editor(tk.Tk):
    def __init__(self) -> None:

        super().__init__()

        self.title(MAIN_WINDOW_TITLE)
        self.geometry(MAIN_WINDOW_SIZE)

        self.custom_notebook = CustomNotebook(self)
        self.custom_notebook.pack(fill = 'both', expand = True)

        self.main_menu = MainMenu(self)
        self.config(menu = self.main_menu)

        self.custom_notebook.add_tab()

        binding_dict = {
            '<Control-n>'    : self.custom_notebook.add_tab,
            '<Control-o>'    : self.custom_notebook.open_file,
            '<Control-s>'    : self.custom_notebook.save_file,
            '<Control-Alt-s>': self.custom_notebook.save_file_as,
            '<Control-F4>'   : self.custom_notebook.remove_tab
        }

        for shortcut, method in binding_dict.items():
            if not shortcut.istitle(): self.bind(shortcut.title(), method)

            self.bind(shortcut, method)
