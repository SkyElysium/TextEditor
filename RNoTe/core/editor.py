import sys
import tkinter as tk
from tkinter import messagebox

from core.config import *
from core.main_menu import MainMenu
from core.custom_notebook import CustomNotebook


class Editor(tk.Tk):
    def __init__(self) -> None:

        super().__init__()

        self.title(MAIN_WINDOW_TITLE)
        self.geometry(MAIN_WINDOW_SIZE)

        self.iconphoto(False, tk.PhotoImage(file = 'data/icon.png'))

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

        self.protocol('WM_DELETE_WINDOW', self._exiting)

    def _exiting(self) -> None:
        saving_result = []

        for tab_id in self.custom_notebook.tabs():
            saving_result.append(self.custom_notebook.nametowidget(tab_id).text.edit_modified())

        if any(saving_result):
            reply = messagebox.askyesnocancel(
                title = '存在未保存的文件',
                message = '在关闭程序前手动保存所有文件？'
            )
            if reply: pass
            elif reply == False: sys.exit()
            else: pass
        else:
            sys.exit()
