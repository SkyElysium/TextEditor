import clipboard
from tkinter import Frame, Text, PhotoImage
from tkinter import SEL_FIRST, SEL_LAST, INSERT
from tkinter.ttk import Notebook, Style

from core.settings import *

class CustomNotebook(Notebook):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = main_window

        self.create_close_btn()

        self.bind('<Button-1>', self.on_press_close)

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
            # Get the tab was clicked element "close"
            tab_id = f'@{event.x}, {event.y}'

            tab = self.nametowidget(self.tabs()[self.index(tab_id)])

            tab.destroy()

        self.display_info_on_title()

    def display_info_on_title(self, event = None): # Should be None
        tab = self.nametowidget(self.select())

        if not self.tabs() or not tab.path:
            self.main_window.title(MAIN_WINDOW_TITLE)
        else:
            self.main_window.title(f'{MAIN_WINDOW_TITLE} - {tab.path}')

class TextTab(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Infomation about the tab
        self.path = ''

        self.place_widgets()

        # Delete all the keys of the events
        for event in self.text.event_info():
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

    def place_widgets(self):
        # "undo = True" means it allows to undo and redo
        self.text = Text(self, undo = True, bd = False, font = ('Consolas', 13))
        self.text.pack(fill = 'both', expand = True)

    def undo(self, event = None):
        self.text.event_generate('<<Undo>>')

    def redo(self, event = None):
        self.text.event_generate('<<Redo>>')

    def copy(self, event = None):
        try:
            sel_text = self.text.get(SEL_FIRST, SEL_LAST)

            clipboard.copy(sel_text)

        except: pass

    def cut(self, event = None):
        try:
            self.copy()

            self.text.delete(SEL_FIRST, SEL_LAST)

        except: pass

    def paste(self, event = None):
        text_from_clipboard = clipboard.paste()

        self.text.insert(INSERT, text_from_clipboard)

    def select_all(self, event = None):
        self.text.event_generate('<<SelectAll>>')
