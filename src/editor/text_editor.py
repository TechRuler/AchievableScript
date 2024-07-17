import tkinter as tk 
from tkinter import ttk
from src.editor.line_number import LineNumber
from src.gui.scrollbar import AutoScrollbar
from src.editor.autocomplete import Autocomplete
from src.editor.syntax_highligter import SyntaxHighlighter
import re 
class Editor(tk.Frame):
    def __init__(self,*arg,**kwarg):
        tk.Frame.__init__(self,*arg,**kwarg)
        self.style = ttk.Style()
       
        self.editor = tk.Text(self,font=("Consolas",15),wrap="none")

        self.syntax = SyntaxHighlighter(master=self.editor)

        self.auto_complete = Autocomplete(master=self.editor)
        

        self.line = LineNumber(self,width=55)
        self.line.attach(self.editor)
        self.line.changefont(("Consolas",15))
        
        self.vertical_scrollbar = AutoScrollbar(self,orient="vertical",command=self.editor.yview)

        self.horizontal_scrollbar = AutoScrollbar(self,orient="horizontal",command=self.editor.xview)
       
        self.editor.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.editor.configure(xscrollcommand=self.horizontal_scrollbar.set)

        

        self.line.grid(row=0,column=0,sticky="ns")
        self.editor.grid(row=0,column=1,sticky="nsew")
        self.vertical_scrollbar.grid(row=0,column=2,rowspan=2,sticky="ns")
        self.horizontal_scrollbar.grid(row=1,column=0,columnspan=2,sticky="ew")

        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        self.editor.bind("<KeyRelease>",lambda event=None:self.start_autocomplet())
        self.editor.bind("<Key>",lambda event=None:self.CurrentLineHighlight(widget=self.editor,delay=10))
        self.editor.bind("<Button-1>",lambda event=None:self.button_1_binding())
        self.editor.bind("<Double-Button-1>",lambda event=None:self.__forget_line_color())
        self.editor.bind("<B1-Motion>",lambda event=None:self.__forget_line_color())
        self.editor.bind("<MouseWheel>",lambda event=None:self.__refresh_line_number())
        self.editor.bind("<Return>",self.autoindent)
        self.editor.bind("<BackSpace>",lambda event=None:self.backspace())
        self.editor.bind("<(>",lambda event=None:self.autocomplete_brackets(bracket="("))
        self.editor.bind("<)>",lambda event=None:self.autocomplete_brackets(bracket=")"))
        self.editor.bind("<[>",lambda event=None:self.autocomplete_brackets(bracket="["))
        self.editor.bind("<]>",lambda event=None:self.autocomplete_brackets(bracket="]"))
        self.editor.bind("<{>",lambda event=None:self.autocomplete_brackets(bracket="{"))
        self.editor.bind("<}>",lambda event=None:self.autocomplete_brackets(bracket="}"))
        self.editor.bind("<'>",lambda event=None:self.autocomplete_strings(symbol="'"))
        self.editor.bind('<">',lambda event=None:self.autocomplete_strings(symbol='"'))
        self.editor.bind("<Control-m>",lambda event=None:self.do_comment())
        
        self.auto_complete.pop_up.add_command_for_element = self.add_by_click
    
    def add_by_click(self,event=None):
        if self.auto_complete.autocomplete_bool:
            self.auto_complete.add_option_to_master()
            self.auto_complete.place_forget()
            self.CurrentLineHighlight(widget=self.editor,delay=10)
        else:
            self.editor.insert("insert","\n")
            self.editor.see("insert")
            self.CurrentLineHighlight(widget=self.editor,delay=10)

        return "break"
    def scrollbar_configure(self,scrollbar="grey",scroll_bg="white"):
        self.style.configure("Vertical.TScrollbar",background=scrollbar,bordercolor=scroll_bg,darkcolor=scrollbar,lightcolor=scrollbar,troughcolor=scroll_bg,arrowcolor=scroll_bg,gripcount=0)
        self.style.map("Vertical.TScrollbar",background=[('active',scrollbar)])

        self.style.configure("Horizontal.TScrollbar",background=scrollbar,bordercolor=scroll_bg,darkcolor=scroll_bg,lightcolor=scroll_bg,troughcolor=scroll_bg,arrowcolor=scroll_bg,gripcount=0)
        self.style.map("Horizontal.TScrollbar",background=[('active',scrollbar)])

    def setCurrentLinecolor(self,color):
        self.editor.tag_configure("CurrentLine",background=color)
        self.CurrentLineHighlight(widget=self.editor,delay=10)

    def start_autocomplet(self):
        self.auto_complete.autcomplete_function()
        self.__refresh_line_number()
    def button_1_binding(self):
        self.__refresh_line_number()
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        self.auto_complete.pop_up.place_forget()
    def __forget_line_color(self):
        self.editor.tag_remove("CurrentLine","1.0","end")

    def __refresh_line_number(self):
        self.after(2,self.line.redraw)
    def autoindent(self,event):
        word = self.editor.get("insert -1c wordstart","insert -1c wordend")
        line = self.editor.get("insert linestart","insert lineend")
        match = re.match(r'^(\s+)',line)
        if word == ":":
            current_indent = len(match.group(0)) if match else 0 
            new_indent = current_indent + 4 
            self.editor.insert("insert",event.char + "\n" + " "*new_indent)
            self.CurrentLineHighlight(widget=self.editor,delay=10)
            self.__refresh_line_number()
        elif self.auto_complete.autocomplete_bool:
            self.auto_complete.add_option_to_master()
            self.CurrentLineHighlight(widget=self.editor,delay=10)
            self.__refresh_line_number()

        else:
            whitespace = match.group(0) if match else ""

            self.editor.insert("insert",f"\n{whitespace}")

            self.CurrentLineHighlight(widget=self.editor,delay=10)
            self.__refresh_line_number()

        self.editor.see("insert")

        return "break"
    def backspace(self):
        current_pos = self.editor.index("insert")
        line_text = self.editor.get("insert linestart","insert")
        match = re.match(r"^(\s+)",line_text)
        if line_text.isspace():
            if current_pos != "1.0":
                whitespace_len = len(match.group(0))if match else 0 
                if whitespace_len%4==0:
                    delet_char = min(whitespace_len,4)
                    line,char = current_pos.split(".")
                    new_char = int(char) - delet_char
                    new_char = max(new_char,0)

                    new_pos = f"{line}.{new_char}"

                    self.editor.delete(new_pos,"insert")

                    self.line.redraw()
                    self.CurrentLineHighlight(widget=self.editor,delay=10)
                    


                    return "break"
        self.line.redraw()
        self.CurrentLineHighlight(widget=self.editor,delay=10)
    def autocomplete_brackets(self,bracket):
        if bracket == "(":
            self.editor.mark_gravity("insert","left")
            self.editor.insert("insert",")")
            self.editor.mark_gravity("insert","right")
        elif bracket == "[":
            self.editor.mark_gravity("insert","left")
            self.editor.insert("insert","]")
            self.editor.mark_gravity("insert","right")
        elif bracket == "{":
            self.editor.mark_gravity("insert","left")
            self.editor.insert("insert","}")
            self.editor.mark_gravity("insert","right")
        elif bracket == ")":
            index = "%s+%sc"%("insert",1)
            if self.editor.get("insert",index) == ")":
                self.editor.delete("insert",index)
            else:
                pass
        elif bracket == "]":
            index = "%s+%sc"%("insert",1)
            if self.editor.get("insert",index) == "]":
                self.editor.delete("insert",index)
            else:
                pass
        elif bracket == "}":
            index = "%s+%sc"%("insert",1)
            if self.editor.get("insert",index) == "}":
                self.editor.delete("insert",index)
            else:
                pass
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        
    def autocomplete_strings(self,symbol):
        index1 = "%s+%sc"%("insert",1)
        index2 = "%s-%sc"%("insert",1)
        if symbol == '"' and self.editor.get("insert",index1) != '"':
            self.editor.mark_gravity("insert","left")
            self.editor.insert("insert",'"')
            self.editor.mark_gravity("insert","right")
        elif symbol == '"' and self.editor.get("insert",index1) == '"':
            self.editor.delete("insert",index1)
        elif symbol == "'" and self.editor.get("insert",index1) != "'":
            self.editor.mark_gravity("insert","left")
            self.editor.insert("insert","'")
            self.editor.mark_gravity("insert","right")
        elif symbol == "'" and self.editor.get("insert",index1) == "'":
            self.editor.delete("insert",index1)
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        
    def CurrentLineHighlight(self,widget,delay):
        def highlight():
            widget.tag_remove("CurrentLine","1.0","end")
            widget.tag_add("CurrentLine","insert linestart","insert lineend +1c")
        self.after(delay,highlight)
    def do_comment(self,event=None):
        myCount = tk.IntVar()
        pos = self.editor.search("# ","insert -1c linestart",regexp=False,count=myCount,stopindex="insert -1c lineend")
        if not pos:
            self.editor.insert("insert linestart","# ")
        else:
            last_pos = "%s+%sc"%(pos,2)
            self.editor.delete(pos,last_pos)
        self.CurrentLineHighlight(widget=self.editor,delay=10)
    
if __name__ == "__main__":
    root = tk.Tk()

    editor = Editor(root)
    editor.pack()

    

    editor.setCurrentLinecolor(color="#e1e1e1")



    root.mainloop()