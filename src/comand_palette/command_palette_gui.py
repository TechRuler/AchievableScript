from tkinter import *
from tkinter import ttk
from src.editor_components.editor.Autocomplete.custom_listbox import PopUp
class Palette(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.hover_color = ""
        self.normal_color = ""
        self.command_dict = {"Theme Change":self.theme_command,'text':(2,4)}
        self.palette_button = Button(self, text='Code', width=50, border=0,command=self.palette_command)
        self.palette_button.pack(expand=True, padx=(2, 2), pady=(2, 2))
        self.palette_top = Toplevel(self)
        self.palette_top.overrideredirect(True)
        self.palette_list = PopUp(self.palette_top)
        self.palette_entry = Entry(self.palette_top)
        
        self.palette_entry.pack(fill='x')
        self.default_list()
        self.palette_list.add_command_for_element = self.theme_command
        self.palette_top.withdraw()
    def default_list(self):
        for i in self.command_dict:
            self.palette_list.insert(text=i)
        self.palette_list.pack(expand=True,fill='both')
        
    def theme_command(self):
        self.palette_list.delete()
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
        self.palette_top.lift()
        self.palette_top.geometry(f'{width}x200+{x}+{y}')
        
        # self.palette_list.lift()
    def hide_palette(self):
        self.palette_top.withdraw()

    
if __name__ == "__main__":
    root = Tk()
    palette = Palette(root,bg='green')
    palette.pack(expand=True, )
    palette.set_hover_color('lightblue', 'white')  # Example colors
    root.mainloop()
