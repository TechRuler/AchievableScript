import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import*
import os 
from src.gui.Treeview import TreeView
import shutil


class FileManager(tk.Frame):
    def __init__(self,*arg,**kwarg):
        tk.Frame.__init__(self,*arg,**kwarg,highlightthickness=0)
        self.folder = ""
        self.command = None
        self.root_node_frame = tk.Frame(self)
        self.root_node_frame2 = tk.Frame(self.root_node_frame)
        self.root_node_frame2.pack(side="top",fill="x")
        self.root_node_frame.pack(side="top",fill="x")
        self.root_node = tk.Label(self.root_node_frame2,text="v No Folder Opened",anchor="w")
        self.root_node.pack(side="left")
        
        self.root_node_add_file = tk.Label(self.root_node_frame2,text="📄",border=0)
        self.root_node_add_folder = tk.Label(self.root_node_frame2,text="📂",border=0)
        self.root_node_add_reload = tk.Label(self.root_node_frame2,text="↻",border=0)
        self.root_node_add_unfold = tk.Label(self.root_node_frame2,text="-",border=0)

        

        self.file_creation_container = tk.Frame(self.root_node_frame)
        self.root_node_declaring_file = tk.Label(self.file_creation_container)
        self.root_node_declaring_file.pack(side="left")
        self.root_node_file_entry = tk.Entry(self.file_creation_container)
        self.root_node_file_entry.pack(side="left",fill="x",expand=True)

        self.folder_creation_container = tk.Frame(self.root_node_frame)
        self.root_node_declaring_folder = tk.Label(self.folder_creation_container)
        self.root_node_declaring_folder.pack(side="left")
        self.root_node_folder_entry = tk.Entry(self.folder_creation_container)
        self.root_node_folder_entry.pack(side="left",fill="x",expand=True)

        
        self.tree = TreeView(self)
        self.tree.pack(fill="both",expand=True)
        self.images()
        self.root_node_declaring_file.config(image=self.image_file)
        self.root_node_declaring_folder.config(image=self.image_folder)
        self.task()
        self.style = ttk.Style()
        self.style.theme_use("clam")
        # print(self.style.theme_names())
        self.Binding()
    def task(self):
        self.tab = None
    def Binding(self):
        self.root_node.bind("<Button-1>",lambda event=None:self.tree_toggle())
        self.root_node_frame.bind("<Button-1>",lambda event=None:self.tree_toggle())
        
        self.bind("<Enter>",lambda event=None:self.button_show())
        self.bind("<Leave>",lambda event=None:self.button_hide())
        self.root_node_add_file.bind("<Button-1>",lambda event=None:self.file_creation_container.pack(side="top",fill="x"))
        self.root_node_add_folder.bind("<Button-1>",lambda event=None:self.folder_creation_container.pack(side="top",fill="x"))

        self.root_node_file_entry.bind("<Return>",lambda event=None:self.create_file())
        self.root_node_file_entry.bind("<KeyRelease>",lambda event=None:self.change_image(self.root_node_file_entry,self.root_node_declaring_file))
        self.root_node_folder_entry.bind("<Return>",lambda event=None:self.create_folder())
        
    def configures(self,background="white",foreground="black",fon=("Consolas",9),selected_bg="grey",selected_fg="white",border_color="white"):
        self.style.configure("Treeview",background=background,foreground=foreground,fieldbackground=background,bordercolor=border_color,highlightthickness=0, padding=0)
        self.style.map("Treeview",background=[("selected",selected_bg)],foreground=[("selected",selected_fg)])
    def root_node_bind(self,normal="grey15",hover="grey"):
        self.root_node_add_file.bind("<Enter>",lambda event=None:self.highlight(self.root_node_add_file,hover))
        self.root_node_add_file.bind("<Leave>",lambda event=None:self.highlight(self.root_node_add_file,normal))
        self.root_node_add_folder.bind("<Enter>",lambda event=None:self.highlight(self.root_node_add_folder,hover))
        self.root_node_add_folder.bind("<Leave>",lambda event=None:self.highlight(self.root_node_add_folder,normal))
        self.root_node_add_reload.bind("<Enter>",lambda event=None:self.highlight(self.root_node_add_reload,hover))
        self.root_node_add_reload.bind("<Leave>",lambda event=None:self.highlight(self.root_node_add_reload,normal))
        self.root_node_add_unfold.bind("<Enter>",lambda event=None:self.highlight(self.root_node_add_unfold,hover))
        self.root_node_add_unfold.bind("<Leave>",lambda event=None:self.highlight(self.root_node_add_unfold,normal))
    def highlight(self,widget,color):
        widget.configure(bg=color)
    def create_file(self):
        if self.root_node_file_entry.get() != "":
            name = os.path.basename(self.folder)
            with open(f"{self.folder}/{self.root_node_file_entry.get()}","w") as f:
                pass
            self.tree.delete()
            abspath = os.path.abspath(self.folder)
            
            self.root_node.config(text=f"v {name}")
            self.process_directory("",abspath,level=0)
            self.root_node_file_entry.delete(0,"end")
            self.file_creation_container.pack_forget()
            with open(f"{self.folder}/{self.root_node_file_entry.get()}","r") as f:
                pass
    def create_folder(self):
        if self.root_node_folder_entry.get() != "":
            name = os.path.basename(self.folder)
            os.makedirs(f"{self.folder}/{self.root_node_folder_entry.get()}")
            self.tree.delete()
            abspath = os.path.abspath(self.folder)
            
            self.root_node.config(text=f"v {name}")
            self.process_directory("",abspath)
            self.root_node_folder_entry.delete(0,"end")
            self.folder_creation_container.pack_forget()
    def remove(self):
        
        item = self.tree.selection()
        name = self.tree.item(item,"text")
        path = self.tree.item(item,"values")
        abspath = os.path.join(self.folder,name)
        folder_name = os.path.basename(self.folder)
        isdir = os.path.isdir(abspath)
        if isdir:
            shutil.rmtree(f"{path}")
            self.tree.delete()
            abspath = os.path.abspath(self.folder)
            # root_node = self.tree.insert("",'end',text=abspath,open=True,image=image_folder)
            self.root_node.config(text=f"v {folder_name}")
            self.process_directory("",abspath)
        else:
            os.remove(f"{path}")
            self.tree.delete()
            abspath = os.path.abspath(self.folder)
            # root_node = self.tree.insert("",'end',text=abspath,open=True,image=image_folder)
            self.root_node.config(text=f"v {folder_name}")
            self.process_directory("",abspath)
    def rename_item(self,background,foreground):
        
        item_id = self.tree.selection()
        item_text = self.tree.item(item_id, "text")
        item_path = self.tree.item(item_id, "values")
        

        # Get the bounding box of the item and place the entry next to the icon
        bbox = self.tree.bbox(item_id)
        level = self.tree.get_level(item_id)
        
        if bbox:
            x, y, width, height = bbox
            if os.path.isdir(item_path):
                icon_width = (int(level) + 40)  # Width of the icon, adjust as needed
            else:
                icon_width = (int(level) + 47)  # Width of the icon, adjust as needed
            
            entry = tk.Entry(self.tree,bg=background,fg=foreground,font=("Consolas",10),insertbackground=foreground, width=30)
            entry.insert(0, item_text)
            entry.bind("<Return>", lambda e: self.save_rename(e, item_id, item_path, entry))
           
            entry.place(x=x + icon_width, y=y, width=width - icon_width, height=height)
            entry.focus_set()
    def save_rename(self,event, item_id, old_path, entry):
        new_name = entry.get()
        entry.destroy()
        
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if os.path.isfile(old_path):
            try:
                os.rename(old_path, new_path)
                extension = os.path.splitext(new_name)[1]
                new_image = self.get_image_for_extension(extension)
                self.tree.item(item_id, text=new_name, values=new_path, image=new_image)
               
            except Exception as e:
                print(f"Error renaming item: {e}")
        else:
            try:
                os.rename(old_path, new_path)
                extension = os.path.splitext(new_name)[1]
                new_image = self.get_image_for_extension(extension)
                self.tree.item(item_id, text=new_name, values=new_path)
                
            except Exception as e:
                print(f"Error renaming item: {e}")
                
    def change_image(self,entry,label):
        if "."in entry.get() and entry.get()!="":
            extension = os.path.splitext(entry.get())[1]
            
            image = self.get_image_for_extension(extension)
            label.config(image=image)
            
    def tree_toggle(self):
        if self.folder:
            name = os.path.basename(self.folder)
            if self.tree.winfo_ismapped():
                self.tree.pack_forget()
                self.root_node.config(text=f"> {name}")
            else:
                self.tree.pack(fill="both",expand=True)
                self.root_node.config(text=f"v {name}")
        else:
            if self.tree.winfo_ismapped():
                self.tree.pack_forget()
                self.root_node.config(text="> No Folder Opened")
            else:
                self.tree.pack(fill="both",expand=True)
                self.root_node.config(text="v No Folder Opened")
    def button_show(self):
        if self.folder:
            self.root_node_add_unfold.pack(side="right",padx=(5,5))
            self.root_node_add_reload.pack(side="right",padx=(5,5))
            self.root_node_add_folder.pack(side="right",padx=(5,5))
            self.root_node_add_file.pack(side="right",padx=(5,5))
    def button_hide(self):
        if self.folder:
            self.root_node_add_unfold.pack_forget()
            self.root_node_add_reload.pack_forget()
            self.root_node_add_folder.pack_forget()
            self.root_node_add_file.pack_forget()
    def open_folder(self,folder):
        self.folder = folder
        self.tree.delete()
        self.folder = askdirectory()
        if self.folder:
            name = os.path.basename(self.folder)
            abspath = os.path.abspath(self.folder)
            # root_node = self.tree.insert("",text=abspath,open=True,image=self.image_folder,values=abspath,level=0)
            self.root_node.config(text=f"v {name}")
            self.process_directory("",abspath,level=0)
            
            self.command()
            

            
    
    def images(self):
        
        self.image_folder =tk.PhotoImage(file="assets/icons/folder.png")
        self.image_python =tk.PhotoImage(file="assets/icons/python.png")
        self.image_text =tk.PhotoImage(file="assets/icons/file.png")
        self.image_html =tk.PhotoImage(file="assets/icons/html.png")
        self.image_css =tk.PhotoImage(file="assets/icons/css.png")
        self.image_js =tk.PhotoImage(file="assets/icons/Javascript.png")
        self.image_pdf =tk.PhotoImage(file="assets/icons/pdf.png")
        self.image_file =tk.PhotoImage(file="assets/icons/Unknown file.png")
        self.image_zip =tk.PhotoImage(file="assets/icons/Zip.png")
        self.image_mp4 =tk.PhotoImage(file="assets/icons/mp4.png")
        self.image_json =tk.PhotoImage(file="assets/icons/Json.png")
        self.image_image =tk.PhotoImage(file="assets/icons/image.png")
    def process_directory(self,parent,path,level=0):
        dirs = []
        files = []

        for i in os.listdir(path):
            abspath = os.path.join(path,i)
            if os.path.isdir(abspath):
                dirs.append(i)
            else:
                files.append(i)
        for d in dirs:
            abspath = os.path.join(path,d)
            tree_element = self.tree.insert(parent,text=d,open=False,image=self.image_folder,values=abspath,level=level+1)
            # print(tree_element)
            self.process_directory(tree_element,abspath,level+1)
        for f in files:
            abspath = os.path.join(path,f)
            extension = os.path.splitext(f)[1]
            image = self.get_image_for_extension(extension)
            self.tree.insert(parent=parent, text=f, open=False, image=image, values=abspath, level=level + 1)
    def get_image_for_extension(self,extension):
        if extension == ".py":
            return self.image_python
        elif extension == ".txt":
            return self.image_text
        elif extension == ".html":
            return self.image_html
        elif extension == ".css":
            return self.image_css 
        elif extension == ".js":
            return self.image_js
        elif extension == ".png":
            return self.image_image
        elif extension == ".spec":
            return self.image_file
        elif extension == ".mp4":
            return self.image_mp4
        elif extension == ".pdf":
            return self.image_pdf
        elif extension == ".zip":
            return self.image_zip
        elif extension == ".json":
            return self.image_json
        else:
            return self.image_file
#------------------------testing------------------------------------------------------------------------
def open_folder(event=None):
    global side_bar
    side_bar.tree.delete()
    folder = askdirectory()
    abspath = os.path.abspath(folder)
    parent = side_bar.tree.insert("",text=folder,open=True,image=side_bar.image_folder,values=abspath,level=0)
    side_bar.process_directory(parent,abspath,level=0)
def main():
    global side_bar
    root = tk.Tk()


    side_bar = FileManager(root)
    side_bar.pack(expand=True,fill="both")
    








    root.bind("<Control-o>",open_folder)
    root.mainloop()
if __name__ == "__main__":
    main()