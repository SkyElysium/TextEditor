import tkinter as tk

class MainMenu(tk.Menu):
    def __init__(self, nb_obj):
        super().__init__()

        self.nb_obj = nb_obj

        self.file_opt = tk.Menu(self, tearoff = False)

        self.file_opt.add_command(label = 'New', accelerator = 'Ctrl+N', command = self.nb_obj.add_tab)
        self.file_opt.add_separator()
        self.file_opt.add_command(label = 'Open', accelerator = 'Ctrl+O', command = self.nb_obj.open)
        self.file_opt.add_command(label = 'Save', accelerator = 'Ctrl+S', command = self.nb_obj.save)
        self.file_opt.add_command(label = 'Save As...', accelerator = 'Ctrl+Alt+S', command = self.nb_obj.save_as)
        self.file_opt.add_separator()
        self.file_opt.add_command(label = 'Close', accelerator = 'Ctrl+F4', command = self.nb_obj.remove_tab)

        self.add_cascade(label = 'File', menu = self.file_opt)

        self.edit_opt = tk.Menu(self, tearoff = False)

        self.edit_opt.add_command(label = 'Undo', accelerator = 'Ctrl+Z', command = lambda : self.nb_obj.get_tab()[1].undo())
        self.edit_opt.add_command(label = 'Redo', accelerator = 'Ctrl+Shift+Z', command = lambda : self.nb_obj.get_tab()[1].redo())
        self.edit_opt.add_separator()
        self.edit_opt.add_command(label = 'Copy', accelerator = 'Ctrl+C', command = lambda : self.nb_obj.get_tab()[1].copy())
        self.edit_opt.add_command(label = 'Cut', accelerator = 'Ctrl+X', command = lambda : self.nb_obj.get_tab()[1].cut())
        self.edit_opt.add_command(label = 'Paste', accelerator = 'Ctrl+V', command = lambda : self.nb_obj.get_tab()[1].paste())
        self.edit_opt.add_separator()
        self.edit_opt.add_command(label = 'Select All', accelerator = 'Ctrl+A', command = lambda : self.nb_obj.get_tab()[1].select_all())
        self.edit_opt.add_separator()
        self.edit_opt.add_command(label = 'Find', accelerator = 'Ctrl+F', command = '')

        self.add_cascade(label = 'Edit', menu = self.edit_opt)
