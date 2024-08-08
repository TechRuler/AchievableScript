from tkinter import *
from tkinter import ttk

class Palette(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.hover_color = ""
        self.normal_color = ""
        self.command_dict = {"Theme Change":self.theme_command}
        self.palette_button = Button(self, text='Code', width=50, border=0,command=self.palette_command)
        self.palette_button.pack(expand=True, padx=(2, 2), pady=(2, 2))
        self.palette_top = Toplevel()
        self.palette_top.overrideredirect(True)
        self.palette_list = Listbox(self.palette_top)
        self.palette_entry = Entry(self.palette_top)
        for i in self.command_dict:
            self.palette_list.insert('end',i)
        self.palette_entry.pack(fill='x')
        self.palette_list.pack(expand=True,fill='both')
        self.palette_top.withdraw()
    def theme_command(self):...
    def set_hover_color(self, hover_color, normal_color):
        self.hover_color = hover_color
        self.normal_color = normal_color
        self.palette_button.bind('<Enter>', lambda event=None: self.hover_or_not(color=self.hover_color))
        self.palette_button.bind('<Leave>', lambda event=None: self.hover_or_not(color=self.normal_color))
        
    def hover_or_not(self, color):
        self.palette_button.config(bg=color)
    def palette_command(self):
        x = self.palette_button.winfo_rootx()
        y = self.palette_button.winfo_rooty()
        width= self.palette_button.winfo_width()
        
        self.palette_top.deiconify()
        self.palette_top.geometry(f'{width}x200+{x}+{y}')
        
        # self.palette_list.lift()

    
if __name__ == "__main__":
    root = Tk()
    palette = Palette(root,bg='green')
    palette.pack(expand=True, )
    palette.set_hover_color('lightblue', 'white')  # Example colors
    root.mainloop()
