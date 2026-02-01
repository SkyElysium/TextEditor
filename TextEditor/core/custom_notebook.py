from core.config import *
from core.line_number_bar import LineNumberBar

from tkinter import filedialog, messagebox

import clipboard
import os

import tkinter as tk
import tkinter.ttk as ttk

class CustomNotebook(ttk.Notebook):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.create_close_btn()

        self.bind('<Button-1>', self.on_press_close)
        self.bind('<B1-Motion>', self.move_sel_tab)
        self.bind('<<NotebookTabChanged>>', self.update_info_on_title)

    def create_close_btn(self):
        self.close_img = tk.PhotoImage(file = 'data/close.png')

        self.custom_style = ttk.Style()

        # Regard "close" as a command lets the tab destory
        self.custom_style.element_create('close', 'image', self.close_img)

        self.custom_style.layout('CustomNotebook', [('CustomNotebook.client', {'sticky': 'nswe'})])

        self.custom_style.layout('CustomNotebook.Tab', CUSTOM_NOTEBOOK_STYLE)

        self['style'] = 'CustomNotebook'

    def on_press_close(self, event):
        if self.identify(event.x, event.y) == 'close':
            self.remove_tab(tab_id = f'@{event.x}, {event.y}')

    def move_sel_tab(self, event):
        # Must be an exsit tab
        try:
            tab_index = self.index(f'@{event.x}, {event.y}')

            self.insert(tab_index, self.select())

        except: pass

    def update_info_on_title(self, event = None):
        tab = self.get_tab()[1]

        if not self.tabs() or not tab.path:
            self.main_window.title(MAIN_WINDOW_TITLE)
        else:
            self.main_window.title(f'{MAIN_WINDOW_TITLE} - {tab.path}')

    def add_tab(self, event = None, tab_name = 'Untitled'):
        tab = TextTab()

        self.add(tab, text = tab_name)

        return tab

    def remove_tab(self, event = None, tab_id = ''):
        if not self.tabs(): return

        if not tab_id:
            tab = self.select()
        else:
            tab = self.tabs()[self.index(tab_id)]

        self.forget(tab)

        self.update_info_on_title()

    def get_tab(self):
        if not self.tabs(): return '', None

        tab_id = self.select()
        tab = self.nametowidget(tab_id) # Get the "TextTab" class

        return tab_id, tab

    def open(self, event = None):
        path = filedialog.askopenfilename(title = 'Open in UTF-8',
                                          filetypes = [('Text File', '*.txt'), ('None Type', '*.*')])
        if not path: return

        tab = self.add_tab()
        tab.path = path

        self.add(tab, text = os.path.basename(path))

        with open(path, 'r', encoding = 'utf-8', buffering = 1024) as get_file_text:
            while True:
                try: block = get_file_text.read()

                except UnicodeDecodeError:
                    self.remove_tab(tab_id = tab)

                    messagebox.showerror(title = 'DecodeError', message = 'Not UTF-8 format')

                    break

                tab.text.insert('end', block)

                if not block: break

        tab.line_number_bar.update_line_number()

    def save(self, event = None, path = ''):
        tab = self.get_tab()[1]
        if not path:
            path = tab.path

        if not path and not tab.path:
            self.save_as()

            return

        with open(path, 'w', encoding = 'utf-8') as save_text_to_file:
            text = tab.text.get('1.0', 'end')

            save_text_to_file.write(text)

    def save_as(self, event = None):
        tab_id, tab = self.get_tab()

        path = filedialog.asksaveasfilename(title = 'Save As... in UTF-8',
                                            defaultextension = '.txt', filetypes = [('Text File', '*.txt'), ('None Type', '*.*')])
        if not path: return

        if tab.path:
            self.save(path = path)

            return

        tab.path = path

        self.save()

        self.update_info_on_title()
        self.tab(tab_id, text = os.path.basename(path))

class TextTab(tk.Frame):
    def __init__(self):
        super().__init__()

        self.path = ''

        self.place_widgets()
        self.right_click_menu()

        # Make sure only one function is called
        for event in ['<<Paste>>', '<<Copy>>', '<<Cut>>', '<<SelectAll>>', '<<Undo>>', '<<Redo>>']:
            for key in self.text.event_info(event):
                self.text.event_delete(event, key)

        self.text.bind('<Control-z>', self.undo)
        self.text.bind('<Control-Z>', self.undo)
        self.text.bind('<Control-Shift-z>', self.redo)
        self.text.bind('<Control-Shift-Z>', self.redo)
        self.text.bind('<Control-c>', self.copy)
        self.text.bind('<Control-C>', self.copy)
        self.text.bind('<Control-x>', self.cut)
        self.text.bind('<Control-X>', self.cut)
        self.text.bind('<Control-v>', self.paste)
        self.text.bind('<Control-V>', self.paste)
        self.text.bind('<Control-a>', self.select_all)
        self.text.bind('<Control-A>', self.select_all)

        self.text.bind('<Button-3>', lambda event: self.menu.post(event.x_root, event.y_root))

        # For the line number bar
        self.text.bind('<Any-KeyPress>', lambda event: self.after(1, self.line_number_bar.update_line_number))
        self.text.bind('<<Selection>>', lambda event: self.line_number_bar.scroll_selection())

        self.text.bind('<MouseWheel>', self.line_number_bar.wheel)
        self.line_number_bar.bind('<MouseWheel>', self.line_number_bar.wheel)

        self.line_number_bar.bind('<Button-1>', lambda event: 'break')

        self.line_number_bar.update_line_number()

    def place_widgets(self):
        self.edit_area = tk.Frame(self)
        self.edit_area.pack(fill = 'both', expand = True)

        self.text = tk.Text(self.edit_area, wrap = 'none', undo = True, bd = False, font = ('Consolas', 13))

        self.line_number_bar = LineNumberBar(master = self.edit_area, text_obj = self.text)

        self.line_number_bar.pack(fill = 'y', side = 'left')

        self.scrollbar = tk.Scrollbar(self.edit_area)
        self.scrollbar.pack(fill = 'y', side = 'right')

        self.text.pack(fill = 'both', expand = True)

        self.text['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command = self.line_number_bar.scroll)

    def right_click_menu(self):
        self.menu = tk.Menu(tearoff = False)

        self.menu.add_command(label = 'Copy', command = self.copy)
        self.menu.add_command(label = 'Cut', command = self.cut)
        self.menu.add_command(label = 'Paste', command = self.paste)

    def undo(self, event = None):
        self.text.event_generate('<<Undo>>')

        self.line_number_bar.update_line_number()

    def redo(self, event = None):
        self.text.event_generate('<<Redo>>')

        self.line_number_bar.update_line_number()

    def copy(self, event = None):
        try:
            sel_text = self.text.get('sel.first', 'sel.last')

            clipboard.copy(sel_text)

        except: pass

    def cut(self, event = None):
        try:
            self.copy()

            self.text.delete('sel.first', 'sel.last')

            self.line_number_bar.update_line_number()

        except: pass

    def paste(self, event = None):
        text_from_clipboard = clipboard.paste()

        try:
            self.text.delete('sel.first', 'sel.last')

        except: pass

        self.text.insert('insert', text_from_clipboard)

        self.line_number_bar.update_line_number()

    def select_all(self, event = None):
        self.text.event_generate('<<SelectAll>>')
