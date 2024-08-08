from src.gui.window import Window
from src.editor_components.File_Exploeror.exploerer import FileManager
from src.gui.notebook import NoteBook
from src.editor_components.editor.text_editor import Editor
from src.editor_components.terminal.pythonshell import PythonShell
from src.editor_components.menubar.menu_bar import MenuBar
from src.editor_components.menubar.menu import MyMenu
from src.editor_components.menubar.popmenu import PopMenu
from src.themes.Theme import Theme
from src.comand_palette.command_palette_gui import Palette
from tkinter import*
from tkinter import ttk
from tkinter.filedialog import*
from PIL import ImageTk, Image
import os

class App(Window):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(1400,800,200,100)
        
        self.title("AchievableScript")
        self.icon = PhotoImage(file="assets/logo/editor.png")
        self.app_icon(image=self.icon)
        self.var()
        self.themes()
        self.setup()
        self.Key_automation() 
        self.config(bg=self.background)
    def Key_automation(self):
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<Control_L>", self.on_ctrl_press)
        self.bind("<Control_R>", self.on_ctrl_press)
        self.bind("<Alt_L>", self.on_alt_press)
        self.bind("<Alt_R>", self.on_alt_press)

        # self.explorer.tree.bind("<<TreeviewSelect>>", self.add_editor)
        self.explorer.tree.added_command.append(self.add_editor)
        self.explorer.command = self.just_show_side_bar
        self.bind("<Control-s>",self.saveas)
        self.editor.editor.bind("<Control-=>",lambda event=None:self.zoom_in())
        self.editor.editor.bind("<Control-minus>",lambda event=None:self.zoom_out())
        self.editor.editor.bind("<Shift-Return>",self.run_code)
       
        
    def var(self):
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.folder = ""
        self.file = ""
    def themes(self):
        # my theme
        self.background = "#1E1E3F"
        self.app_background = "#15152D"
        self.tab_bg = "#181832"
        self.autocomplete = "#181832"
        self.foreground = "#D6D6E3"
        self.currentline = "#2B2B4A"
        self.selection = "#37375E"
        self.keyword = "#f97583"
        self.builtin = "#82AAFF"
        self.comment = "#7F7FA8"
        self.string = "#C3E88D"
        self.definition = "#82AAFF"
        self.methods = "#82AAFF"
        self.number = "#FEB974"
        self.operator = "#FFB86C"
        self.circle_bracket = "#82AAFF"
        self.square_bracket = "#6BE6FD"
        self.curlly_bracket = "#82AAFF"
        self.parameter = "#FEB974"
        self.variable = "#FEB974"
        self.decorator = "#FFB86C"
        self.self_color = "#f97583"

        self.font = "Consolas"
        self.font_size = 14
        self.line_number_width = 55
        self.pop_up_coordinates = 22
    def setup(self):
        self.my_style = Theme()
        self.my_style.set_theme()
        self.my_style.buttons(font=self.font,bg=self.app_background,fg=self.foreground,activebackgrround=self.selection,activeforeground='white',bordercolor=self.background)
        self.Mainmenu = MenuBar(self,bg=self.app_background,fg=self.foreground,activebakground=self.selection,font=(self.font,12))
        
        
        self.add_configure(background=self.app_background,foreground=self.foreground,hover_minimise_button_color=self.selection,hover_resize_button_color=self.selection)
        self.side_bar = Frame(self,background=self.background)
        self.hid_button = Button(self.side_bar,text="<",background=self.background,foreground=self.foreground,border=0,font=("Consolas",10),command=self.hide_side)
        self.hid_button.pack(side="top",fill="x")
        self.side_bar.pack(side="left",fill="y")

        self.side_panel_window = PanedWindow(self,orient="horizontal",background=self.app_background)
        self.side_panel_window.pack(expand=True,fill="both")

        self.explorer = FileManager(self.side_panel_window,width=350,cursor="hand2")
        self.explorer.tree.color_config(default_bgcolor=self.app_background,default_fgcolor=self.foreground,selected_bgcolor=self.background,selected_fgcolor=self.foreground,hover_bgcolor=self.currentline,font_size=10)
        # self.explorer.pack(side="left",fill="y")
        self.explorer.pack_propagate(0)
        self.my_style.tree_configures(background=self.app_background,foreground=self.foreground,selected_bg=self.currentline,selected_fg=self.foreground,border_color=self.selection)
        self.explorer.config(bg=self.app_background)
        self.explorer.root_node_frame.config(bg=self.background)
        self.explorer.root_node.config(bg=self.background,fg=self.foreground,font=("Consolas",12,"bold"),)
        self.explorer.root_node_add_file.config(bg=self.background,fg=self.foreground,font=("Consolas",10))
        self.explorer.root_node_add_folder.config(bg=self.background,fg=self.foreground,font=("Consolas",10))
        self.explorer.root_node_add_reload.config(bg=self.background,fg=self.foreground,font=("Consolas",10))
        self.explorer.root_node_add_unfold.config(bg=self.background,fg=self.foreground,font=("Consolas",10))
        self.explorer.root_node_bind(normal=self.background,hover=self.currentline)
        self.explorer.root_node_frame2.config(bg=self.background)
        self.explorer.root_node_file_entry.config(bg=self.background,fg=self.foreground,insertbackground=self.foreground,font=("Consolas",12,"bold"))
        self.explorer.root_node_folder_entry.config(bg=self.background,fg=self.foreground,insertbackground=self.foreground,font=("Consolas",12,"bold"))
        self.explorer.file_creation_container.config(bg=self.background)
        self.explorer.folder_creation_container.config(bg=self.background)
        self.explorer.root_node_declaring_file.config(bg=self.background)
        self.explorer.root_node_declaring_folder.config(bg=self.background)



        self.editor_frame = PanedWindow(self,orient="vertical",background=self.app_background)
        # self.editor_frame.pack(side="right",fill=BOTH,expand=True)

        self.side_panel_window.add(self.explorer)
        self.side_panel_window.add(self.editor_frame)

        self.new_panel_index = IntVar(value=0)
        self.tab = NoteBook(self.editor_frame,height=550)
        self.tab.configure(background=self.background)
        # self.tab.pack(side="top",fill=BOTH,expand=True)
        self.tab.pack_propagate(0)

        self.tab.config_colors(tab_bg=self.tab_bg,tab_bar_color=self.tab_bg,tab_fg=self.foreground,selected_tab_color=self.background,frame_color=self.background,line_color="#0078D4")
        self.editor = Editor(self.tab)
        self.editor.editor.configure(font=(self.font,self.font_size),bg=self.background,fg=self.foreground,border=0,selectbackground=self.selection,insertbackground=self.foreground,undo=True)
        self.editor.line.configure(bg=self.background,border=0)
        self.my_style.scrollbar_configure(scrollbar=self.currentline,scroll_bg=self.background,active_scrollbar=self.selection)
        self.editor.line.changefg(self.foreground)
        self.editor.line.changefont((self.font,self.font_size))
        self.editor.auto_complete.pop_up.configure(bg=self.app_background,fg=self.foreground,selectbackground=self.selection,selectforeground=self.foreground,font=("Consolas",14),toggle_color=self.currentline)
        self.editor.auto_complete.calltip_label.config(bg=self.app_background,fg=self.foreground,font=("Consolas",10))
        self.editor.auto_complete.detail_calltip_label.config(bg=self.app_background,fg=self.foreground,font=("Consolas",10))
        self.editor.minimap.configure(bg=self.background,fg=self.foreground)
        
        self.editor.setCurrentLinecolor(self.currentline) 
        
        self.editor.change_indent_color(self.selection)
        self.editor.syntax.configures(method=self.methods,number=self.number,operator=self.operator,circle_brackets=self.circle_bracket,square_brackets=self.square_bracket,curlly_brackets=self.curlly_bracket,variable_in_parameter=self.parameter,variables=self.foreground,decorator=self.decorator,self_color=self.self_color,keyword=self.keyword,constant=self.methods,builtin=self.builtin,string=self.string,comment=self.comment,class_definition=self.definition,definition=self.methods)
        

        self.tab.add_tab(frame=self.editor,text="Untitled")

        


        self.output_frame = Frame(self.editor_frame)
        # self.output_frame.pack(side="top",fill=BOTH)
        self.output_frame_inner = Frame(self.output_frame,bg=self.app_background,border=0)
        self.output_frame_inner.pack(side="top",fill="x")
        self.output_label = Label(self.output_frame_inner,text="Terminal",font=("Consolas",15),bg=self.app_background,fg=self.foreground,border=0)
        self.output_label.pack(side="left",fill="y")
        self.output_close = Button(self.output_frame_inner,text=" ✕ ",font=("Consolas",15),bg=self.app_background,fg=self.foreground,border=0,command=self.hide_terminal)
        self.output_close.pack(side="right",fill="y")


        self.output_container = Frame(self.output_frame)
        self.output_container.pack(side="top",expand=True,fill=BOTH)

        self.output = PythonShell(self.output_container)
        self.output.pack(side="top",fill="both",expand=True)

        self.output_terminate = Button(self.output_frame_inner,text="Terminate",font=("Consolas",15),bg=self.app_background,fg=self.foreground,border=0,command=self.output.cancel_command)
        self.output_terminate.pack(side="right",fill="y")
        
        self.output.output.configure(font=("Consolas",15),bg=self.app_background,fg=self.foreground,border=0,selectbackground=self.selection,insertbackground=self.foreground)
        self.output.output_line.config(bg=self.app_background)

        self.output.output_line.changefg(self.foreground)
        self.output.output_line.changefont(("Consolas",15))

        # added frames to panelwindow

        self.editor_frame.add(self.tab)

        self.editor_frame.add(self.output_frame)

        self.panewindow_index = IntVar(value=1)
        
        
        
        

        self.output_container.rowconfigure(0,weight=1)
        self.output_container.columnconfigure(1,weight=1)


        


        Run = Menubutton(master=self.Mainmenu.menu_bar,text="▷",font=("Consolas",15),bg=self.app_background,fg=self.foreground,activebackground=self.currentline,activeforegroun=self.foreground) #command=lambda:self.run_code()
        Run.pack(side="right",fill="y",padx=(0,10))

        Run.bind("<Button-1>",lambda event=None:self.run_code())


       
        File_menu = MyMenu(parent=self.Mainmenu,font=(self.font,12),bg=self.app_background,fg=self.foreground,activebackground=self.selection,activeforeground=self.foreground)
        File_menu.add_command(label="New Text File",shortcut="Ctrl+N",command=self.new_file)
        File_menu.add_command(label="New File",shortcut="Ctrl+Alt+N")
        File_menu.add_command(label="New Window",shortcut="Ctrl+T")
        File_menu.add_separator()
        File_menu.add_command(label="Open File",shortcut="Ctrl+O",command=self.open_file)
        File_menu.add_command(label="Open Folder",shortcut="Ctrl+Alt+O",command=lambda:self.explorer.open_folder(self.folder))
        File_menu.add_command(label="Open Recent")
        File_menu.add_separator()
        File_menu.add_command(label="Add Folder to Workspace")
        File_menu.add_command(label="Save Workspace As")
        File_menu.add_command(label="Duplicate Workspace")
        File_menu.add_separator()
        File_menu.add_command(label="Save File",command=self.saveas)
        File_menu.add_command(label="Save As File",command=self.saveas)
        File_menu.add_separator()
        File_menu.add_command(label="Exit",command=self.close_app)
        File_menu.initilize_menubar(menubar=self.Mainmenu)

        Edit_menu = MyMenu(parent=self.Mainmenu,font=(self.font,12),bg=self.app_background,fg=self.foreground,activebackground=self.selection,activeforeground=self.foreground)
        Edit_menu.add_command(label="Undo",shortcut="Ctrl+Z")
        Edit_menu.add_command(label="Redo",shortcut="Ctrl+Y")
        Edit_menu.add_separator()
        Edit_menu.add_command(label="Cut",shortcut="Ctrl+X")
        Edit_menu.add_command(label="Copy",shortcut="Ctrl+C")
        Edit_menu.add_command(label="Paste",shortcut="Ctrl+V")
        Edit_menu.add_separator()
        Edit_menu.add_command(label="Find",shortcut="Ctrl+F")
        Edit_menu.add_command(label="Replace",shortcut="Ctrl+H")
        Edit_menu.add_separator()
        Edit_menu.add_command(label="Toggle Line Comment",shortcut="Ctrl+/")
        Edit_menu.initilize_menubar(menubar=self.Mainmenu)

        Help_menu = MyMenu(parent=self.Mainmenu,font=(self.font,12),bg=self.app_background,fg=self.foreground,activebackground=self.selection,activeforeground=self.foreground)
        Help_menu.add_command(label="Document")
        Help_menu.add_command(label="About")
        Help_menu.initilize_menubar(menubar=self.Mainmenu)


        

        
        Terminal_Menu = MyMenu(parent=self.Mainmenu,font=(self.font,12),bg=self.app_background,fg=self.foreground,activebackground=self.selection,activeforeground=self.foreground)
        Terminal_Menu.add_command(label="Terminal",command=self.hide_terminal)
        Terminal_Menu.initilize_menubar(menubar=self.Mainmenu)

        self.Mainmenu.add_cascade(menu=File_menu,text="File")
        self.Mainmenu.add_cascade(menu=Edit_menu,text="Edit")
        self.Mainmenu.add_cascade(menu=Terminal_Menu,text="Terminal")
        self.Mainmenu.add_cascade(menu=Help_menu,text="Help")
        
        self.do_popup = PopMenu(master=self)
        TreeviewMenu = self.do_popup.setmenu(bg=self.app_background,fg=self.foreground,activebackground=self.currentline,activeforeground=self.foreground,font=("Consolas",12))
        TreeviewMenu.add_command(label="Open to the slide")
        TreeviewMenu.add_command(label="Open with...")
        TreeviewMenu.add_command(label="Reveal in File Explorer")
        TreeviewMenu.add_command(label="Run File",command=lambda:self.run_code())
        TreeviewMenu.add_separator()
        TreeviewMenu.add_command(label="Rename",command=lambda:self.explorer.rename_item(self.background,self.foreground))
        TreeviewMenu.add_command(label="Delete",command=self.explorer.remove)
        TreeviewMenu.initilize_menubar(menubar=None)

        self.palette_adding_interace()

        self.menu_list = [File_menu,Edit_menu,Terminal_Menu,Help_menu]

        


        self.explorer.tree.added_one_more_command = lambda event,j=TreeviewMenu:self.do_popup.show(j,event)
        

    def palette_adding_interace(self):
        width = self.get_app_width()
        adjust = width/2
        print(width)
        print(adjust)
        self.my_palette = Palette(self.Mainmenu.menu_bar,bg=self.currentline)
        self.my_palette.palette_button.config(bg=self.app_background,fg=self.foreground,font=self.font,activebackground=self.selection,activeforeground='white')
        self.my_palette.set_hover_color(hover_color=self.selection,normal_color=self.app_background)
        self.my_palette.pack(side='left',expand=True)
    def hideing(self):
        for i in self.menu_list:
            i.menu.place_forget()
    def zoom_in(self):
        current_size = self.editor.editor.cget("font").split()[1]
        self.font_size = int(current_size) + 2  # Increase font size by 2 points
        self.font = self.editor.editor.cget("font").split()[0]
        self.editor.editor.configure(font=(self.font, self.font_size))
        self.line_number_width += (int(self.line_number_width) + 1)/20
        self.pop_up_coordinates = (int(self.pop_up_coordinates)+3)
        self.editor.auto_complete.change_y(self.pop_up_coordinates)
        self.editor.line.configure(width=self.line_number_width)
        self.editor.line.changefont((self.font,self.font_size))
        height = self.editor.indentation_guide_height + 4
        position = self.editor.indentation_guide_position + 4
        self.editor.change_indentation_guide_height_position(height=height,position=position)
    
    def zoom_out(self):
        current_size = self.editor.editor.cget("font").split()[1]
        self.font_size = int(current_size) - 2  # Increase font size by 2 points
        self.font = self.editor.editor.cget("font").split()[0]
        self.editor.editor.configure(font=(self.font, self.font_size))
        self.line_number_width -= (int(self.line_number_width) - 1)/20
        self.pop_up_coordinates = (int(self.pop_up_coordinates)-3)
        self.editor.auto_complete.change_y(self.pop_up_coordinates)
        self.editor.line.configure(width=self.line_number_width)
        self.editor.line.changefont((self.font,self.font_size))
        height = self.editor.indentation_guide_height - 4
        position = self.editor.indentation_guide_position - 4
        self.editor.change_indentation_guide_height_position(height=height,position=position)
        
    def button_show(self):
        if self.folder:
            self.root_node_add_unfold.pack(side="right")
            self.root_node_add_reload.pack(side="right")
            self.root_node_add_folder.pack(side="right")
            self.root_node_add_file.pack(side="right")
    def button_hide(self):
        if self.folder:
            self.root_node_add_unfold.pack_forget()
            self.root_node_add_reload.pack_forget()
            self.root_node_add_folder.pack_forget()
            self.root_node_add_file.pack_forget()
    
    def hide_terminal(self):
        if self.panewindow_index.get() == -1:
            self.editor_frame.add(self.output_frame)
            self.panewindow_index.set(1)
        else:
            self.editor_frame.forget(self.output_frame)
            self.panewindow_index.set(-1)
    def hide_side(self):
        if self.new_panel_index.get() == -1:
            self.side_panel_window.add(self.explorer)
            self.side_panel_window.forget(self.editor_frame)
            self.side_panel_window.add(self.editor_frame)
            self.hid_button.config(text=">")
            self.new_panel_index.set(0)
        else:
            # self.explorer.pack(side="left",fill="y")
            self.side_panel_window.forget(self.explorer)
            self.new_panel_index.set(-1)
            self.hid_button.config(text="<")
    def just_show_side_bar(self):
        if not self.explorer.winfo_ismapped():
            self.explorer.pack(side="left",fill="y")
            self.hid_button.config(text="<")
    def run_code(self,event=None):
        
        self.output.run_code(self.tab.file)
        if self.panewindow_index.get() == -1:
            self.editor_frame.add(self.output_frame)
            self.panewindow_index.set(1)
        
        return "break"
    def new_file(self):
        self.file = ""
        self.add_editor_to_tab(file=self.file,name="New File",image="")
        self.title("MyEditor")
    def open_file(self):
        self.file = askopenfilename()
        name = os.path.basename(self.file)
        if name.endswith(".py"):
                
                self.add_python_file(self.file,name)
                
        elif name.endswith(".txt"):
                
                self.editor = self.add_editor_to_tab(self.file,name,self.explorer.image_text)
    
    def saveas(self,event=None):
        if self.tab.file != "":
            for existing_frame, associated_tab in self.tab.tabs.items():
                        if self.tab.file_paths[existing_frame] == self.tab.file:
                            for child in existing_frame.winfo_children(): 
                                if isinstance(child,Text):
                                    content = child.get("1.0","end")
                                    with open(self.tab.file_paths[existing_frame],"w",encoding='utf-8') as f:
                                        f.write(content)
            self.output.output.insert("end",f"{self.tab.file}--saved\n","saved")
            self.output.output.see("end")
           
        else:
            save_path = asksaveasfilename()
            if save_path:
                self.tab.file = save_path
                print(self.tab.file)
                name = os.path.basename(save_path)
                selected_tab = self.tab.selection()
                existing_frame = self.tab.frames[selected_tab]
                self.tab.file_paths[existing_frame] = self.tab.file
                if name.endswith(".py"):
                            image = selected_tab.winfo_children()[1]
                            label =  selected_tab.winfo_children()[2]
                            image.config(image=self.explorer.image_python)
                            label.config(text=name)
                for child in existing_frame.winfo_children():
                            if isinstance(child,Text):
                                content = child.get("1.0","end")
                                with open(self.tab.file_paths[existing_frame],"w",encoding='utf-8') as f:
                                    f.write(content)
    def add_editor(self,event=None):
        # global side_bar, file, tab
        item = self.explorer.tree.selection()
        name = self.explorer.tree.item(item, "text")
        file = self.explorer.tree.item(item, "values")
        if os.path.isfile(file):
            if name.endswith(".py"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.add_python_file(file,name)
                
                # self.editor.editor.bind("<KeyRelease>",lambda event=None:self.editor.highlight_syntax(widget=self.editor.editor))
            elif name.endswith(".txt"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.editor = self.add_editor_to_tab(file,name,self.explorer.image_text)
                self.editor.editor.unbind("<KeyRelease>")
            elif name.endswith(".json"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.editor = self.add_editor_to_tab(file,name,self.explorer.image_text)
                self.editor.editor.unbind("<KeyRelease>")
            elif name.endswith(".html"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.editor = self.add_editor_to_tab(file,name,self.explorer.image_html)
                self.editor.editor.unbind("<KeyRelease>")
            elif name.endswith(".css"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.editor = self.add_editor_to_tab(file,name,self.explorer.image_css)
                self.editor.editor.unbind("<KeyRelease>")
            elif name.endswith(".js"):
                # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                
                self.editor = self.add_editor_to_tab(file,name,self.explorer.image_js)
                self.editor.editor.unbind("<KeyRelease>")
            elif name.endswith(".png") or name.endswith(".jpg") or name.endswith(".PNG") or name.endswith(".JPG") or name.endswith(".jpeg") or name.endswith(".JPEG"):
                 # Check if tab already exists for this file
                for existing_frame, associated_tab in self.tab.tabs.items():
                    if self.tab.file_paths[existing_frame] == file:
                        self.tab.tab_click(None, associated_tab)
                        return
                self.add_image_to_tab(file,name,self.explorer.image_image)
    def add_python_file(self,file,name):
        self.editor=self.add_editor_to_tab(file,name,self.explorer.image_python)
        self.editor.syntax.configures(method=self.methods,number=self.number,operator=self.operator,circle_brackets=self.circle_bracket,square_brackets=self.square_bracket,curlly_brackets=self.curlly_bracket,variable_in_parameter=self.parameter,variables=self.foreground,decorator=self.decorator,self_color=self.self_color,keyword=self.keyword,constant=self.methods,builtin=self.builtin,string=self.string,comment=self.comment,class_definition=self.definition,definition=self.methods)
        self.editor.auto_complete.calltip_label.config(bg=self.app_background,fg=self.foreground,font=("Consolas",10))
        self.editor.auto_complete.detail_calltip_label.config(bg=self.app_background,fg=self.foreground,font=("Consolas",10))
        self.editor.editor.bind("<Shift-Return>",self.run_code)
    def add_editor_to_tab(self,file,name,image):
        self.editor = Editor(self.tab)
        self.tab.add_tab(frame=self.editor, text=name, image=image, file_path=file)
        self.editor.setCurrentLinecolor(self.currentline)
        self.editor.editor.configure(font=(self.font,self.font_size),bg=self.background,fg=self.foreground,border=0,selectbackground=self.selection,insertbackground=self.foreground,undo=True)
        self.editor.line.configure(bg=self.background,border=0)
        self.editor.line.changefg(self.foreground)
        self.editor.line.changefont((self.font,self.font_size))
        self.my_style.scrollbar_configure(scrollbar=self.currentline,scroll_bg=self.background,active_scrollbar=self.selection)
        self.editor.auto_complete.pop_up.configure(bg=self.app_background,fg=self.foreground,selectbackground=self.selection,selectforeground=self.foreground,font=("Consolas",14))
        self.editor.minimap.configure(bg=self.background,fg=self.foreground)
        self.editor.change_indent_color(self.selection)
        self.file = file

        self.editor.editor.bind("<Control-=>",lambda event=None:self.zoom_in())
        self.editor.editor.bind("<Control-minus>",lambda event=None:self.zoom_out())
        
        with open(file, "r",encoding='utf-8') as f:
            self.editor.editor.insert("1.0", f.read())
        return self.editor
    def add_image_to_tab(self,file,name,image):
        
        
        label = Label(self.tab,bg=self.background)
        self.tab.add_tab(frame=label,text=name,image=image,file_path=file)

        image_pil = Image.open(file)
        # Convert the image to a format that tkinter can display
        image_pil.thumbnail((800,600))
        image_tk = ImageTk.PhotoImage(image_pil)
        # Update the label with the new image
        label.config(image=image_tk)

        label.image = image_tk
       
        self.file = file 


    def on_key_press(self,event):
        
        
        # Check if Ctrl and Alt are pressed along with 'o' key
        if event.keysym.lower() == 'o' and self.ctrl_pressed and self.alt_pressed:
            index = "%s-%sc"%("insert",1)
            self.editor.editor.delete(index,"insert")
            self.explorer.open_folder(self.folder)
            self.ctrl_pressed = False
            self.alt_pressed = False
           
        
            return "break"
    def on_key_release(self,event):
        
        
        # Reset Ctrl and Alt states when released
        if event.keysym.lower() in ['control_l', 'control_r']:
            self.ctrl_pressed = False
        elif event.keysym.lower() in ['alt_l', 'alt_r']:
            self.alt_pressed = False

    def on_ctrl_press(self,event):
       
        self.ctrl_pressed = True

    def on_alt_press(self,event):
       
        self.alt_pressed = True

        

    def Run(self):
        self.run()
    
if __name__ == "__main__":
    app = App()
    app.run()
