import tkinter as tk
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