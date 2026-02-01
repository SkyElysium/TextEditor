import tkinter as tk

class LineNumberBar(tk.Text):
    def __init__(self, text_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_obj = text_obj

        self.config(width = 5, bg = '#e8e8e8', fg = '#8f8f8f', state = 'disabled',
                    cursor = 'arrow', bd = False, font = ('Consolas', 13))

        self.tag_config('center', justify = 'center')

    def scroll(self, *xy):
        self.text_obj.yview(*xy)
        self.yview(*xy)

    def scroll_selection(self):
        self.yview_moveto(self.text_obj.yview()[0])

    def wheel(self, event):
        self.text_obj.yview_scroll(int(-1 * (event.delta / 60)), 'units')
        self.yview_scroll(int(-1 * (event.delta / 60)), 'units')

        return 'break'

    def update_line_number(self):
        line_num = self.text_obj.index('end').split('.')[0]

        line_num_text = '\n'.join([str(num) for num in range(1, int(line_num))])

        # Can't get out of the line number bar
        max_width = 5

        if len(str(line_num)) > max_width:
            self.config(width = len(str(line_num)))
        else:
            self.config(width = 5)

        self.config(state = 'normal')

        self.delete('1.0', 'end')
        self.insert('1.0', line_num_text)

        self.config(state = 'disabled')

        self.yview_moveto(self.text_obj.yview()[0])

        self.tag_add('center', '1.0', 'end')
