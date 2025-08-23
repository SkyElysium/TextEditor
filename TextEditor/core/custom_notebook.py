from tkinter import Frame, Text, Menu, Scrollbar, PhotoImage
from tkinter.ttk import Notebook, Style

from core.settings import *
from core.line_number_bar import LineNumberBar

import clipboard

class CustomNotebook(Notebook):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = main_window

        self.create_close_btn()

        self.bind('<Button-1>', self.on_press_close)

        self.bind('<B1-Motion>', self.move_sel_tab)

        self.bind('<<NotebookTabChanged>>', self.display_info_on_title)

    def create_close_btn(self):
        self.close_img = PhotoImage(file = 'data/close.png')

        self.custom_style = Style()

        # Regard "close" as a command lets the tab destory
        self.custom_style.element_create('close', 'image', self.close_img)

        self.custom_style.layout('CustomNotebook', [('CustomNotebook.client', {'sticky': 'nswe'})])

        self.custom_style.layout('CustomNotebook.Tab', CUSTOM_NOTEBOOK_STYLE)

        self['style'] = 'CustomNotebook'

    def on_press_close(self, event):
        if self.identify(event.x, event.y) == 'close':
            tab_id = f'@{event.x}, {event.y}'

            tab = self.nametowidget(self.tabs()[self.index(tab_id)])

            tab.destroy()

        self.display_info_on_title()

    def move_sel_tab(self, event):
        # Must be an exsit tab
        try:
            tab_index = self.index(f'@{event.x}, {event.y}')

            self.insert(tab_index, self.select())

        except: pass

    def display_info_on_title(self, event = None): # Be binded, so None
        tab = self.nametowidget(self.select())

        if not self.tabs() or not tab.path:
            self.main_window.title(MAIN_WINDOW_TITLE)
        else:
            self.main_window.title(f'{MAIN_WINDOW_TITLE} - {tab.path}')

class TextTab(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.text.bind('<<Selection>>', lambda event: self.after(1, self.line_number_bar.update_line_number))

        self.text.bind('<MouseWheel>', self.line_number_bar.wheel)
        self.line_number_bar.bind('<MouseWheel>', self.line_number_bar.wheel)

        self.line_number_bar.bind('<Button-1>', lambda event: 'break')

        self.line_number_bar.update_line_number()

    def place_widgets(self):
        self.text = Text(self, wrap = 'none', undo = True, bd = False, font = ('Consolas', 13))

        self.line_number_bar = LineNumberBar(master = self, text_obj = self.text)

        self.line_number_bar.pack(fill = 'y', side = 'left')

        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(fill = 'y', side = 'right')

        self.text.pack(fill = 'both', expand = True)

        self.text['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command = self.line_number_bar.scroll)

    def right_click_menu(self):
        self.menu = Menu(tearoff = False)

        self.menu.add_command(label = 'Copy', command = self.copy)
        self.menu.add_command(label = 'Cut', command = self.cut)
        self.menu.add_command(label = 'Paste', command = self.paste)

    def undo(self, event = None):
        self.text.event_generate('<<Undo>>')

    def redo(self, event = None):
        self.text.event_generate('<<Redo>>')

    def copy(self, event = None):
        try:
            sel_text = self.text.get('sel.first', 'sel.last')

            clipboard.copy(sel_text)

        except: pass

    def cut(self, event = None):
        try:
            self.copy()

            self.text.delete('sel.first', 'sel.last')

        except: pass

    def paste(self, event = None):
        text_from_clipboard = clipboard.paste()

        self.text.insert('insert', text_from_clipboard)

    def select_all(self, event = None):
        self.text.event_generate('<<SelectAll>>')

