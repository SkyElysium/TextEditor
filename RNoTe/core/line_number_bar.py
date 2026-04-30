import tkinter as tk


class LineNumberBar(tk.Text):
    def __init__(self, master: tk.Misc) -> None:

        super().__init__(master)

        self.tab_text = self.master.text

        self.max_width = 5

        self.config(
            width = self.max_width,
            bg = '#e8e8e8',
            fg = '#8f8f8f',
            state = 'disabled',
            cursor = 'arrow',
            bd = False,
            font = ('Consolas', 13)
        )

        self.tag_config('center', justify = 'center')
        self.tag_config('current_line', foreground = '#3e3e3e')

    def scroll(self, *xy: tuple) -> None:

        self.tab_text.yview(*xy)
        self.yview(*xy)

    def update_line_number(self) -> None:
        line_num = self.tab_text.count('1.0', 'end', 'displaylines')[0]

        line_num_text = '\n'.join([str(num) for num in range(1, int(line_num) + 1)])

        # Can't get out of the line number bar
        if len(str(line_num)) > self.max_width:
            self.config(width = len(str(line_num)))
        else:
            self.config(width = self.max_width)

        self.config(state = 'normal')

        self.delete('1.0', 'end')
        self.insert('1.0', line_num_text)

        self.config(state = 'disabled')

        self.yview_moveto(self.tab_text.yview()[0])

        self.tag_add('center', '1.0', 'end')

        self.update_highlight_current_line()

    def update_highlight_current_line(self) -> None:

        self.tag_remove('current_line', '1.0', 'end')

        current_line = self.tab_text.count('1.0', 'insert', 'displaylines')

        if current_line is None: current_line = 1
        else: current_line = current_line[0] + 1

        start = f'{current_line}.0'
        end = f'{current_line}.end'

        self.tag_add('current_line', start, end)
