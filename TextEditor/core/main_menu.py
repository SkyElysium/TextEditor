import tkinter as tk

class MainMenu(tk.Menu):
    def __init__(self, main_notebook):
        super().__init__()

        self.main_notebook = main_notebook

        # File
        self.file_option = tk.Menu(self, tearoff = False)

        file_option_dict = {
            'New'       : ('Ctrl+N', self.main_notebook.add_tab),
            'separator1': (),
            'Open'      : ('Ctrl+O', self.main_notebook.open),
            'Save'      : ('Ctrl+S', self.main_notebook.save),
            'Save As...': ('Ctrl+Alt+S', self.main_notebook.save_as),
            'separator2': (),
            'Close'     : ('Ctrl+F4', self.main_notebook.remove_tab)
        }

        self.create_child_options(self.file_option, file_option_dict)
        self.add_cascade(label = 'File', menu = self.file_option)

        # Edit
        self.edit_option = tk.Menu(self, tearoff = False)

        edit_option_dict = {
            'Undo'      : ('Ctrl+Z', lambda: self.main_notebook.get_tab()[1].undo()),
            'Redo'      : ('Ctrl+Shift+Z', lambda : self.main_notebook.get_tab()[1].redo()),
            'separator1': (),
            'Copy'      : ('Ctrl+C', lambda : self.main_notebook.get_tab()[1].copy()),
            'Cut'       : ('Ctrl+X', lambda : self.main_notebook.get_tab()[1].cut()),
            'Paste'     : ('Ctrl+V', lambda : self.main_notebook.get_tab()[1].paste()),
            'separator2': (),
            'Select All': ('Ctrl+A', lambda : self.main_notebook.get_tab()[1].select_all()),
        }

        self.create_child_options(self.edit_option, edit_option_dict)
        self.add_cascade(label = 'Edit', menu = self.edit_option)

    def create_child_options(self, master_option, option_dict):
        master_option_ = master_option
        option_dict_   = option_dict

        # The structure of option_info: (accelerator, command)
        for option_label, option_info in option_dict_.items():
            # Use separator<number> for separator
            if option_label.startswith('separator'):
                master_option_.add_separator()

                continue

            master_option_.add_command(label = option_label, accelerator = option_info[0], command = option_info[1])
