import tkinter as tk
from tkinter.filedialog import askdirectory
import os
from src.gui.scrollbar import AutoScrollbar



class TreeView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frames = {}
        self.file_path = {}
        self.order = []
        self.data_frame_and_level = {}
        self.selected_item = None
        self.added_command = list()
        self.added_one_more_command = None
        self.indentation = 20  # Set the indentation width
        self.default_bgcolor = "white"
        self.default_fgcolor = "black"
        self.selected_bgcolor = "grey15"
        self.selected_fgcolor = "white"
        self.hover_bgcolor = "grey"
        self.font = "Consolas"
        self.font_size = 12

        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(self,bd=0, highlightthickness=0)
        self.scrollbar = AutoScrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window =self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(self.canvas_window,width=event.width)
        )
        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.canvas.grid(row=0,column=0,sticky="nsew")
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        # Bind mousewheel events
        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        current_y = self.canvas.yview()
        if event.delta > 0:  # Mouse wheel up
            if current_y[0] > 0:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.delta < 0:  # Mouse wheel down
            if current_y[1] < 1:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def insert(self, parent="", text="", image="", open=False, values="", level=0):
        is_dir = os.path.isdir(values)
        container_frame = tk.Frame(self.scrollable_frame if parent == "" else parent,bg=self.default_bgcolor)
        container_frame.level = level
        
        data_frame = tk.Frame(container_frame,bg=self.default_bgcolor)
    
        element_frame = tk.Frame(data_frame,bg=self.default_bgcolor)
        textvariable = str()
        if open:
            direction_text = "v" if is_dir else "  "
        else:
             direction_text = ">" if is_dir else "  "
        direction = tk.Label(element_frame, text=direction_text, anchor="w", font=(self.font, self.font_size),bg=self.default_bgcolor,fg=self.default_fgcolor)
        element = tk.Label(element_frame, text=text, image=image, compound="left",textvariable=textvariable, anchor="w", font=(self.font, self.font_size),bg=self.default_bgcolor,fg=self.default_fgcolor)

        # Bind click event to directory text
        if is_dir:
            element.bind("<Button-1>", lambda e, ef=element_frame, d=data_frame: self.on_items(d, self.selected_bgcolor, self.selected_fgcolor))
            direction.bind("<Button-1>", lambda e, ef=element_frame, d=data_frame: self.on_items(d, self.selected_bgcolor, self.selected_fgcolor))
            element.bind("<Button-3>", lambda event, ef=element_frame, d=data_frame: self.added_one_more_command(event))

        else:
            element.bind("<Button-1>", lambda e, ef=element_frame, d=data_frame: self.on_click(d, self.selected_bgcolor, self.selected_fgcolor))
            direction.bind("<Button-1>", lambda e, ef=element_frame, d=data_frame: self.on_click(d, self.selected_bgcolor, self.selected_fgcolor))
            element.bind("<Button-3>", lambda event, ef=element_frame, d=data_frame: self.added_one_more_command(event))
        data_frame.bind("<Enter>", lambda event=None, i=data_frame: self.highlight(i, self.hover_bgcolor))
        data_frame.bind("<Leave>", lambda event=None, i=data_frame: self.highlight(i, self.default_bgcolor, self.default_fgcolor))

        direction.pack(side="left")
        element.pack(side="left", expand=True, fill="both")
        element_frame.pack(fill="x", padx=(level * self.indentation,0))
        data_frame.pack(fill="x")
        container_frame.pack(fill="x")

        self.file_path[data_frame] = values
        self.data_frame_and_level[data_frame] = level * self.indentation
        
        if is_dir:
            frame = tk.Frame(container_frame)
            self.frames[data_frame] = frame
            if open:
                frame.pack(fill="both")
            self.order.append(container_frame)
            return frame
        else:
            self.order.append(container_frame)
        return container_frame
        

    def on_items(self,data_frame, bgcolor, fgcolor):
        self.toggle_directory(data_frame=data_frame)
        self.on_click(element=data_frame, bgcolor=bgcolor, fgcolor=fgcolor)

    def on_click(self, element, bgcolor, fgcolor):
        if self.selected_item:
            self.deselect(self.selected_item)

        self.selected_item = element
        self.select(element, bgcolor, fgcolor)
        for task in self.added_command:
            task()
    def selection(self):
        if self.selected_item:
            return self.selected_item
        else:
            raise tk.TclError('there is nothing selected!!')
    def item(self,input,string=None,text=None,values=None,image=None):
        if string:
            
            if string == "text":
                text_name = None
                for child in input.winfo_children():
                    for sub_child in child.winfo_children():
                        if isinstance(sub_child,tk.Label) and sub_child.cget("text") != ">" and sub_child.cget("text") != "v":
                            text_name = sub_child.cget("text")
                return text_name
            elif string == "values":
                values_get = None
                for data_frame, path in self.file_path.items():
                    if input == data_frame:
                        values_get = path 
                return values_get
            elif string == "image":
                image_get = None
                for child in input.winfo_children():
                    for sub_child in child.winfo_children():
                        if isinstance(sub_child,tk.Label) and sub_child.cget("text") != ">" and sub_child.cget("text") != "v":
                            image_get = sub_child.cget("image")
                return image_get
        if text:
            for child in input.winfo_children():
                label = child.winfo_children()[1]
                   
                label.config(text=text)
        if values:
            for data_frame, path in self.file_path.items():
                if input == data_frame:
                    self.file_path[data_frame] = values
        if image:
            for child in input.winfo_children():
                label = child.winfo_children()[1]
                       
                label.config(image=image)
                        
    def bbox(self,item):
        parent_x = self.scrollable_frame.winfo_rootx()
        parent_y = self.scrollable_frame.winfo_rooty()
        x = item.winfo_rootx() - parent_x
        y = item.winfo_rooty() - parent_y
        width = item.winfo_width()
        height = item.winfo_height()
        return x, y, width, height

    def get_level(self,item):
        for data_frame,level in self.data_frame_and_level.items():
            if data_frame == item:
                return level
    def select(self, element, bgcolor, fgcolor):
        element.config(bg=bgcolor)
        for widget in element.winfo_children():
            widget.config(bg=bgcolor)
            for child in widget.winfo_children():
                child.config(bg=bgcolor, fg=fgcolor)

    def deselect(self, element):
        element.config(bg=self.default_bgcolor)
        for widget in element.winfo_children():
            widget.config(bg=self.default_bgcolor)
            for child in widget.winfo_children():
                child.config(bg=self.default_bgcolor, fg=self.default_fgcolor)

    def toggle_directory(self,data_frame):
        frame = self.frames.get(data_frame)
        if frame:
            if frame.winfo_ismapped():
                frame.pack_forget()
                for element in data_frame.winfo_children():
                    direction_label = element.winfo_children()[0]
                    direction_label.config(text=">")
            else:
                frame.pack(fill="both")
                for element in data_frame.winfo_children():
                    direction_label = element.winfo_children()[0]
                    direction_label.config(text="v")

    def highlight(self, parent, bg_color, fg_color=None):
        if self.selected_item != parent:
            parent.config(bg=bg_color)
            for child in parent.winfo_children():
                child.config(bg=bg_color)
                for widget in child.winfo_children():
                    widget.config(bg=bg_color, fg=(self.default_fgcolor if fg_color is None else fg_color))

    def delete(self):
        for element in self.order:
            element.pack_forget()

    def pack_ordered(self):
        for element in self.order:
            element.pack(fill="x")

    def color_config(self, default_bgcolor="white", default_fgcolor="black", selected_bgcolor="grey15", selected_fgcolor="white", hover_bgcolor="grey",font="Consolas",font_size=12):
        self.default_bgcolor = default_bgcolor
        self.default_fgcolor = default_fgcolor
        self.selected_bgcolor = selected_bgcolor
        self.selected_fgcolor = selected_fgcolor
        self.hover_bgcolor = hover_bgcolor
        self.font = font
        self.font_size = font_size
        self.canvas.config(bg=self.default_bgcolor)
        # self.config(bg=self.default_bgcolor)
        self.scrollable_frame.config(bg=self.default_bgcolor)
        for element in self.order:
            element.config(bg=default_bgcolor)
            for child in element.winfo_children():
                child.config(bg=default_bgcolor)
                for widget in child.winfo_children():
                    widget.config(bg=default_bgcolor, fg=default_fgcolor)
                    for sub_child in widget.winfo_children():
                        sub_child.config(bg=default_bgcolor, fg=default_fgcolor,font=(self.font,self.font_size))

def get_image_for_extension(extension):
    if extension == ".py":
        return image_python
    elif extension == ".txt":
        return image_text
    elif extension == ".html":
        return image_html
    elif extension == ".png":
        return image_image
    elif extension == ".spec":
        return image_file
    elif extension == ".mp4":
        return image_mp4
    elif extension == ".pdf":
        return image_pdf
    elif extension == ".zip":
        return image_zip
    elif extension == ".json":
        return image_json
    else:
        return image_file
def process_directory(parent, path, level=0):
    dirs = []
    files = []

    for i in os.listdir(path):
        abspath = os.path.join(path, i)
        if os.path.isdir(abspath):
            dirs.append(i)
        else:
            files.append(i)
    for d in dirs:
        abspath = os.path.join(path, d)
        tree_element = tree.insert(parent=parent, text=d, open=False, image=image_folder, values=abspath, level=level + 1)
        process_directory(tree_element, abspath, level + 1)
    for f in files:
        abspath = os.path.join(path, f)
        extension = os.path.splitext(f)[1]
        image = get_image_for_extension(extension)
        tree.insert(parent=parent, text=f, open=False, image=image, values=abspath, level=level + 1)
def select(event=None):
    a = tree.selection()
    text = tree.item(a,"text")
    values = tree.item(a,"values")
    print(text)
    print(values)
def Printing(event=None):
    print("function is working here file")
def Open(event=None):
    tree.delete()
    folder = askdirectory()
    abspath = os.path.abspath(folder)
    root_node = tree.insert(parent="", text=folder, open=True, image=image_folder, values=abspath, level=0)
    process_directory(parent=root_node, path=folder, level=0)

if __name__ == "__main__":
    root = tk.Tk()
    image_folder = tk.PhotoImage(file="assets/icons/folder.png")
    image_python = tk.PhotoImage(file="assets/icons/python.png")
    image_text = tk.PhotoImage(file="assets/icons/file.png")
    image_html = tk.PhotoImage(file="assets/icons/html.png")
    image_css = tk.PhotoImage(file="assets/icons/css.png")
    image_js = tk.PhotoImage(file="assets/icons/Javascript.png")
    image_pdf = tk.PhotoImage(file="assets/icons/pdf.png")
    image_file = tk.PhotoImage(file="assets/icons/Unknown file.png")
    image_zip = tk.PhotoImage(file="assets/icons/Zip.png")
    image_mp4 = tk.PhotoImage(file="assets/icons/mp4.png")
    image_json = tk.PhotoImage(file="assets/icons/Json.png")
    image_image = tk.PhotoImage(file="assets/icons/image.png")
        
    tree = TreeView(root)
    tree.pack(fill="both", expand=True)

    # Example of setting custom colors
    
    tree.color_config(default_bgcolor="spring green", default_fgcolor="black", selected_bgcolor="tomato", selected_fgcolor="white", hover_bgcolor="cyan")

    # tree.added_command = Printing
    tree.added_one_more_command = Printing
    tree.bind("<Button-3>",lambda event=None:Printing())
    root.bind("<Control-o>", Open)
    root.bind("<Control-p>",select)

    root.mainloop()
