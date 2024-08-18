import tkinter as tk
from tkinter import ttk
from src.editor_components.editor.Line_Number.line_number import LineNumber
from src.widgets.scrollbar import AutoScrollbar
from src.editor_components.editor.Autocomplete.autocomplete import Autocomplete
from src.editor_components.editor.minimap.minimap import TextPeer
from src.api.bind_control import EventManager, EventAPI
from src.editor_components.editor.syntax_highlighter.syntax_highligter import SyntaxHighlighter
import re

import keyword

class Editor(tk.Frame):
    def __init__(self, *arg, **kwarg):

        tk.Frame.__init__(self, *arg, **kwarg)
        
        self.indent_guides = []
        #self.indentation_guide_color = "spring green"
        self.style = ttk.Style()

        self.editor = tk.Text(self, font=("Monaco", 15), wrap="none",background="#1E1E3F")
        self.minimap = TextPeer(self.editor, font=("Monaco", 2), state="disable", wrap=None, border=0)

        self.syntax = SyntaxHighlighter(master=self.editor)
        self.syntax.configures()
        self.auto_complete = Autocomplete(master=self.editor)

        self.line = LineNumber(self, width=55)
        self.line.attach(self.editor)
        self.line.changefont(("Monaco", 15))

        self.vertical_scrollbar = AutoScrollbar(self, orient="vertical", command=self.muliple_scroll)
        self.horizontal_scrollbar = AutoScrollbar(self, orient="horizontal", command=self.editor.xview)

        self.editor.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.editor.configure(xscrollcommand=self.horizontal_scrollbar.set)

        self.line.grid(row=0, column=0, sticky="ns")
        self.editor.grid(row=0, column=1, sticky="nsew")
        self.minimap.grid(row=0, column=2, rowspan=2, sticky="ns")
        self.vertical_scrollbar.grid(row=0, column=3, rowspan=2, sticky="ns")
        self.horizontal_scrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.editor.bind("<KeyRelease>", lambda event=None: self.start_autocomplet())
        self.editor.bind("<Key>", lambda event=None: self.CurrentLineHighlight(widget=self.editor, delay=10))
        self.editor.bind("<Button-1>", lambda event=None: self.button_1_binding())
        self.editor.bind("<Double-Button-1>", lambda event=None: self.__forget_line_color())
        self.editor.bind("<B1-Motion>", lambda event=None: self.__forget_line_color())
        self.editor.bind("<MouseWheel>", lambda event=None: self.function_mouse_wheel())
        self.editor.bind("<Return>", self.autoindent)
        self.editor.bind("<Control-Return>", self.Enter_)
        self.editor.bind("<BackSpace>", lambda event=None: self.backspace())
        self.editor.bind("<(>", lambda event=None: self.autocomplete_brackets(bracket="("))
        self.editor.bind("<)>", lambda event=None: self.autocomplete_brackets(bracket=")"))
        self.editor.bind("<[>", lambda event=None: self.autocomplete_brackets(bracket="["))
        self.editor.bind("<]>", lambda event=None: self.autocomplete_brackets(bracket="]"))
        self.editor.bind("<{>", lambda event=None: self.autocomplete_brackets(bracket="{"))
        self.editor.bind("<}>", lambda event=None: self.autocomplete_brackets(bracket="}"))
        self.editor.bind("<'>", lambda event=None: self.autocomplete_strings(symbol="'"))
        self.editor.bind('<">', lambda event=None: self.autocomplete_strings(symbol='"'))
        self.editor.bind("<Tab>", lambda event=None: self.on_tab_click())
        self.editor.bind("<Control-m>", lambda event=None: self.do_comment())
        self.vertical_scrollbar.bind("<B1-Motion>", lambda event=None: self.__refresh_line_number())

        self.auto_complete.pop_up.add_command_for_element = self.add_by_click

    def function_mouse_wheel(self):
        self.minimap.yview_moveto(self.editor.yview()[0])
        self.__refresh_line_number()

    def muliple_scroll(self, *args):
        self.editor.yview(*args)
        self.minimap.yview(*args)

    def change_indent_color(self, color):
        self.indentation_guide_color = color 

    def add_by_click(self, event=None):
        if self.auto_complete.autocomplete_bool:
            self.auto_complete.add_option_to_master()
            self.auto_complete.place_forget()
            self.CurrentLineHighlight(widget=self.editor, delay=10)
        else:
            self.editor.insert("insert", "\n")
            self.editor.see("insert")
            self.CurrentLineHighlight(widget=self.editor, delay=10)
        return "break"

    def scrollbar_configure(self, scrollbar="grey", scroll_bg="white", active_scrollbar="white"):
        self.style.layout("Vertical.TScrollbar",
                 [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.style.layout("Horizontal.TScrollbar",
                 [('Horizontal.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ew'})])
        self.style.configure("Vertical.TScrollbar", background=scrollbar, bordercolor=scroll_bg, darkcolor=scrollbar, lightcolor=scrollbar, troughcolor=scroll_bg, arrowcolor=scroll_bg, gripcount=0)
        self.style.map("Vertical.TScrollbar", background=[('active', active_scrollbar)])
        self.style.configure("Horizontal.TScrollbar", background=scrollbar, bordercolor=scroll_bg, darkcolor=scroll_bg, lightcolor=scroll_bg, troughcolor=scroll_bg, arrowcolor=scroll_bg, gripcount=0)
        self.style.map("Horizontal.TScrollbar", background=[('active', active_scrollbar)])

    def setCurrentLinecolor(self, color):
        self.editor.tag_configure("CurrentLine", background=color)
        self.CurrentLineHighlight(widget=self.editor, delay=10)

    def start_autocomplet(self):
        self.auto_complete.on_key_release()
        self.__refresh_line_number()

    def button_1_binding(self):
        self.__refresh_line_number()
        self.auto_complete.hide_autocomplete()
        self.auto_complete.hide_calltip()
        self.CurrentLineHighlight(widget=self.editor, delay=10)

    def __refresh_line_number(self):
        self.line.redraw()
        self.__forget_line_color()
        self.__indent_guide()

    def __indent_guide(self):
        for item in self.indent_guides:
            self.editor.tag_delete(item)
        self.indent_guides.clear()
        for index in range(1, int(self.editor.index('end-1c').split('.')[0]) + 1):
            line = self.editor.get(f"{index}.0", f"{index}.end")
            space_number = re.search(r'(\s+)', line)
            if space_number is not None:
                space_number = space_number.span()[1]
                self.draw_guide(index, space_number)
            else:
                pass

    def draw_guide(self, index, indent_number):
        for count in range(1, indent_number + 1):
            if count % 4 == 0:
                tag_name = f"indent_{index}_{count // 4}"
                self.editor.tag_configure(tag_name, foreground=self.indentation_guide_color)
                self.editor.tag_add(tag_name, f"{index}.{count - 1}", f"{index}.{count}")
                self.indent_guides.append(tag_name)

    def __forget_line_color(self):
        self.editor.tag_delete("CurrentLine")

    def autoindent(self, event):
        current_line = self.editor.get("insert linestart", "insert")
        indent_match = re.match(r"^(\s+)", current_line)
        if indent_match:
            indent = indent_match.group(1)
            self.editor.insert("insert", "\n" + indent)
        else:
            self.editor.insert("insert", "\n")
        self.__refresh_line_number()
        return "break"

    def Enter_(self, event):
        try:
            word = self.auto_complete.autocomplete_word.strip()
            index = self.auto_complete.list_var.index(word)
        except:
            pass
        self.auto_complete.add_option_to_master()
        self.__refresh_line_number()
        index = self.editor.index("insert")
        index2 = "%s+1c" % index
        self.editor.tag_add("sel", index, index2)
        self.editor.mark_set("insert", index2)
        self.editor.see("insert")
        self.auto_complete.hide_autocomplete()
        self.auto_complete.hide_calltip()
        self.CurrentLineHighlight(widget=self.editor, delay=10)
        return "break"

    def backspace(self):
        self.auto_complete.on_key_backspace()
        self.__refresh_line_number()
        self.CurrentLineHighlight(widget=self.editor, delay=10)

    def autocomplete_brackets(self, bracket):
        pos = self.editor.index("insert")
        if bracket == "(":
            self.editor.insert(pos, "()")
        elif bracket == ")":
            pass
        elif bracket == "[":
            self.editor.insert(pos, "[]")
        elif bracket == "]":
            pass
        elif bracket == "{":
            self.editor.insert(pos, "{}")
        elif bracket == "}":
            pass
        self.editor.mark_set("insert", f"{pos}+1c")
        self.CurrentLineHighlight(widget=self.editor, delay=10)
        return "break"

    def autocomplete_strings(self, symbol):
        pos = self.editor.index("insert")
        self.editor.insert(pos, symbol * 2)
        self.editor.mark_set("insert", f"{pos}+1c")
        self.CurrentLineHighlight(widget=self.editor, delay=10)
        return "break"

    def on_tab_click(self):
        self.editor.insert("insert", " " * 4)
        self.CurrentLineHighlight(widget=self.editor, delay=10)
        self.__refresh_line_number()
        return "break"

    def do_comment(self):
        line_start = self.editor.index("insert linestart")
        line_end = self.editor.index("insert lineend")
        line_content = self.editor.get(line_start, line_end)
        if line_content.lstrip().startswith("#"):
            new_content = line_content.lstrip("#").strip()
        else:
            new_content = "# " + line_content
        self.editor.delete(line_start, line_end)
        self.editor.insert(line_start, new_content)
        self.CurrentLineHighlight(widget=self.editor, delay=10)
        self.__refresh_line_number()
        return "break"

    def CurrentLineHighlight(self, widget, delay=10):
        widget.tag_remove("CurrentLine", "1.0", "end")
        widget.tag_add("CurrentLine", "insert linestart", "insert lineend +1c")
        widget.after(delay, lambda: widget.tag_remove("CurrentLine", "1.0", "end"))

if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    editor.pack(fill="both", expand=True)
    editor.setCurrentLinecolor("#555555")  # Adjust the color as needed
    editor.scrollbar_configure()
    root.mainloop()
