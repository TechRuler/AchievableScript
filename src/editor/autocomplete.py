import tkinter as tk
import keyword
import types
import pkgutil


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
    def __init__(self,master,*arg,**kwarg):
        tk.Frame.__init__(self,master,*arg,*kwarg)
        self.master = master
        self.autocomplete_bool = False
        self.data_for_autocomplete = keyword.kwlist + dir(__builtins__) + [name for name,_ in vars(types).items()if isinstance(getattr(types,name),type)]+[name for _,name,_ in pkgutil.iter_modules()]
        self.pop_up_y = 22
        
        self.pop_up = PopUp(self)
        self.pop_up.pack(fill="both",expand=True)
    
    def change_y(self,y):
        self.pop_up_y = y
    def autcomplete_function(self,event=None):
        word = self.master.get("insert -1c wordstart","insert -1c wordend")
        line_text = self.master.get("insert linestart","insert")
        bbox = self.master.bbox("insert")
        if bbox:
            x,y,_,_ = bbox
        if line_text.lstrip().startswith("#"):
            self.place_forget()
            self.autocomplete_bool = False
        else:
            data = [i for i in self.data_for_autocomplete if i.startswith(word)]
            new_suggestion = len(data)
            if new_suggestion > 10:
                height = 185
                self.place_configure(x=x,y=(y+self.pop_up_y),height=height,width=350)
                self.autocomplete_bool = True
            elif new_suggestion == 0:
                self.place_forget()
                self.autocomplete_bool = False
            else:
                height = new_suggestion*20
                self.place_configure(x=x,y=(y+self.pop_up_y),height=height,width=350)
                self.autocomplete_bool= True

            self.pop_up.delete()
            for i in data:
                    self.pop_up.insert(text=i)
            self.pop_up.select_set(0)
    def add_option_to_master(self,event=None):
        self.master.delete("insert -1c wordstart","insert -1c wordend")
        self.master.insert("insert",self.pop_up.selection_get())

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
    editor.bind("<KeyRelease>",auto_complet.autcomplete_function)
    editor.bind("<Return>",enter)



    root.mainloop()