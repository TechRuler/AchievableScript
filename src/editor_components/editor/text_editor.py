import tkinter as tk 
from tkinter import ttk
from src.editor_components.editor.Line_Number.line_number import LineNumber
from src.gui.scrollbar import AutoScrollbar
from src.editor_components.editor.Autocomplete.autocomplete import Autocomplete
from src.editor_components.editor.syntax_highlighter.syntax_highligter import SyntaxHighlighter
from src.editor_components.editor.minimap.minimap import TextPeer
from src.api.bind_control import EventManager,EventAPI
import re 
class Editor(tk.Frame):
    def __init__(self,*arg,**kwarg):
        tk.Frame.__init__(self,*arg,**kwarg)
        self.indent_guides = []
        self.indentation_guide_color = "spring green"
        self.indentation_guide_height = 28
        self.indentation_guide_position = 35
        self.style = ttk.Style()
       
        self.editor = tk.Text(self,font=("Consolas",15),wrap="none")

        self.minimap = TextPeer(self.editor,font=("Consolas",2),state="disable",wrap=None,border=0)
        

        self.syntax = SyntaxHighlighter(master=self.editor)

        self.auto_complete = Autocomplete(master=self.editor)
        

        self.line = LineNumber(self,width=55)
        self.line.attach(self.editor)
        self.line.changefont(("Consolas",15))
        
        self.vertical_scrollbar = AutoScrollbar(self,orient="vertical",command=self.muliple_scroll)

        self.horizontal_scrollbar = AutoScrollbar(self,orient="horizontal",command=self.editor.xview)
       
        self.editor.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.editor.configure(xscrollcommand=self.horizontal_scrollbar.set)

        

        self.line.grid(row=0,column=0,sticky="ns")
        self.editor.grid(row=0,column=1,sticky="nsew")
        self.minimap.grid(row=0,column=2,rowspan=2,sticky="ns")
        self.vertical_scrollbar.grid(row=0,column=3,rowspan=2,sticky="ns")
        self.horizontal_scrollbar.grid(row=1,column=0,columnspan=2,sticky="ew")

        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        
        # event_manager = EventManager(default_interval=0.1,mode='throttle')
        # self.auto_complete.on_key_release()
        # self.__refresh_line_number()
        # self.draw_indentation_guides()
        # event_api = EventAPI(event_manager)
        # event_api.add_function(self.auto_complete.on_key_release,0.2)
        # event_api.add_function(lambda event=None:self.after(2,self.line.redraw),0.1)
        # event_api.add_function(lambda event=None:self.draw_indentation_guides(),priority=True)

        # event_api.bind_event(self.editor,"<KeyRelease>")

        self.editor.bind("<KeyRelease>",lambda event=None:self.start_autocomplet())
        self.editor.bind("<Key>",lambda event=None:self.CurrentLineHighlight(widget=self.editor,delay=10))
        self.editor.bind("<Button-1>",lambda event=None:self.button_1_binding())
        self.editor.bind("<Double-Button-1>",lambda event=None:self.__forget_line_color())
        self.editor.bind("<B1-Motion>",lambda event=None:self.__forget_line_color())
        self.editor.bind("<MouseWheel>",lambda event=None:self.function_mouse_wheel())
        self.editor.bind("<Return>",self.autoindent)
        self.editor.bind("<Control-Return>",self.Enter_)
        self.editor.bind("<BackSpace>",lambda event=None:self.backspace())
        self.editor.bind("<(>",lambda event=None:self.autocomplete_brackets(bracket="("))
        self.editor.bind("<)>",lambda event=None:self.autocomplete_brackets(bracket=")"))
        self.editor.bind("<[>",lambda event=None:self.autocomplete_brackets(bracket="["))
        self.editor.bind("<]>",lambda event=None:self.autocomplete_brackets(bracket="]"))
        self.editor.bind("<{>",lambda event=None:self.autocomplete_brackets(bracket="{"))
        self.editor.bind("<}>",lambda event=None:self.autocomplete_brackets(bracket="}"))
        self.editor.bind("<'>",lambda event=None:self.autocomplete_strings(symbol="'"))
        self.editor.bind('<">',lambda event=None:self.autocomplete_strings(symbol='"'))
        self.editor.bind("<Tab>",lambda event=None:self.on_tab_click())
        self.editor.bind("<Control-m>",lambda event=None:self.do_comment())
        self.vertical_scrollbar.bind("<B1-Motion>",lambda event=None:self.__refresh_line_number())
        
        self.auto_complete.pop_up.add_command_for_element = self.add_by_click
    def change_indentation_guide_height_position(self,height,position):
        self.indentation_guide_height = height
        self.indentation_guide_position = position
    def function_mouse_wheel(self):
        self.minimap.yview_moveto(self.editor.yview()[0])
        self.__refresh_line_number()
    def muliple_scroll(self,*args):
            self.editor.yview(*args)
            self.minimap.yview(*args)
    def change_indent_color(self,color):
        self.indentation_guide_color = color 
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

    def setCurrentLinecolor(self,color):
        self.editor.tag_configure("CurrentLine",background=color)
        self.CurrentLineHighlight(widget=self.editor,delay=10)

    def start_autocomplet(self):
        self.auto_complete.on_key_release()
        self.__refresh_line_number()
        # self.draw_indentation_guides()
    def button_1_binding(self):
        self.__refresh_line_number()
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        self.auto_complete.hide_autocomplete()
        self.auto_complete.hide_calltip()
    def __forget_line_color(self):
        self.editor.tag_remove("CurrentLine","1.0","end")

    def __refresh_line_number(self):
        self.after(2,self.line.redraw)
        # self.draw_indentation_guides()
        
        self.editor.after(1, self.draw_indentation_guides)

    def on_key_release(self, event=None):
        self.draw_indentation_guides()

    def on_scroll(self, event=None):
        self.editor.after(1, self.draw_indentation_guides)

    def draw_indentation_guides(self):
        # Clear existing guides
        for guide in self.indent_guides:
            guide.destroy()
        self.indent_guides.clear()
        
        lines = self.editor.get("1.0", "end-1c").split('\n')
        for line_number, line_text in enumerate(lines, start=1):
            match = re.match(r"^(\s+)", line_text)
            if match:
                indent_level = len(match.group(0))
                for i in range(4, indent_level + 1, 4):
                    self.draw_guide(line_number, i)

    def draw_guide(self, line_number, indent_level):
        bbox = self.editor.bbox(f"{line_number}.0 + {indent_level - 1} chars")
        if bbox:
            x = bbox[0]
            y = bbox[1]
            height = bbox[3] - bbox[1]
            guide_frame = tk.Frame(self.editor, bg=self.indentation_guide_color, width=2, height=self.indentation_guide_height)
            guide_frame.place(x=(x-self.indentation_guide_position), y=y)
            self.indent_guides.append(guide_frame)
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
    def Enter_(self,event=None):
        index = self.editor.index(tk.INSERT)
        index2 = "%s-%sc"%(index,1)
        word = self.editor.get(index2,index)
        line = self.editor.get("insert linestart", "insert lineend")

        match = re.match(r'^(\s+)', line)

        if word == ":":
            current_indent = len(match.group(0)) if match else 0
                
            
            new_indent = current_indent + 4
            
            self.editor.insert("insert", event.char + " "*new_indent)
        elif self.auto_complete.autocomplete_bool == True:
            self.button_1_binding()
            whitespace = match.group(0) if match else ""
            self.select_ = self.editor.get("insert","insert lineend")
            self.editor.insert("insert + 1line","") 
            self.editor.insert("insert",self.select_)
        
            self.editor.insert("insert", f"\n{whitespace}")
            self.editor.delete("insert","insert lineend")
        else:
            whitespace = match.group(0) if match else ""
            self.select_ = self.editor.get("insert","insert lineend")
            self.editor.insert("insert + 1line","")
            self.editor.insert("insert",self.select_)
        
            self.editor.insert("insert", f"\n{whitespace}")
            self.editor.delete("insert","insert lineend")
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        self.__refresh_line_number()

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

                    self.__refresh_line_number()
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
    def on_tab_click(self):
        self.editor.insert("insert"," "*4)
        self.CurrentLineHighlight(widget=self.editor,delay=10)
        return "break"
        
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
