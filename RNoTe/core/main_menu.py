import tkinter as tk


class MainMenu(tk.Menu):
    def __init__(self, master: tk.Misc) -> None:

        super().__init__(master)

        self.main_notebook = master.custom_notebook
        self.master = master

        self['postcommand'] = self._change_status_of_options

        # Options needed to check the status in "_change_status_of_options"
        self.file_option_checklist = ['关闭', '保存', '另存为...']
        self.edit_option_checklist = ['撤销', '重做', '复制', '剪切', '粘贴', '全选']

        # File
        self.file_option = tk.Menu(
            self,
            tearoff = False,
            activeforeground = 'black',
            activebackground = '#91c9f7'
        )

        self.file_option.add_command(
            label = '新建',
            accelerator = 'Ctrl+N',
            command = self.main_notebook.add_tab
        )
        self.file_option.add_separator()
        self.file_option.add_command(
            label = '打开',
            accelerator = 'Ctrl+O',
            command = self.main_notebook.open_file
        )
        self.file_option.add_command(
            label = '保存',
            accelerator = 'Ctrl+S',
            command = self.main_notebook.save_file
        )
        self.file_option.add_command(
            label = '另存为...',
            accelerator = 'Ctrl+Alt+S',
            command = self.main_notebook.save_file_as
        )
        self.file_option.add_separator()
        self.file_option.add_command(
            label = '关闭',
            accelerator = 'Ctrl+F4',
            command = self.main_notebook.remove_tab
        )
        self.file_option.add_separator()
        self.file_option.add_command(
            label = '退出',
            accelerator = 'Alt+F4',
            command = self.master._exiting
        )

        self.add_cascade(label = '文件', menu = self.file_option)

        # Edit
        self.edit_option = tk.Menu(
            self,
            tearoff = False,
            activeforeground = 'black',
            activebackground = '#91c9f7'
        )

        self.edit_option.add_command(
            label = '撤销',
            accelerator = 'Ctrl+Z',
            command = lambda : self.main_notebook.get_tab()[1].undo()
        )
        self.edit_option.add_command(
            label = '重做',
            accelerator = 'Ctrl+Shift+Z',
            command = lambda : self.main_notebook.get_tab()[1].redo()
        )
        self.edit_option.add_separator()
        self.edit_option.add_command(
            label = '复制',
            accelerator = 'Ctrl+C',
            command = lambda : self.main_notebook.get_tab()[1].copy()
        )
        self.edit_option.add_command(
            label = '剪切',
            accelerator = 'Ctrl+X',
            command = lambda : self.main_notebook.get_tab()[1].cut()
        )
        self.edit_option.add_command(
            label = '粘贴',
            accelerator = 'Ctrl+V',
            command = lambda : self.main_notebook.get_tab()[1].paste()
        )
        self.edit_option.add_separator()
        self.edit_option.add_command(
            label = '全选',
            accelerator = 'Ctrl+A',
            command = lambda : self.main_notebook.get_tab()[1].select_all()
        )

        self.add_cascade(label = '编辑', menu = self.edit_option)

    def _change_status_of_options(self) -> None:

        status = 'disabled' if not self.main_notebook.tabs() else 'normal'

        for each in self.file_option_checklist:
            self.file_option.entryconfig(each, state = status)
        for each in self.edit_option_checklist:
            self.edit_option.entryconfig(each, state = status)
