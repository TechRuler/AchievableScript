from ctypes import windll
import tkinter as tk 
import threading
import time 
import ctypes
from ctypes import wintypes

# Constants for DPI awareness levels
PROCESS_PER_MONITOR_DPI_AWARE = 2


# Load necessary libraries
user32 = ctypes.WinDLL('user32', use_last_error=True)
shcore = ctypes.WinDLL('Shcore', use_last_error=True)

# Function to set process DPI awareness (for Windows 8.1 and later)
def set_process_dpi_awareness():
    try:
        shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    except AttributeError:
        # Fallback for older versions of Windows (Vista, 7, 8)
        user32.SetProcessDPIAware()

# Function to adjust window DPI awareness for Windows 10
def set_process_dpi_aware_v2():
    try:
        success = user32.SetProcessDpiAwarenessContext(wintypes.HANDLE(-4))  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
    except AttributeError:
        # If SetProcessDpiAwarenessContext is not available, use the older method
        set_process_dpi_awareness()

# Apply DPI awareness settings
set_process_dpi_aware_v2()


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.geometry("250x250+100+100")
        self.resizable(True,True)
        self.minsize(250,250)

        self.variables()
        self.setup_ui()
        # self.menubar()
        self.bindings()

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.background_task)
        self.thread.start()
    def bindings(self):
        self.titleBar.bind("<Map>",self.Mapping)
        self.titleBar.bind("<B1-Motion>",self.on_drag)
        self.Title.bind("<B1-Motion>",self.on_drag)
        self.title_minimise_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_minimise_button,color="grey"))
        self.title_minimise_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_minimise_button,color="white"))
        self.title_resize_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_resize_button,color="grey"))
        self.title_resize_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_resize_button,color="white"))
        self.title_close_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_close_button,color="red"))
        self.title_close_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_close_button,color="white"))

        self.bind_all("<ButtonPress-1>",self.on_click)
        self.bind_all("<Motion>",self.motions)
        self.bind_all("<B1-Motion>",self.on_resizing)
    def variables(self):
        self.app_height = 250
        self.app_width = 250
        self.app_x = 100
        self.app_y = 100
        self.size = False
        self._drag_data = {"x":0,"y":0,"abs_x":0,"abs_y":0,"side":None}
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00400000
        self.WS_EX_TOOLWINDOW = 0x00000080
        self.hasstyle = False
    def get_app_height(self):
        return self.app_height
    def get_app_width(self):
        return self.app_width
    def on_resizing(self,event):
        if not self.size:
            self.window_resizings(event)
    def setGeometry(self,width,height,x,y): # to get height, width, x and y in main app 
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.app_width = width
        self.app_height = height
        self.app_x = x 
        self.app_y = y
    def setup_ui(self):

        self.titleBar = tk.Frame(self)
        self.titleBar.pack(side="top",fill="x")

        self.titleBar_icon = tk.Label(self.titleBar,text="")
        self.titleBar_icon.pack(side="left")

        self.Title = tk.Label(self.titleBar,text="My Code editor",font=("Consolas",12))
        self.Title.pack(side="left")

        self.title_close_button = tk.Button(self.titleBar,text=" ✕ ",border=0,font=("Consolas",12),bg="white",command=self.close_app)
        self.title_close_button.pack(side="right")
        self.title_resize_button = tk.Button(self.titleBar,text=" \u25a0 ",font=("Consolas",12),bg="white",border=0,command=self.resize_button_function)
        self.title_resize_button.pack(side="right")
        self.title_minimise_button = tk.Button(self.titleBar,text=" - ",font=("Consolas",12),bg="white",border=0,command=self.minimise_function)
        self.title_minimise_button.pack(side="right")

        self.config(bg="white")
    def close_app(self):
        # Set the stop_event to stop the background thread
        self.stop_event.set()
        self.thread.join()  # Wait for the background thread to finish
        self.force_close()  # Proceed to force close the application

    def force_close(self):
        # Forcefully close the application using ctypes
        try:
            ctypes.windll.user32.PostQuitMessage(0)
        except Exception as e:
            print(f"Error while closing the application: {e}")
        finally:
            self.quit()  # Ensure the application is quit
    def background_task(self):
        while not self.stop_event.is_set():
            # Simulating background work
            print("Background task is running...")
            time.sleep(1)
        print("Background task has stopped.")
    
    def highlight(self,widget,color):
        widget.config(bg=color)
    def app_icon(self,image):
        self.titleBar_icon.config(image=image)
    def my_title(self,title="My Code Editor"):
        self.Title.config(text=title)
    title = my_title
    # def menubar(self):
    #     self.menu_frame = tk.Frame(self)
    #     self.menu_frame.pack(side="top",fill="x") 
    # def add_menu(self,text="",bg="white",fg="black",font=("Consolas",12),activebackground="tomato",activeforegroun="white",command=None):
    #     menu = tk.Menubutton(self.menu_frame,text=text,background=bg,foreground=fg,font=font,activebackground=activebackground,activeforeground=activeforegroun,border=0)
    #     # menu.pack(side="left",fill="y")
    #     self.menu_frame.config(bg=bg)
    #     if command:
    #         menu.bind("<Button-1>",lambda event=None:command())
    #     return menu
    def add_configure(self,font=("Consolas",12),background="white",foreground="black",hover_resize_button_color="grey",hover_minimise_button_color="grey",hover_close_button_color="red"):
        self.Title.configure(font=font,bg=background,fg=foreground)
        self.titleBar.configure(bg=background)
        self.titleBar_icon.configure(bg=background)
        self.title_resize_button.configure(font=font,background=background,foreground=foreground)
        self.title_close_button.configure(font=font,background=background,foreground=foreground)
        self.title_minimise_button.configure(font=font,background=background,foreground=foreground)

        self.title_minimise_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_minimise_button,color=hover_minimise_button_color))
        self.title_minimise_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_minimise_button,color=background))
        self.title_resize_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_resize_button,color=hover_resize_button_color))
        self.title_resize_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_resize_button,color=background))
        self.title_close_button.bind("<Enter>",lambda event=None:self.highlight(widget=self.title_close_button,color=hover_close_button_color))
        self.title_close_button.bind("<Leave>",lambda event=None:self.highlight(widget=self.title_close_button,color=background))
        
    
    def motions(self,event):
        x,y = self.winfo_pointerx()-self.winfo_rootx(),self.winfo_pointery()-self.winfo_rooty()
        borderwidth = 5
        if not self.size:
            if x < borderwidth and y < borderwidth:
                self.config(cursor="top_left_corner")
                self._drag_data["side"] = "top_left_corner"
            elif x > self.winfo_width() - borderwidth and y < borderwidth:
                self.config(cursor="top_right_corner")
                self._drag_data["side"] = "top_right_corner"
            elif x > self.winfo_width() - borderwidth and y > self.winfo_height() - borderwidth:
                self.config(cursor="bottom_right_corner")
                self._drag_data["side"] = "bottom_right_corner"
            elif x < borderwidth and y > self.winfo_height() - borderwidth:
                self.config(cursor="bottom_left_corner")
                self._drag_data["side"] = "bottom_left_corner"
            elif x < borderwidth:
                self.config(cursor="left_side")
                self._drag_data["side"] = "left"
            elif x > self.winfo_width() - borderwidth:
                self.config(cursor="right_side")
                self._drag_data["side"] = "right"
            elif y < borderwidth:
                self.config(cursor="top_side")
                self._drag_data["side"] = "top"
            elif y > self.winfo_height() - borderwidth:
                self.config(cursor="bottom_side")
                self._drag_data["side"] = "bottom"
            else:
                self.config(cursor="")
                self._drag_data["side"] = None
    def window_resizings(self,event):
        if self._drag_data["side"] == "left":
            new_width = self.winfo_width() - (event.x_root - self._drag_data["abs_x"])
            new_x = self.winfo_x() + (event.x_root - self._drag_data["abs_x"])
            self.geometry(f"{new_width}x{self.winfo_height()}+{new_x}+{self.winfo_y()}")
            self._drag_data["abs_x"] = event.x_root

            self.app_height = self.winfo_height()
            self.app_width = new_width
            self.app_x = new_x
            self.app_y = self.winfo_y()
        elif self._drag_data["side"] == "right":
            new_width = self.winfo_width() + (event.x_root - self._drag_data["abs_x"])
            self.geometry(f"{new_width}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()}")
            self._drag_data["abs_x"] = event.x_root

            self.app_height = self.winfo_height()
            self.app_width = new_width
            self.app_x = self.winfo_x()
            self.app_y = self.winfo_y()

        elif self._drag_data["side"] == "top":
            new_height = self.winfo_height() - (event.y_root - self._drag_data["abs_y"])
            new_y = self.winfo_y() + (event.y_root - self._drag_data["abs_y"])
            self.geometry(f"{self.winfo_width()}x{new_height}+{self.winfo_x()}+{new_y}")
            self._drag_data["abs_y"] = event.y_root

            self.app_height = new_height
            self.app_width = self.winfo_width()
            self.app_x = self.winfo_x()
            self.app_y = new_y



        elif self._drag_data["side"] == "bottom":
            new_height = self.winfo_height() + (event.y_root - self._drag_data["abs_y"])
            self.geometry(f"{self.winfo_width()}x{new_height}+{self.winfo_x()}+{self.winfo_y()}")
            self._drag_data["abs_y"] = event.y_root

            self.app_height = new_height
            self.app_width = self.winfo_width()
            self.app_x = self.winfo_x()
            self.app_y = self.winfo_y()
        elif self._drag_data["side"] == "top_left_corner":
            new_height = self.winfo_height() - (event.y_root - self._drag_data["abs_y"])
            new_width = self.winfo_width() - (event.x_root - self._drag_data["abs_x"])
            new_x = self.winfo_x() + (event.x_root - self._drag_data["abs_x"])
            new_y = self.winfo_y() + (event.y_root - self._drag_data["abs_y"])
            self.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")
            self._drag_data["abs_x"] = event.x_root
            self._drag_data["abs_y"] = event.y_root

            self.app_height = new_height
            self.app_width = new_width
            self.app_x = new_x
            self.app_y = new_y
        
        elif self._drag_data["side"] == "bottom_right_corner":
            new_height = self.winfo_height() + (event.y_root - self._drag_data["abs_y"])
            new_width = self.winfo_width() + (event.x_root - self._drag_data["abs_x"])
            self.geometry(f"{new_width}x{new_height}+{self.winfo_x()}+{self.winfo_y()}")
            self._drag_data["abs_x"] = event.x_root
            self._drag_data["abs_y"] = event.y_root


            self.app_height = new_height
            self.app_width = new_width
            self.app_x = self.winfo_x()
            self.app_y = self.winfo_y()
        elif self._drag_data["side"] == "top_right_corner":
            new_height = self.winfo_height() - (event.y_root - self._drag_data["abs_y"])
            new_width = self.winfo_width() + (event.x_root - self._drag_data["abs_x"])
            new_y = self.winfo_y() + (event.y_root - self._drag_data["abs_y"])
            self.geometry(f"{new_width}x{new_height}+{self.winfo_x()}+{new_y}")
            self._drag_data["abs_x"] = event.x_root
            self._drag_data["abs_y"] = event.y_root

            self.app_height = new_height
            self.app_width = new_width
            self.app_x = self.winfo_x()
            self.app_y =new_y



        elif self._drag_data["side"] == "bottom_left_corner":
            new_height = self.winfo_height() + (event.y_root - self._drag_data["abs_y"])
            new_width = self.winfo_width() - (event.x_root - self._drag_data["abs_x"])
            new_x = self.winfo_x() + (event.x_root - self._drag_data["abs_x"])
            self.geometry(f"{new_width}x{new_height}+{new_x}+{self.winfo_y()}")
            self._drag_data["abs_x"] = event.x_root
            self._drag_data["abs_y"] = event.y_root

            self.app_height = new_height
            self.app_width = new_width
            self.app_x =new_x
            self.app_y = self.winfo_y()

        




    def minimise_function(self):
        self.update_idletasks()
        self.overrideredirect(False)
        self.state("iconic")
        self.hasstyle = False
    def resize_button_function(self):
        if not self.size:
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()-50}+0+0")
            self.title_resize_button.config(text=" \u2752 ")
            self.size = True
        else:
            self.geometry(f"{self.app_width}x{self.app_height}+{self.app_x}+{self.app_y}")# update it
            self.title_resize_button.config(text=" \u25a0 ")

            self.size = False
    def on_drag(self,event):
        if not self.size:
            x = self.titleBar.winfo_pointerx() - self._drag_data["x"]
            y = self.titleBar.winfo_pointery() - self._drag_data["y"]
            self.geometry(f"+{x}+{y}")
            self.app_x = x 
            self.app_y = y 
        else:
            x = self.titleBar.winfo_pointerx() - self._drag_data["x"]
            y = self.titleBar.winfo_pointery() - self._drag_data["y"]
            self.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")
            self.title_resize_button.config(text=" \u25a0 ")
            self.size = False
            self.app_x = x 
            self.app_y = y 
        
    def on_click(self,event):
        self._drag_data["x"] = self.winfo_pointerx() - self.winfo_rootx()
        self._drag_data["y"] = self.winfo_pointery() - self.winfo_rooty()
        self._drag_data["abs_x"] = event.x_root
        self._drag_data["abs_y"] = event.y_root

    def Mapping(self,event=None):
        self.overrideredirect(True)
        self.update_idletasks()
        self.app_window()
        self.state("normal")
        self.force_foreground()
    def app_window(self):
        if not self.hasstyle:
            hmnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hmnd,self.GWL_EXSTYLE)
            style = style & ~self.WS_EX_TOOLWINDOW
            style = style | self.WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hmnd,self.GWL_EXSTYLE,style)
            self.withdraw()
            self.after(100,lambda:self.wm_deiconify())
            self.hasstyle = True
    def force_foreground(self):
        hmnd = windll.user32.GetParent(self.winfo_id())
        windll.user32.SetForegroundWindow(hmnd)
    def run(self):
        self.hasstyle = False
        self.update_idletasks()
        self.withdraw()
        self.app_window()
        self.mainloop()
if __name__ == "__main__":
    app = Window()
    app.run()
