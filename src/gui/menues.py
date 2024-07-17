import tkinter as tk

class Menu:
    def __init__(self, parent, font=("Consolas", 12), bg="grey15", fg="white", activebackground="tomato", activeforeground="white"):
        self.master = parent.master
        self.font = font
        self.bg = bg
        self.fg = fg
        self.activebackground = activebackground
        self.activeforeground = activeforeground
        self.menubutton_and_menu = {}
        self.x = []
        self.y = []
        self.select = None
        self.sub_menu = None
        self.toggle = False
        self.menu = tk.Frame(self.master, bg=self.bg)

    def add_command(self, label="", shortcut="", command=None):
        element = tk.Label(self.menu, text=label, anchor="w", bg=self.bg, fg=self.fg, font=self.font)
        element.pack(side="top", fill="x")
        self.menubutton_and_menu[element] = None
        element.bind("<Enter>", lambda event=None, j=element: self.__open_menu_enter(j))
        element.bind("<Leave>", lambda event=None, j=element: self.__open_menu_leave(j))
        if command:
            element.bind("<Button-1>", lambda event=None: command())

    def add_separator(self):
        separator = tk.Frame(self.menu, height=1, bg=self.fg)
        separator.pack(side="top", fill="x", pady=2)

    def add_cascade(self, menu=None, label=""):
        element = tk.Label(self.menu, text=f"{label}\t>", anchor="w", bg=self.bg, fg=self.fg, font=self.font)
        element.pack(side="top", fill="x")
        self.menubutton_and_menu[element] = menu.menu if menu else None
        element.bind("<Enter>", lambda event=None, j=element: self.__open_menu_enter(j))
        element.bind("<Leave>", lambda event=None, j=element: self.__open_menu_leave(j))

    def __open_menu_leave(self, element):
        element.configure(bg=self.bg, fg=self.fg)
        new_menu = self.menubutton_and_menu[element]
        if new_menu and self.toggle:
            new_menu.place_forget()
            self.toggle = False

    def __open_menu_enter(self, element):
        
        if self.sub_menu:
            self.sub_menu.place_forget()
        self.select = element
        element.configure(bg=self.activebackground, fg=self.activeforeground)
        new_menu = self.menubutton_and_menu[element]
        self.sub_menu = new_menu
        if new_menu and not self.toggle:
            x = element.winfo_x() + element.winfo_width()
            y = element.winfo_y()
            
            new_menu.place_configure(x=(x+5), y=(y+25))
            self.toggle = True
            new_menu.bind("<Enter>", lambda event=None, j=new_menu, i=element: self.__hover_enter(j, i))

    def __hover_enter(self, new_menu, element):
        x = element.winfo_x() + element.winfo_width()
        y = element.winfo_y()
        new_menu.place_configure(x=(x+5), y=(y+25))


class setMenuBar:
    def __init__(self, master):
        self.master = master
        self.default_bg = "grey15"
        self.default_fg = "white"
        self.active_bg = "tomato"
        self.menubutton_and_menu = {}
        self.selected_menu = None
        self.current_menu = None
        self.menu_bar = tk.Frame(self.master, height=25, bg=self.default_bg)
        self.menu_bar.pack(side="top", fill="x")

    def add_cascade(self, menu=None, text="", font=("Consolas", 12)):
        menubutton = tk.Label(self.menu_bar, text=text, font=font, bg=self.default_bg, fg=self.default_fg)
        menubutton.pack(side="left", fill="y", padx=(5, 5), pady=(5, 5))
        self.menubutton_and_menu[menubutton] = menu.menu if menu else None
        menubutton.bind("<Button-1>", lambda event=None, j=menubutton: self.__open_menu(j))
        menubutton.bind("<Enter>", lambda event=None, j=menubutton: self.__toggle_enter(j))
        menubutton.bind("<Leave>", lambda event=None, j=menubutton: self.__toggle_leave(j))

    def __open_menu(self, menubutton):
        menu = self.menubutton_and_menu[menubutton]
        if menu and menu.winfo_ismapped():
            menu.place_forget()
            self.current_menu = None
            self.selected_menu = None
        elif menu:
            x = menubutton.winfo_x()
            y = menubutton.winfo_y() + menubutton.winfo_height()
            self.current_menu = menu
            self.selected_menu = menubutton
            menu.place_configure(x=x, y=y)
            menu.lift()
        self.change_color()

    def __toggle_enter(self, menubutton):
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


def main():
    root = tk.Tk()
    main = tk.Menu
    root.geometry("400x400+100+100")
    menu_bar = setMenuBar(root)

    editor = tk.Text(root)
    editor.pack(expand=True, fill="both")

    file_menu = Menu(parent=menu_bar)
    file_menu.add_command(label="New File", command=lambda: print("New File"))
    file_menu.add_command(label="Open File", command=lambda: print("Open File"))
    file_menu.add_command(label="Open Folder", command=lambda: print("Open Folder"))

    theme_menu = Menu(parent=file_menu)
    theme_menu.add_command(label="Red", command=lambda: print("Red Theme"))

    new_theme = Menu(parent=theme_menu)
    new_theme.add_command(label="Code", command=lambda: print("Code Theme"))
    theme_menu.add_cascade(menu=new_theme, label="New")
    theme_menu.add_command(label="Green", command=lambda: print("Green Theme"))
    theme_menu.add_command(label="Blue", command=lambda: print("Blue Theme"))

    file_menu.add_cascade(menu=theme_menu, label="Themes")

    file_menu.add_separator()
    file_menu.add_command(label="Save File", command=lambda: print("Save File"))
    file_menu.add_command(label="Save As File", command=lambda: print("Save As File"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    edit_menu = Menu(parent=menu_bar)
    edit_menu.add_command(label="Undo", command=lambda: print("Undo"))
    edit_menu.add_command(label="Redo", command=lambda: print("Redo"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", command=lambda: print("Cut"))
    edit_menu.add_command(label="Copy", command=lambda: print("Copy"))
    edit_menu.add_command(label="Paste", command=lambda: print("Paste"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Search", command=lambda: print("Search"))
    edit_menu.add_command(label="Find", command=lambda: print("Find"))

    menu_bar.add_cascade(menu=file_menu, text="File")
    menu_bar.add_cascade(menu=edit_menu, text="Edit")

    root.mainloop()

if __name__ == "__main__":
    main()
