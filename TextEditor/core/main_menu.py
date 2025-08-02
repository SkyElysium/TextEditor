import os
from tkinter import Menu, filedialog, messagebox

from core.custom_notebook import TextTab

class MainMenu(Menu):
    def __init__(self, nb_obj):
        super().__init__()

        self.menu_opt_cmd = MenuOptCmd(nb_obj)

        self.main_menu_config()

    def main_menu_config(self):
        self.file_opt = Menu(self, tearoff = False)

        self.file_opt.add_command(label = 'New', accelerator = 'Ctrl+N', command = self.menu_opt_cmd.new)
        self.file_opt.add_separator()
        self.file_opt.add_command(label = 'Open', accelerator = 'Ctrl+O', command = self.menu_opt_cmd.open)
        self.file_opt.add_command(label = 'Save', accelerator = 'Ctrl+S', command = self.menu_opt_cmd.save)
        self.file_opt.add_command(label = 'Save As...', accelerator = 'Ctrl+Alt+S', command = self.menu_opt_cmd.save_as)

        self.add_cascade(label = 'File', menu = self.file_opt)

        self.edit_opt = Menu(self, tearoff = False)

        self.edit_opt.add_command(label = 'Undo', accelerator = 'Ctrl+Z', command = self.menu_opt_cmd.undo)
        self.edit_opt.add_command(label = 'Redo', accelerator = 'Ctrl+Shift+Z', command = self.menu_opt_cmd.redo)
        self.edit_opt.add_separator()
        self.edit_opt.add_command(label = 'Copy', accelerator = 'Ctrl+C', command = self.menu_opt_cmd.copy)
        self.edit_opt.add_command(label = 'Cut', accelerator = 'Ctrl+X', command = self.menu_opt_cmd.cut)
        self.edit_opt.add_command(label = 'Paste', accelerator = 'Ctrl+V', command = self.menu_opt_cmd.paste)
        self.edit_opt.add_separator()
        self.edit_opt.add_command(label = 'Select All', accelerator = 'Ctrl+A', command = self.menu_opt_cmd.select_all)

        self.add_cascade(label = 'Edit', menu = self.edit_opt)

class MenuOptCmd:
    def __init__(self, nb_obj):
        self.nb_obj = nb_obj

    def new(self, event = None):
        self.nb_obj.add(TextTab(), text = 'Undefined')

    def open(self, event = None):
        path = filedialog.askopenfilename()
        if not path: return

        tab = TextTab()
        tab.path = path

        self.nb_obj.add(tab, text = os.path.basename(path))

        with open(path, 'r', encoding = 'utf-8', buffering = 1024) as get_file_text:
            while True:
                try: block = get_file_text.read()

                except UnicodeDecodeError as err:
                    self.nb_obj.forget(tab)

                    messagebox.showerror(title = type(err).__name__,
                                         message = 'Cannot decode the file in UTF-8 format')

                    break

                tab.text.insert('end', block)

                if not block: break

    def save(self, event = None):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select()) # Get the "TextTab" class

        if not tab.path:
            self.save_as()

            return

        with open(tab.path, 'w', encoding = 'utf-8') as save_text_to_file:
            text = tab.text.get('1.0', 'end')

            save_text_to_file.write(text)

    def save_as(self, event = None):
        if not self.nb_obj.tabs(): return

        tab_id = self.nb_obj.select()

        tab = self.nb_obj.nametowidget(tab_id)

        path = filedialog.asksaveasfilename()
        if not path: return

        tab.path = path

        self.save()

        self.nb_obj.display_info_on_title()
        self.nb_obj.tab(tab_id, text = os.path.basename(path))

    def undo(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.undo()

    def redo(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.redo()

    def copy(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.copy()

    def cut(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.cut()

    def paste(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.paste()

    def select_all(self):
        if not self.nb_obj.tabs(): return

        tab = self.nb_obj.nametowidget(self.nb_obj.select())

        tab.select_all()
