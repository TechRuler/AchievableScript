import tkinter as tk 
from tkinter.filedialog import*
class NoteBook(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # self.config(bg="grey")
        self.text = ""
        self.original_color = "white"
        self.selected_color = "grey"
        self.line_color = "yellow"
        self.tab_bar = tk.Frame(self, height=25)
        self.tab_bar.pack(side=tk.TOP, fill="x")
        self.frames = {}  # Store frames associated with tabs
        self.tabs = {}  # Store tab associated with frames
        self.file_paths = {}  # Store file paths associated with frames
        self.selected_tab = None
        self.current_frame = None
        self.master.master.title("PossibleScript")
        self.file = ""
    def config_colors(self, tab_bg, tab_fg, tab_bar_color, frame_color, selected_tab_color,line_color):
        self.original_color = tab_bg
        self.selected_color = selected_tab_color
        self.line_color = line_color
        self.tab_bar.config(bg=tab_bar_color)
        
        # Update existing tabs with new colors
        for tab in self.frames:
            tab.config(bg=self.original_color)
            for widget in tab.winfo_children():
                if isinstance(widget,tk.Frame):
                    widget.config(bg=self.line_color)
                else:
                    widget.config(bg=self.original_color, fg=tab_fg)

        # Update existing frames with new color
        for frame in self.frames.values():
            frame.config(bg=frame_color)
            for child in frame.winfo_children():
                try:
                    child.config(bg=selected_tab_color)
                except:
                    pass
            print(frame)

        # Update the currently selected tab
        if self.current_frame:
            current_tab = self.tabs[self.current_frame]
            self.change_tab_color(current_tab, self.selected_color)
    def add_tab(self, frame=None, text="", image="", file_path=""):
        self.text = text
        self.image = image
        tab = tk.Frame(self.tab_bar, bg=self.original_color,cursor="hand2")
        tab.pack(side="left", fill="y")
        line = tk.Frame(tab,height=2)
        line.pack(fill="x")
        line.pack_propagate(0)
        
        image_label = tk.Label(tab, image=self.image, fg="white", background=self.original_color,pady=5)
        image_label.pack(side="left", fill="y")

        text_label = tk.Label(tab, text=self.text, fg="white", background=self.original_color, font=("Consolas", 12),pady=10)
        text_label.pack(side="left", fill="y")

        close_button = tk.Label(tab, text="✕", border=0, background=self.original_color, fg="white", font=("Consolas", 12),pady=10)
        close_button.pack(side="right", fill="y", padx=(20, 5))

        # Store the frame, its associated tab, and file path
        self.frames[tab] = frame
        self.tabs[frame] = tab
        self.file_paths[frame] = file_path

        tab.bind("<Button-1>", lambda event, tab=tab: self.tab_click(event, tab))
        text_label.bind("<Button-1>", lambda event, tab=tab: self.tab_click(event, tab))
        image_label.bind("<Button-1>", lambda event, tab=tab: self.tab_click(event, tab))
        close_button.bind("<Button-1>", lambda event, tab=tab: self.destroy_tab(event, tab))
        close_button.bind("<Enter>",lambda event=None,j=close_button:self.changeColor(j,"yellow"))
        close_button.bind("<Leave>",lambda event=None,j=close_button:self.changeColor(j,"white"))

        self.select_tab(tab)  # Automatically select the new tab
    def changeColor(self,widget,color):
        widget.config(fg=color)
    def tab_click(self, event, tab):
        self.select_tab(tab)

    def select_tab(self, tab):
        # Hide the current frame
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Show the new frame
        self.current_frame = self.frames[tab]
        self.current_frame.pack(expand=True, fill=tk.BOTH)
        
        # Handle tab selection visuals
        self.change_tab_color(tab, self.selected_color)

        # Update window title with the file path
        self.master.master.title(f"PossibleScript - {self.file_paths[self.current_frame]}")
        self.file = self.file_paths[self.current_frame]
        self.selected_tab = tab 

    def destroy_tab(self, event, tab):
        if tab in self.frames:
            frame_to_destroy = self.frames[tab]

            # If the frame to destroy is the currently selected frame
            if frame_to_destroy == self.current_frame:
                frame_to_destroy.pack_forget()
                self.current_frame = None

                # Find the index of the tab before removing it
                tabs = list(self.frames.keys())
                index = tabs.index(tab)

                # Remove the tab and frame
                self.frames.pop(tab)
                self.tabs.pop(frame_to_destroy, None)
                self.file_paths.pop(frame_to_destroy, None)
                tab.destroy()

                # If there are any remaining tabs, select the adjacent one
                if self.frames:
                    if index > 0:
                        adjacent_tab = tabs[index - 1]
                    else:
                        adjacent_tab = tabs[1] if len(tabs) > 1 else None

                    if adjacent_tab:
                        self.current_frame = self.frames[adjacent_tab]
                        self.current_frame.pack(expand=True, fill=tk.BOTH)
                        self.change_tab_color(adjacent_tab, self.selected_color)
                        self.master.master.title(f"PossibleScript - {self.file_paths[self.current_frame]}")
                        self.file  = self.file_paths[self.current_frame]
                        self.selected_tab = adjacent_tab
            else:
                # If the frame to destroy is not the currently selected frame
                self.frames.pop(tab)
                self.tabs.pop(frame_to_destroy, None)
                self.file_paths.pop(frame_to_destroy, None)
                tab.destroy()
    def selection(self):
        return self.selected_tab
    

        
    def change_tab_color(self, selected_tab, color):
        for tab in self.frames:
            if tab == selected_tab:
                tab.config(bg=color)
                for widget in tab.winfo_children():
                    if isinstance(widget,tk.Frame):
                        widget.config(bg=self.line_color)
                    else:
                        widget.config(bg=color)
            else:
                tab.config(bg=self.original_color)
                for widget in tab.winfo_children():
                    widget.config(bg=self.original_color)
def save(event=None):
    global side_bar,file,tab
    if file:
        for current,associated_tab in tab.tabs.items():
            if tab.file_paths[current] == file :
                content = current.get("1.0","end")
                with open(file,"w") as f:
                            f.write(content)
                            print("complete")
    else:
        file = asksaveasfilename()
        for current,associated_tab in tab.tabs.items():
            if tab.file_paths[current] == file :
                for widget in current.winfo_children():
                    if isinstance(widget,tk.Text):
                        content = widget.get("1.0","end")
                        with open(file,"w") as f:
                            f.write(content)