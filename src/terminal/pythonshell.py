import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import subprocess
import threading
class AutoScrollbar(ttk.Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)
    
    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')
class LineNumber(tk.Canvas):
    def __init__(self,*arg,**kwarg):
        tk.Canvas.__init__(self,*arg,**kwarg,highlightthickness=0)
        self.text_widget = None
        self.font = ("Consolas",10)
        self.foreground = "black"
    def changefont(self,font):
        self.font = font 
    def changefg(self,foreground):
        self.foreground = foreground
    def attach(self,text_widget):
        self.text_widget = text_widget
    def redraw(self,event=None):
        self.delete("all")

        a = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(a)
            if not dline:break
            y = dline[1]
            line_number = str(a).split(".")[0]
            self.create_text(2,y,anchor="nw",text=line_number,fill=self.foreground,font=self.font)
            a = self.text_widget.index("%s + 1line"%a)
class PythonShell(tk.Frame):
    def __init__(self,*arg,**kwarg):
        tk.Frame.__init__(self,*arg,**kwarg)
        self.file = ""
        self.process = None
        self.prompt = ""
        self.output = tk.Text(self)
        self.output.grid(row=0,column=1,sticky="nsew")
        self.output.tag_configure("output",foreground="grey")
        self.output.tag_configure("error",foreground="red")
        self.output.tag_configure("saved",foreground="spring green")
        self.vertical_scroll = AutoScrollbar(self,orient=tk.VERTICAL, command=self.output.yview)
        self.vertical_scroll.grid(row=0, column=2, sticky='ns',rowspan=2)
        self.output.configure(yscrollcommand=self.vertical_scroll.set)
        self.output_line = LineNumber(self,width=55)
        self.output_line.grid(row=0,column=0,sticky="ns")
        self.output_line.attach(self.output)
        

        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.output.bind("<Button-1>",lambda event=None:self.refresh_line_number())
        self.output.bind("<MouseWheel>",lambda event=None:self.refresh_line_number())
        self.output.bind("<Key>",lambda event=None:self.refresh_line_number())
        self.output.bind("<Return>",lambda event=None:self.on_enter_key_click())
    def on_enter_key_click(self):
        self.refresh_line_number()
        command = self.output.get("insert linestart", "insert lineend").strip()
        self.run_command(command)
    def refresh_line_number(self):
        self.after(2,self.output_line.redraw)
    def change(self,file):
        self.file = file 
    def run_code(self,file, event=None):
        self.file = file 
        if self.file:
            if self.file.endswith(".py"):
                command = f'python "{self.file}"'
                self.run_command(command)
            else:
                self.output.insert("end", "No file selected to run.\n", "error")
                self.output.see("end")
            self.refresh_line_number()
        return "break"
    def run_command(self, command):
        try:
            self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, bufsize=1, universal_newlines=True)
            if self.output.index("insert") != self.output.index("insert linestart"):
                self.output.insert("end", f"\nRunning {self.file}...\n", "info")
            else:
                self.output.insert("end", f"Running {self.file}...\n", "info")
            self.output.see("end")

                    # Start threads to read stdout and stderr
            threading.Thread(target=self.read_output).start()
            threading.Thread(target=self.read_error).start()

                    # Bind Enter key to send input to the process
            self.output.bind("<Return>", self.send_input)
        except Exception as e:
            self.output.insert("end", f"An error occurred: {e}\n", "error")
            self.output.see("end")
        
    def read_output(self):
        while True:
            output_char = self.process.stdout.read(1)
            if output_char:
                self.output.insert("end", output_char, "output")
                self.output.see("end")
                if output_char == ":" and self.output.get("end-2c")[-1] == " ":
                    self.prompt += output_char
                    self.wait_for_input()
                else:
                    self.prompt += output_char
            else:
                break
        self.refresh_line_number()

    def read_error(self):
        while True:
            error_line = self.process.stderr.readline()
            if error_line:
                self.output.insert("end", error_line, "error")
                self.output.see("end")
            else:
                break
        self.refresh_line_number()
        

    def wait_for_input(self):
        self.output.insert("end", "\n", "input")
        self.output.focus_set()
    def get_last_line(self):
        lines = self.prompt.splitlines()
        if lines:
            return lines[-1]
        return ""
    def send_input(self, event=None):
        self.prompt = self.get_last_line()
        input_text = self.output.get("insert linestart", "insert lineend").replace(self.prompt, "").strip() + "\n"
        self.process.stdin.write(input_text)
        self.process.stdin.flush()
        self.output.insert("end", "\n", "input")
        self.output.see("end")
        self.prompt = ""# Reset the prompt after sending input
        self.refresh_line_number()

        return "break"
