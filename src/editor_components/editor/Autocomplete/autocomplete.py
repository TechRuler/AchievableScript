import tkinter as tk
import jedi 
from src.gui.scrollbar import AutoScrollbar

class PopUp(tk.Frame):
    def __init__(self,*arg,**kwarg):
        tk.Frame.__init__(self,*arg,*kwarg)
        self.element_list = []
        self.toggle_color = "tomato"
        self.select_bgcolor = "grey"
        self.select_fgcolor = "white"
        self.default_bg = "grey15"
        self.default_fg = "white"
        self.add_command_for_element = None
        self.font = ("Consolas",10)
        self.select_element = None
        self.select_index = None
        self.config(cursor="hand2")
    def insert(self,text="",image=""):
        element = tk.Label(self,text=text,image=image,anchor="w",compound="left",bg=self.default_bg,fg=self.default_fg,font=self.font)
        element.pack(side="top",fill="x")
        element.bind("<Button-1>",lambda event=None,i=element:self.selection(i))
        element.bind("<Enter>",lambda event=None, i=element:self.hightlight_enter(i))
        element.bind("<Leave>",lambda event=None, i=element:self.hightlight_leave(i))
        self.element_list.append(element)
    
    
    def selection_get(self):
        text = self.select_element.cget("text")
        return text
    def delete(self):
        for i in self.element_list:
            i.pack_forget()
        self.element_list.clear()
    def select_set(self,index):
        for i,element in enumerate(self.element_list):
            if i == index:
                self.select(element)
    def selection(self,element):
        if self.select_element!=element:
            self.deselect(self.select_element)

        self.select(element)
        self.add_command_for_element()
            

    def hightlight_enter(self,element):
        if self.select_element != element:
            element.config(bg=self.toggle_color,fg=self.default_fg)

    def hightlight_leave(self,element):
        if self.select_element != element:
            element.config(bg=self.default_bg,fg=self.default_fg)
                
    def select(self,element):
        for i,_ in enumerate(self.element_list):
            if _ == element:
                self.select_index = i
        self.select_element = element
        element.config(bg=self.select_bgcolor,fg=self.select_fgcolor)

    def deselect(self,element):
        self.select_element = None
        self.select_index = None
        element.config(bg=self.default_bg,fg=self.default_fg)
    def configure(self,bg=None,fg=None,selectbackground=None,selectforeground=None,font=None,toggle_color=None):
        self.default_bg = bg 
        self.default_fg = fg 
        self.select_bgcolor = selectbackground
        self.select_fgcolor = selectforeground
        self.toggle_color = toggle_color
        self.font = font
        for element in self.element_list:
            element.config(bg=self.default_bg,fg=self.default_fg,font=self.font)
        


class Autocomplete(tk.Frame):
    def __init__(self, master, *arg, **kwarg):
        tk.Frame.__init__(self, master, *arg, **kwarg)
        self.master = master
        

        self.autocomplete_bool = False
        
        self.pop_up_y = 22
        self.pop_up = PopUp(self.master)
        self.pop_up.place_forget()

        self.calltip_popup = tk.Toplevel(self)
        self.calltip_popup.withdraw()
        self.calltip_popup.wm_overrideredirect(True)
        self.calltip_popup.wm_attributes("-topmost", 1)
        self.scrollbar = AutoScrollbar(self.calltip_popup, orient="vertical")
        self.calltip_label = tk.Text(self.calltip_popup, background="lightyellow", height=6, borderwidth=1, state="disabled", cursor="arrow", wrap="word",border=0, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.calltip_label.yview)
        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.calltip_label.grid(row=0,column=0,sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        

        self.detail_calltip_popup = tk.Toplevel(self)
        self.detail_calltip_popup.withdraw()
        self.detail_calltip_popup.wm_overrideredirect(True)
        self.detail_calltip_popup.wm_attributes("-topmost", 1)
        self.detail_scrollbar = AutoScrollbar(self.detail_calltip_popup, orient="vertical")
        self.detail_calltip_label = tk.Text(self.detail_calltip_popup, background="lightblue", height=10, width=40, borderwidth=0, state="disabled", cursor="arrow", wrap="word", yscrollcommand=self.detail_scrollbar.set)
        self.detail_scrollbar.config(command=self.detail_calltip_label.yview)
        self.detail_scrollbar.grid(row=0,column=1,sticky="ns")
        self.detail_calltip_label.grid(row=0,column=0,sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

    def change_y(self, y):
        self.pop_up_y = y

    def get_cursor_position(self):
        cursor_index = self.master.index(tk.INSERT)
        line, column = map(int, cursor_index.split('.'))
        return line, column

    def on_key_release(self, event=None):
        code = self.master.get("1.0", "end-1c")
        line, column = self.get_cursor_position()
        script = jedi.Script(code)

        try:
            completions = script.complete(line, column)
            self.autocomplete_function(completions)
            call_signatures = script.get_signatures(line, column)
            self.show_calltip(call_signatures)
        except Exception as e:
            self.hide_autocomplete()
            self.hide_calltip()
            self.hide_detail_calltip()

    def autocomplete_function(self, completions):
        word = self.master.get("insert -1c wordstart", "insert -1c wordend")
        line_text = self.master.get("insert linestart", "insert")
        bbox = self.master.bbox("insert")
        if bbox:
            x, y, _, _ = bbox
        if line_text.strip() == "" or line_text.lstrip().startswith("#"):
            self.hide_autocomplete()
        else:
            data = [i.name for i in completions]
            new_suggestion = len(data)

            if new_suggestion > 10:
                height = 185
            elif word == data[0]:
                self.hide_autocomplete()
            else:
                height = new_suggestion * 20

            if new_suggestion > 0:
                self.pop_up.place_configure(x=x, y=(y + self.pop_up_y), height=height, width=300)
                self.autocomplete_bool = True
                self.pop_up.delete()
                for i in data:
                    self.pop_up.insert(text=i)
                self.pop_up.select_set(0)
                self.update_detail_calltip()
                
            else:
                self.hide_autocomplete()

    def hide_autocomplete(self, event=None):
        self.pop_up.place_forget()
        self.autocomplete_bool = False
        self.hide_detail_calltip()

    def show_calltip(self, call_signatures):
        if call_signatures:
            calltip = call_signatures[0].docstring()
            bbox = self.master.bbox("insert")
            if bbox:
                x, y, width, height = bbox
                x += self.master.winfo_rootx()
                y += self.master.winfo_rooty()

                screen_height = self.winfo_screenheight()
                calltip_height = self.calltip_label.winfo_reqheight()

                if y + height + calltip_height + self.pop_up_y > screen_height:
                    y -= (calltip_height + self.pop_up_y + height)
                else:
                    y -= (calltip_height)
                if calltip_height <= 6:
                    print(calltip_height)
                    self.calltip_label.configure(height=calltip_height)
                else:
                    self.calltip_label.configure(height=6)

                self.calltip_label.configure(state="normal")
                self.calltip_label.delete("1.0", "end")
                self.calltip_label.insert("1.0", calltip)
                self.calltip_label.configure(state="disabled")
                self.calltip_popup.geometry(f"+{x}+{y}")
                self.calltip_popup.deiconify()
        else:
            self.hide_calltip()

    def hide_calltip(self):
        self.calltip_popup.withdraw()
    def update_detail_calltip(self, event=None):
        if self.autocomplete_bool:
            try:
                selected_item = self.pop_up.selection_get()
                script = jedi.Script(self.master.get("1.0", "end-1c"))
                completions = script.complete(*self.get_cursor_position())
                for comp in completions:
                    if comp.name == selected_item:
                        docstring = comp.docstring()
                        if docstring.strip():
                            self.detail_calltip_label.configure(state="normal")
                            self.detail_calltip_label.delete("1.0", "end")
                            self.detail_calltip_label.insert("1.0", docstring)
                            self.detail_calltip_label.configure(state="disabled")

                            bbox = self.master.bbox("insert")
                            if bbox:
                                x, y, width, height = bbox
                                x += self.master.winfo_rootx()
                                y += self.master.winfo_rooty() + 25

                                self.detail_calltip_popup.geometry(f"+{x + 300}+{y}")
                                self.detail_calltip_popup.deiconify()
                                
                        else:
                            self.hide_detail_calltip()
            except tk.TclError:
                pass

    def hide_detail_calltip(self):
        self.detail_calltip_popup.withdraw()


    def add_option_to_master(self, event=None):
        if self.autocomplete_bool:
            self.master.delete("insert -1c wordstart", "insert -1c wordend")
            self.master.insert("insert", self.pop_up.selection_get())
            self.hide_autocomplete()
            return 'break'


if __name__ == "__main__":
    def enter(event=None):
        if auto_complet.autocomplete_bool:
            auto_complet.add_option_to_master()
            auto_complet.place_forget()
        else:
            editor.insert("insert","\n")
            editor.see("insert")
        return "break"
    root = tk.Tk()

    editor = tk.Text(root,font=("Consolas",15),bg="grey20",fg="white",insertbackground="white") 
    editor.pack()
    auto_complet = Autocomplete(master=editor)

    auto_complet.pop_up.add_command_for_element = enter
    editor.bind("<KeyRelease>",auto_complet.on_key_release)
    editor.bind("<Return>",enter)



    root.mainloop()