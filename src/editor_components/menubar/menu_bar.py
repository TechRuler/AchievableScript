import tkinter as tk
class MenuBar:
    """This is menubar for our editor"""
    def __init__(self, master,bg="grey15",fg="white",activebakground="tomato",font=("Consolas", 12)):
        self.master = master
        self.default_bg = bg 
        self.default_fg = fg 
        self.active_bg = activebakground
        self.font = font 
        self.menubutton_and_menu = {}
        self.menu_class = []
        self.selected_menu = None
        self.current_menu = None
        self.menu_bar = tk.Frame(self.master, height=25, bg=self.default_bg)
        self.menu_bar.pack(side="top", fill="x")

    def add_cascade(self, menu=None, text=""):
        """adding menu to menubar"""
        menubutton = tk.Label(self.menu_bar, text=text, font=self.font, bg=self.default_bg, fg=self.default_fg)
        menubutton.pack(side="left", fill="y", padx=(5,5), pady=(5,5))
        self.menubutton_and_menu[menubutton] = menu.menu if menu else None
        self.menu_class.append(menu)
        menubutton.bind("<Button-1>", lambda event=None, j=menubutton: self.__open_menu(j))
        menubutton.bind("<Enter>", lambda event=None, j=menubutton: self.__toggle_enter(j))
        menubutton.bind("<Leave>", lambda event=None, j=menubutton: self.__toggle_leave(j))

    def __open_menu(self, menubutton):
        menu = self.menubutton_and_menu[menubutton]
        if menu and menu.winfo_ismapped():
            menu.place_forget()
            for i in self.menu_class:
                i.reset()
            self.current_menu = None
            self.selected_menu = None
        elif menu:
            x = menubutton.winfo_rootx() - self.master.winfo_rootx()
            y = menubutton.winfo_rooty() + menubutton.winfo_height() - self.master.winfo_rooty()
            self.current_menu = menu
            self.selected_menu = menubutton
            menu.place_configure(x=x, y=y)
            menu.lift()
        self.change_color()

    def __toggle_enter(self, menubutton):
        for i in self.menu_class:
                i.reset()
        if self.current_menu != self.menubutton_and_menu[menubutton] and self.current_menu:
            self.current_menu.place_forget()
            self.__open_menu(menubutton)
        menubutton.config(bg=self.active_bg)

    def __toggle_leave(self, menubutton):
        if menubutton != self.selected_menu:
            menubutton.config(bg=self.default_bg)

    def change_color(self):
        for widget in self.menu_bar.winfo_children():
            if widget == self.selected_menu:
                widget.config(bg=self.active_bg)
            else:
                widget.config(bg=self.default_bg)
    def reset(self):
        self.current_menu = None
        self.selected_menu = None
        for widget in self.menu_bar.winfo_children():
            widget.config(bg=self.default_bg)