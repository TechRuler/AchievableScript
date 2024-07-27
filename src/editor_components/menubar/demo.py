import tkinter as tk
from menu_bar import MenuBar
from menu import MyMenu
def lets():
    print("code")
def main():
    root = tk.Tk()
    root.geometry("400x400+100+100")
    menu_bar = MenuBar(root)

    editor = tk.Text(root)
    editor.pack(expand=True, fill="both")

    file_menu = MyMenu(parent=menu_bar)
    file_menu.add_command(label="New File", command=lets)
    file_menu.add_command(label="Open File", command=lambda: print("Open File"))
    file_menu.add_command(label="Open Folder", command=lambda: print("Open Folder"))
    file_menu.initilize_menubar(menubar=menu_bar)
    
    
    theme_menu = MyMenu(parent=file_menu)
    theme_menu.add_command(label="Red", command=lambda: print("Red Theme"))
    theme_menu.initilize_menubar(menubar=menu_bar)

    new_theme = MyMenu(parent=theme_menu)
    new_theme.initilize_menubar(menubar=menu_bar)
    new_theme.add_command(label="Code", command=lets)
    new_theme.add_command(label="Code", command=lambda: print("Code Theme"))
    new_theme.initilizing_last_menu(menus=[file_menu,theme_menu])
    theme_menu.add_cascade(menu=new_theme, label="New",nested=[file_menu,theme_menu])
    theme_menu.add_command(label="Green", command=lambda: print("Green Theme"))
    theme_menu.add_command(label="Blue", command=lambda: print("Blue Theme"))

    file_menu.add_cascade(menu=theme_menu, label="Themes",nested=[file_menu])

    file_menu.add_separator()
    file_menu.add_command(label="Save File", command=lambda: print("Save File"))
    file_menu.add_command(label="Save As File", command=lambda: print("Save As File"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    edit_menu = MyMenu(parent=menu_bar)
    edit_menu.add_command(label="Undo", command=lambda: print("Undo"))
    edit_menu.add_command(label="Redo", command=lambda: print("Redo"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", command=lambda: print("Cut"))
    edit_menu.add_command(label="Copy", command=lambda: print("Copy"))
    edit_menu.add_command(label="Paste", command=lambda: print("Paste"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Search", command=lambda: print("Search"))
    edit_menu.add_command(label="Find", command=lambda: print("Find"))
    edit_menu.initilize_menubar(menubar=menu_bar)

    menu_bar.add_cascade(menu=file_menu, text="File")
    menu_bar.add_cascade(menu=edit_menu, text="Edit")

    

    

    root.mainloop()

if __name__ == "__main__":
    main()
