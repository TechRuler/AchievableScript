import tkinter.filedialog as tf 
def Read(file):
    with open(file,"r",encoding='utf-8') as f:
        content = f.read()
    return content
def Write(file,widget):
    with open(file,"w",encoding='utf-8') as f:
        content = widget.get("1.0","end")
        f.write(content)
