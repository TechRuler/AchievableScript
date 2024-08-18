import tkinter as tk
from tkinter import ttk

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
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")

    # Create a style
    style = ttk.Style()

    # Configure the style for Vertical.TScrollbar and Horizontal.TScrollbar
    style.configure("Vertical.TScrollbar",
                    background="lightblue",
                    troughcolor="darkblue",
                    arrowcolor="blue")
    style.configure("Horizontal.TScrollbar",
                    background="lightblue",
                    troughcolor="darkblue",
                    arrowcolor="blue")

    frame = tk.Frame(root)
    frame.pack(expand=True,fill="both")

    text = tk.Text(frame, wrap=tk.NONE)
    text.grid(row=0, column=0, sticky='nsew')

    v_scrollbar = AutoScrollbar(frame, orient=tk.VERTICAL, command=text.yview, style="Vertical.TScrollbar")
    v_scrollbar.grid(row=0, column=1, sticky='ns')

    h_scrollbar = AutoScrollbar(frame, orient=tk.HORIZONTAL, command=text.xview, style="Horizontal.TScrollbar")
    h_scrollbar.grid(row=1, column=0, sticky='ew')

    text.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Configure grid weights to make sure text widget expands properly
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Fill the text widget with enough content to require scrolling
    for i in range(100):
        text.insert(tk.END, f"Line {i}\n")
    for i in range(50):
        text.insert(tk.END, f"Column {i} ")

    root.mainloop()