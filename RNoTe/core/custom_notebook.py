from __future__ import annotations
from typing import Optional, Tuple

import clipboard
import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog, messagebox
from pathlib import Path

from core.config import *
from core.line_number_bar import LineNumberBar


class CustomNotebook(ttk.Notebook):
    def __init__(self, master: tk.Misc) -> None:

        super().__init__(master)

        self.main_window = master

        # Create the closing button.
        self.close_image = tk.PhotoImage(file = 'data/close.png')

        self.custom_style = ttk.Style()

        # Regard "close" as a command that lets the tab destory.
        self.custom_style.element_create('close', 'image', self.close_image)

        self.custom_style.layout('CustomNotebook', [('CustomNotebook.client', {'sticky': 'nswe'})])
        self.custom_style.layout('CustomNotebook.Tab', CUSTOM_NOTEBOOK_STYLE)

        self['style'] = 'CustomNotebook'

        # Binding part
        self.bind('<Button-1>', self._on_pressing_close)
        self.bind('<B1-Motion>', self._move_selected_tab)

        self.bind('<<NotebookTabChanged>>', self._update_info_on_title)

    def _on_pressing_close(self, event: tk.Event) -> None:

        if self.identify(event.x, event.y) == 'close':
            self.remove_tab(tab_id = f'@{event.x}, {event.y}')

    def _move_selected_tab(self, event: tk.Event) -> None:

        # Use try-except to prevent the cursor from moving on nothing.
        try:
            tab_index = self.index(f'@{event.x}, {event.y}')

            self.insert(tab_index, self.select())
        except tk.TclError: pass

    def _update_info_on_title(self, event: Optional[tk.Event] = None) -> None:

        self.main_window.title(MAIN_WINDOW_TITLE)

        if not self.tabs(): return

        _, text_tab = self.get_tab()

        if text_tab.path:
            self.main_window.title(f'{MAIN_WINDOW_TITLE} - {text_tab.path}')

    def add_tab(self, event: Optional[tk.Event] = None, tab_name: str = '未命名') -> TextTab:

        text_tab = TextTab(self)
        text_tab.label = tab_name

        self.add(text_tab, text = tab_name)

        text_tab.line_number_bar.update_line_number()
        self.select(text_tab)

        return text_tab

    def remove_tab(self, event: Optional[tk.Event] = None, tab_id: str = '') -> None:

        # TabId for @x, y should be turned into ".!".
        tab = self.tabs()[self.index(tab_id)] if tab_id else self.select()

        self.forget(tab)
        self.nametowidget(tab).destroy()

        self.event_generate('<<NotebookTabClosed>>')

        self._update_info_on_title()

    def get_tab(self) -> Tuple[str, TextTab]:

        tab = self.select()
        text_tab = self.nametowidget(tab)

        return tab, text_tab

    def open_file(self, event: Optional[tk.Event] = None) -> None:

        path = filedialog.askopenfilename(
            title = '打开',
            filetypes = [('文本文档', '*.txt'), ('所有类型', '*.*')]
        )

        if not path: return

        try:
            file = Path(path)
            text = file.read_text(encoding = 'utf-8')

            text_tab = self.add_tab(tab_name = file.name)
            text_tab.text.insert('end', text)
        except UnicodeDecodeError:
            messagebox.showerror(
                title = '错误',
                message = '无法打开此文件，因为格式不兼容'
            )

            return

        text_tab.path = path
        text_tab.label = file.name

        text_tab.text.edit_modified(False)

        text_tab.line_number_bar.update_line_number()

    def save_file(self, event: Optional[tk.Event] = None, path: str = '') -> None:

        _, text_tab = self.get_tab()

        if not text_tab.path:
            self.save_file_as()
            if not text_tab.path: return

        text = text_tab.text.get('1.0', 'end-1c')  # No self adding "new line".

        file = Path(text_tab.path)
        file.write_text(text, encoding = 'utf-8')

        text_tab.text.edit_modified(False)

    def save_file_as(self, event: Optional[tk.Event] = None) -> None:

        path = filedialog.asksaveasfilename(
            title = '另存为...',
            defaultextension = '.txt',
            filetypes = [('文本文档', '*.txt'), ('所有类型', '*.*')]
        )

        if not path: return

        tab, text_tab = self.get_tab()

        if text_tab.path:
            # When the file has been, enter this fork.
            temp = text_tab.path
            text_tab.path = path

            self.save_file()

            text_tab.path = temp

            return

        text_tab.path = path
        text_tab.label = Path(path).name

        self.save_file()

        self.tab(tab, text = text_tab.label)


class TextTab(tk.Frame):
    def __init__(self, master) -> None:

        super().__init__(master)

        self.notebook = master

        # Tab config
        self.path = ''
        self.label = ''  # A variable displayed on tab, only used in "save_as".

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        # Wigets
        self.text = tk.Text(
            self,
            wrap = 'none',
            undo = True,
            bd = False,
            font = ('Consolas', 13),
            selectbackground = '#d3e9fc',
            selectforeground = 'black'
        )

        self.line_number_bar = LineNumberBar(self)
        self.line_number_bar.grid(row = 0, column = 0, rowspan = 2, sticky = 'ns')

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row = 0, column = 2, sticky = 'ns')

        self.x_scrollbar = tk.Scrollbar(self, orient = 'horizontal')
        self.x_scrollbar.grid(row = 1, column = 1, columnspan = 2, sticky = 'ew')

        self.text['xscrollcommand'] = self.x_scrollbar.set
        self.x_scrollbar.config(command = self.text.xview)

        self.text.grid(row = 0, column = 1, sticky = 'nsew')

        self.text['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command = self.line_number_bar.scroll)

        self.right_click_menu()

        # Reimplement these methods below inside the class.
        for event in [
            '<<Undo>>',
            '<<Redo>>',
            '<<Copy>>',
            '<<Cut>>',
            '<<Paste>>',
            '<<SelectAll>>'
        ]:
            for key in self.text.event_info(event):
                self.text.event_delete(event, key)

        # Binding part
        binding_dict = {
            '<Control-z>': self.undo,
            '<Control-Shift-z>': self.redo,
            '<Control-c>': self.copy,
            '<Control-x>': self.cut,
            '<Control-v>': self.paste,
            '<Control-a>': self.select_all
        }

        for shortcut, method in binding_dict.items():
            if not shortcut.istitle(): self.text.bind(shortcut.title(), method)

            self.text.bind(shortcut, method)

        self.text.bind('<Control-o>', self._ctrl_o)
        self.text.bind('<Button-3>', self._popup_menu)
        self.text.bind('<Configure>', self._is_out_of_text)
        self.text.bind('<<Modified>>', self._text_is_changed)

        # For the line number bar
        self.text.bind('<Any-KeyPress>', self._delay_to_update_line_number)
        self.text.bind('<Any-KeyPress>', self._delay_to_detect_text, add = '+')
        self.text.bind('<<Selection>>', self._selecting_scrolling)

        self.text.bind('<MouseWheel>', self.line_number_bar.wheel)
        self.line_number_bar.bind('<MouseWheel>', self.line_number_bar.wheel)

        self.line_number_bar.bind('<Button-1>', self._no_clicking_line_number_bar)

        # For highlighting the current line
        self.text.bind('<Button-1>', self._delay_to_highlight)

        self.line_number_bar.update_line_number()

    def right_click_menu(self) -> None:

        self.menu = tk.Menu(self, tearoff = False, activeforeground = 'black', activebackground = '#91c9f7')

        self.menu.add_command(label = '复制', accelerator = 'Ctrl+C', command = self.copy)
        self.menu.add_command(label = '剪切', accelerator = 'Ctrl+X', command = self.cut)
        self.menu.add_command(label = '粘贴', accelerator = 'Ctrl+V', command = self.paste)
        self.menu.add_separator()
        self.menu.add_command(label = '复制当前文件路径', command = self.copy_file_path)

    def _popup_menu(self, event: tk.Event) -> None:

        self.menu.post(event.x_root, event.y_root)

    def _delay_to_detect_text(self, event: tk.Event) -> None:

        self.after(1, self._is_out_of_text)

    def _delay_to_update_line_number(self, event: tk.Event) -> None:

        # Wait until entering successfully.
        self.after(1, self.line_number_bar.update_line_number)

    def _delay_to_highlight(self, event: tk.Event) -> None:

        # Wait until clicking successfully.
        self.after(1, self.line_number_bar.update_highlight_current_line)

    def _ctrl_o(self, event: tk.Event) -> None: return None  # Tkinter has bound ctrl+o inside "Text".

    def _is_out_of_text(self, event: Optional[tk.Event] = None) -> None:

        if self.text.xview() != (0.0, 1.0):
            self.x_scrollbar.grid()
        else:
            self.x_scrollbar.grid_remove()

    def _text_is_changed(self, event: tk.Event) -> None:

        if self.text.edit_modified():
            self.notebook.tab(self.notebook.get_tab()[0], text = f'*{self.label}')
        else:
            self.notebook.tab(self.notebook.get_tab()[0], text = self.label)

    def _no_clicking_line_number_bar(self, event: tk.Event) -> str: return 'break'

    def _selecting_scrolling(self, event: tk.Event) -> None:

        self.line_number_bar.scroll_when_selecting()

    def undo(self, event: Optional[tk.Event] = None) -> None:

        self.text.event_generate('<<Undo>>')

        self.line_number_bar.update_line_number()
        self._is_out_of_text()

    def redo(self, event: Optional[tk.Event] = None) -> None:

        self.text.event_generate('<<Redo>>')

        self.line_number_bar.update_line_number()
        self._is_out_of_text()

    def copy(self, event: Optional[tk.Event] = None) -> None:

        try:
            sel_text = self.text.get('sel.first', 'sel.last')

            clipboard.copy(sel_text)
        except tk.TclError: pass

    def cut(self, event: Optional[tk.Event] = None) -> None:

        try:
            self.copy()

            self.text.delete('sel.first', 'sel.last')

            self.line_number_bar.update_line_number()
            self._is_out_of_text()
        except tk.TclError: pass

    def paste(self, event: Optional[tk.Event] = None) -> None:

        text_from_clipboard = clipboard.paste().replace('\r\n', '\n')

        try:
            self.text.delete('sel.first', 'sel.last')
        except tk.TclError: pass

        self.text.insert('insert', text_from_clipboard)

        self.line_number_bar.update_line_number()
        self._is_out_of_text()

    def select_all(self, event: Optional[tk.Event] = None) -> None:

        self.text.event_generate('<<SelectAll>>')

    def copy_file_path(self) -> None:

        clipboard.copy(self.path)
