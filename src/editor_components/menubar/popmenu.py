import tkinter as tk 
from src.editor_components.menubar.menu import MyMenu
class PopMenu:
    def __init__(self,master):
        self.master = master
        self.menu = None
        
    def setmenu(self,font=("Consolas", 12), bg="grey15", fg="white", activebackground="tomato", activeforeground="white"):
        return MyMenu(parent=self.master,font=font,bg=bg,fg=fg,activebackground=activebackground,activeforeground=activeforeground)
    def show(self,menu,event):
        if self.menu is not None:
            if self.menu.winfo_ismapped():
                self.menu.place_forget()
        self.menu = menu.menu
        self.master.bind("<Button-1>",lambda event=None:menu.hide())
        
        
        x,y = self.master.winfo_pointerx()-self.master.winfo_rootx(),self.master.winfo_pointery()-self.master.winfo_rooty()
        self.menu.place_configure(x=x,y=y)
    # def hide(self):
    #     self.menu.place_forget()