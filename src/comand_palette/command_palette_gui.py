from tkinter import *
from tkinter import ttk

class Palette(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.hover_color = ""
        self.normal_color = ""
        self.palette_button = Button(self, text='Code', width=50, border=0)
        self.palette_button.pack(expand=True, padx=(2, 2), pady=(2, 2))
        
    def set_hover_color(self, hover_color, normal_color):
        self.hover_color = hover_color
        self.normal_color = normal_color
        self.palette_button.bind('<Enter>', lambda event=None: self.hover_or_not(color=self.hover_color))
        self.palette_button.bind('<Leave>', lambda event=None: self.hover_or_not(color=self.normal_color))
        
    def hover_or_not(self, color):
        self.palette_button.config(bg=color)
    
if __name__ == "__main__":
    root = Tk()
    palette = Palette(root)
    palette.pack(expand=True, fill=BOTH)
    palette.set_hover_color('lightblue', 'white')  # Example colors
    root.mainloop()
