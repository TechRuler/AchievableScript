import tkinter as tk
from tkinter import font
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from pygments.token import Token
import re

class SyntaxHighlightingText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_tags()

        self.bind('<KeyRelease>', self._on_key_release)

    def configure_tags(self):
        # Configure tags based on a Pygments style
        style = get_style_by_name("default")
        for token, opts in style:
            tag_name = str(token)
            tag_opts = {}
            if 'color' in opts:
                tag_opts['foreground'] = f'#{opts["color"]}'
            if 'bgcolor' in opts:
                tag_opts['background'] = f'#{opts["bgcolor"]}'
            if 'bold' in opts:
                tag_opts['font'] = ('TkDefaultFont', 10, 'bold')
            if 'italic' in opts:
                tag_opts['font'] = ('TkDefaultFont', 10, 'italic')

            self.tag_configure(tag_name, **tag_opts)

    def _on_key_release(self, event=None):
        self.update_idletasks()
        self.highlight()

    def highlight(self):
        text = self.get("1.0", tk.END)
        self.remove_tags()

        tokens = lex(text, PythonLexer())
        for token, content in tokens:
            self.apply_tag(token, content)

    def apply_tag(self, token, content):
        start_idx = '1.0'
        while True:
            start_idx = self.search(re.escape(content), start_idx, stopindex=tk.END, nocase=True)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(content)}c"
            self.tag_add(str(token), start_idx, end_idx)
            start_idx = end_idx

    def remove_tags(self):
        for tag in self.tag_names():
            self.tag_remove(tag, "1.0", tk.END)

root = tk.Tk()
text = SyntaxHighlightingText(root, wrap="word", undo=True)
text.pack(expand=1, fill="both")
text.insert("1.0", "def example():\n    print('Hello, world!')\n")
root.mainloop()
