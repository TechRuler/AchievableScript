from tkinter import ttk
class Theme:
    def __init__(self):
        self.style = ttk.Style()
    def set_theme(self,string='clam'):
        self.style.theme_use(string)
    def scrollbar_configure(self,scrollbar="grey",scroll_bg="white",active_scrollbar="white"):
        self.style.layout("Vertical.TScrollbar",
                 [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        
        self.style.layout("Horizontal.TScrollbar",
                 [('Horizontal.TScrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ew'})])

        self.style.configure("Vertical.TScrollbar",background=scrollbar,bordercolor=scroll_bg,darkcolor=scrollbar,lightcolor=scrollbar,troughcolor=scroll_bg,arrowcolor=scroll_bg,gripcount=0)
        self.style.map("Vertical.TScrollbar",background=[('active',active_scrollbar)])

        self.style.configure("Horizontal.TScrollbar",background=scrollbar,bordercolor=scroll_bg,darkcolor=scroll_bg,lightcolor=scroll_bg,troughcolor=scroll_bg,arrowcolor=scroll_bg,gripcount=0)
        self.style.map("Horizontal.TScrollbar",background=[('active',active_scrollbar)])
    def tree_configures(self,background="white",foreground="black",font=("Consolas",9),selected_bg="grey",selected_fg="white",border_color="white"):
        self.style.configure("Treeview",background=background,foreground=foreground,fieldbackground=background,bordercolor=border_color,highlightthickness=0, padding=0)
        self.style.map("Treeview",background=[("selected",selected_bg)],foreground=[("selected",selected_fg)])
    def buttons(self,font=("Consolas",12,'bold'),bg='blue',fg='white',activebackgrround='yellow',activeforeground='green',bordercolor='red'):
        

        self.style.configure('TButton',
                        font=font,
                        foreground=fg,
                        background=bg,
                        bordercolor=bordercolor,
                        relief="raised")
        
        self.style.map('TButton',
                  foreground=[('active', activeforeground)],
                  background=[('active', activebackgrround)])