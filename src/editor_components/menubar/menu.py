import tkinter as tk
class MyMenu:
    def __init__(self, parent, font=("Consolas", 12), bg="grey15", fg="white", activebackground="tomato", activeforeground="white"):
        self.master = parent.master
        self.parent = parent
        self.font = font
        self.bg = bg
        self.fg = fg
        self.activebackground = activebackground
        self.activeforeground = activeforeground
        self.menubutton_and_menu = {}
        self.elements = []
        self.menu_list = []
        self.select = None
        self.sub_menu = None
        self.menu = tk.Frame(self.master, bg=self.bg)
    def add_command(self, label="", shortcut="", command=None):
        """Adding commands to menu dropdown"""
        element = tk.Frame(self.menu,bg=self.bg,cursor="hand2")
        element.pack(side="top", fill="x")
        label = tk.Label(element, text=label, anchor="w", bg=self.bg, fg=self.fg, font=self.font,padx=20,cursor="hand2")
        label.pack(side="left")
        shortcut_label = tk.Label(element, text=f"{shortcut}   ", bg=self.bg, fg=self.fg, font=self.font,cursor="hand2")
        shortcut_label.pack(side="right")

        self.elements.append(element)

        self.menubutton_and_menu[element] = None
        element.bind("<Enter>", lambda event=None, j=element: self.__open_menu_enter(j,None))
        
        if command:
            element.bind("<Button-1>", lambda event=None: self.run_command(command))
            label.bind("<Button-1>", lambda event=None: self.run_command(command))
            shortcut_label.bind("<Button-1>", lambda event=None: self.run_command(command))
    def run_command(self,command):
        self.hide()
        command()
    def hide(self):
        for i in self.menu_list:
            i.menu.place_forget()
        self.menu.place_forget()
        if self.bar is not None:
            self.bar.reset()

    def initilize_menubar(self,menubar):
        self.bar = menubar

    def add_separator(self):
        """Adding sparator to menu dropdown"""
        separator = tk.Frame(self.menu, height=1, bg=self.fg)
        separator.pack(side="top", fill="x", pady=2)

    def add_cascade(self, menu=None, label="",nested=None):
        element = tk.Frame(self.menu,bg=self.bg,cursor="hand2")
        element.pack(side="top", fill="x")
        label = tk.Label(element, text=label, anchor="w", bg=self.bg, fg=self.fg, font=self.font,padx=20,cursor="hand2")
        label.pack(side="left")
        shortcut_label = tk.Label(element, text=">", anchor="w", bg=self.bg, fg=self.fg, font=self.font,cursor="hand2")
        shortcut_label.pack(side="right")
        if nested is not None:
            self.menu_list += nested

        self.elements.append(element)
        self.menubutton_and_menu[element] = menu.menu if menu else None
        element.bind("<Enter>", lambda event=None, j=element,i=nested: self.__open_menu_enter(j,i))
        element.bind("<Leave>",lambda event=None,j=element:self.hide_sub_menu(j))
        
    def hide_sub_menu(self,element):
        menu = self.menubutton_and_menu[element]
        if menu.winfo_ismapped():
            menu.place_forget()
        self.__inner_reset(menu)
    
    def __open_menu_enter(self, element,width):
        """Open sub menu in menu dropdown"""

        if self.sub_menu:
            self.sub_menu.place_forget()
            for child in self.sub_menu.winfo_children():
                child.configure(bg=self.bg)
                for sub_child in child.winfo_children():
                    sub_child.configure(bg=self.bg,fg=self.fg)
        for remain_elements in self.elements:
            if remain_elements != element:
                remain_elements.configure(bg=self.bg)
                for sub_element in remain_elements.winfo_children():
                    sub_element.configure(bg=self.bg,fg=self.fg)

        self.select = element
        #for check
        # if width is not None:
            # for index,i in enumerate(width,start=1):
            #     if index == 2:
            # if len(width)==2:
            #     menu = width[1]
            #     print(menu.get_select().winfo_y())
            # else:
            #     menu = width[0]
            #     print(menu.get_select().winfo_y())

        element.configure(bg=self.activebackground)
        for sub_element in element.winfo_children():
            sub_element.configure(bg=self.activebackground, fg=self.activeforeground)


        new_menu = self.menubutton_and_menu[element]
        self.sub_menu = new_menu
        if new_menu:
            self.menu.update_idletasks()
            adding_value = 0
            adding_y = 0
            if width is not None:
                for i in width:
                    a = i.get_menu()
                    b = i.get_select().winfo_y()
                    adding_value += a.winfo_width()
                    adding_y += b
            x = element.winfo_x() + adding_value
            y = adding_y
            
            new_menu.place_configure(x=(x+5), y=(y+25))
            
            new_menu.bind("<Enter>", lambda event=None, j=new_menu, i=element,k=width: self.__hover_enter(j, i,k))

    def __hover_enter(self, new_menu, element,width):
        """when hover on sub menu it should visible"""
        adding_value = 0
        adding_y = 0
        if width is not None:
                for i in width:
                    a = i.get_menu()
                    b = i.get_select().winfo_y()
                    adding_value += a.winfo_width()
                    adding_y += b
        x = element.winfo_x() + adding_value
        y = adding_y
        new_menu.place_configure(x=(x+5), y=(y+25))
    def get_select(self):
        if self.select is not None:
            return self.select
    def get_menu(self):
        return self.menu
    def initilizing_last_menu(self,menus=None):
        if menus is not None:
            self.menu_list = menus
    def reset(self):
        self.select = None
        for remain_elements in self.elements:
            remain_elements.configure(bg=self.bg)
            for sub_element in remain_elements.winfo_children():
                sub_element.configure(bg=self.bg,fg=self.fg)
    def __inner_reset(self,menu):
        for remain_elements in menu.winfo_children():
            remain_elements.configure(bg=self.bg)
            for sub_element in remain_elements.winfo_children():
                sub_element.configure(bg=self.bg,fg=self.fg)
    