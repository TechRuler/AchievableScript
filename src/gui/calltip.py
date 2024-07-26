import tkinter as tk 
class CallTip(tk.Frame):

    """This is the calltip for widget"""

    def __init__(self,master=None,text:str="",*arg,**kwarg):
        tk.Frame.__init__(self,*arg,**kwarg)
        self.text = text 
        self.master = master
        self.master.bind("<Enter>",lambda event:self.show(event))
        self.master.bind("<Leave>",lambda event=None:self.hide())
    def show(self,event):
        if self.text:
            x = event.x
            y = event.y
            self.place(x=x,y=y)
    def hide(self):
        self.place_forget()
    