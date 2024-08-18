import tkinter as tk 
from tkinter import ttk
from src.widgets.scrollbar import AutoScrollbar
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

        self.canvas = tk.Canvas(self,bd=0, highlightthickness=0)

        self.scrollbar = AutoScrollbar(self,orient='vertical',command=self.canvas.yview,style="Custom.Vertical.TScrollbar")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.pop_up_frame = tk.Frame(self.canvas)

        self.pop_up_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.pop_up_frame, anchor="nw")

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(self.canvas_window,width=event.width)
        )

        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.canvas.grid(row=0,column=0,sticky="nsew")
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)


        
    # Bind mousewheel events
        self.pop_up_frame.bind("<Enter>", self._bind_mousewheel)
        self.pop_up_frame.bind("<Leave>", self._unbind_mousewheel)
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        current_y = self.canvas.yview()
        if event.delta > 0:  # Mouse wheel up
            if current_y[0] > 0:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.delta < 0:  # Mouse wheel down
            if current_y[1] < 1:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def insert(self,text="",image=""):
        element = tk.Label(self.pop_up_frame,text=text,image=image,anchor="w",compound="left",bg=self.default_bg,fg=self.default_fg,font=self.font)
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
        if self.select_element!=element and self.select_element:
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
        self.canvas.config(bg=self.default_bg)
        self.pop_up_frame.config(bg=self.default_bg)
        for element in self.element_list:
            element.config(bg=self.default_bg,fg=self.default_fg,font=self.font)
        

