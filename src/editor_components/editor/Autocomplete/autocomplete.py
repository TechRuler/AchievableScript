import tkinter as tk
import jedi 
from src.widgets.scrollbar import AutoScrollbar
from src.editor_components.editor.Autocomplete.custom_listbox import PopUp
from src.editor_components.editor.syntax_highlighter.syntax_highligter import SyntaxHighlighter
class Autocomplete(tk.Frame):
    def __init__(self, master,*arg, **kwarg):
        tk.Frame.__init__(self, master, *arg, **kwarg)
        self.master = master
        

        self.autocomplete_bool = False
        
        self.pop_up_y = 22
        self.pop_up = PopUp(self.master)
        self.pop_up.place_forget()

        self.calltip_popup = tk.Toplevel(self)
        self.calltip_popup.withdraw()
        self.calltip_popup.wm_overrideredirect(True)
        self.calltip_popup.wm_attributes("-topmost", 1)
        self.scrollbar = AutoScrollbar(self.calltip_popup, orient="vertical")
        self.calltip_label = tk.Text(self.calltip_popup, background="lightyellow", height=6, borderwidth=1, state="disabled", cursor="arrow", wrap="word",border=0, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.calltip_label.yview)
        self.scrollbar.grid(row=0,column=1,sticky="ns")
        self.calltip_label.grid(row=0,column=0,sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        

        self.detail_calltip_popup = tk.Toplevel(self)
        self.detail_calltip_popup.withdraw()
        self.detail_calltip_popup.wm_overrideredirect(True)
        self.detail_calltip_popup.wm_attributes("-topmost", 1)
        self.detail_scrollbar = AutoScrollbar(self.detail_calltip_popup, orient="vertical")
        self.detail_calltip_label = tk.Text(self.detail_calltip_popup, background="lightblue", height=10, width=40, borderwidth=0, state="disabled", cursor="arrow", wrap="word", yscrollcommand=self.detail_scrollbar.set)
        self.detail_scrollbar.config(command=self.detail_calltip_label.yview)
        self.detail_scrollbar.grid(row=0,column=1,sticky="ns")
        self.detail_calltip_label.grid(row=0,column=0,sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)


        self.syntax1 = SyntaxHighlighter(master=self.calltip_label)
        self.syntax2 = SyntaxHighlighter(master=self.detail_calltip_label)

    def change_y(self, y):
        self.pop_up_y = y

    def get_cursor_position(self):
        cursor_index = self.master.index(tk.INSERT)
        line, column = map(int, cursor_index.split('.'))
        return line, column

    def on_key_release(self, event=None):
        code = self.master.get("1.0", "end-1c")
        line, column = self.get_cursor_position()
        script = jedi.Script(code)

        try:
            completions = script.complete(line, column)
            self.autocomplete_function(completions)
            call_signatures = script.get_signatures(line, column)
            self.show_calltip(call_signatures)
        except Exception as e:
            self.hide_autocomplete()
            self.hide_calltip()
            self.hide_detail_calltip()

    def autocomplete_function(self, completions):
        word = self.master.get("insert -1c wordstart", "insert -1c wordend")
        line_text = self.master.get("insert linestart", "insert")
        bbox = self.master.bbox("insert")
        if bbox:
            x, y, _, _ = bbox

        # Check the character before the cursor position
        char_before = self.master.get("insert -1c", "insert")

        if line_text.strip() == "" or line_text.lstrip().startswith("#") or char_before in "()[]{} ":
            self.hide_autocomplete()
            return

        data = [i.name for i in completions ]
        if not data:
            self.hide_autocomplete()
            return

        new_suggestion = len(data)
        # print(data)
        height = min(new_suggestion * 35, 200)

        self.pop_up.place_configure(x=x, y=(y + self.pop_up_y), height=height, width=300)
        self.autocomplete_bool = True
        self.pop_up.delete()
        for i in data:
            self.pop_up.insert(text=i)
        self.pop_up.select_set(0)
        self.update_detail_calltip()

    def hide_autocomplete(self, event=None):
        self.pop_up.place_forget()
        self.autocomplete_bool = False
        self.hide_detail_calltip()

    def show_calltip(self, call_signatures):
        if call_signatures:
            calltip = call_signatures[0].docstring()
            bbox = self.master.bbox("insert")
            if bbox:
                x, y, width, height = bbox
                x += self.master.winfo_rootx()
                y += self.master.winfo_rooty()

                screen_height = self.winfo_screenheight()
                calltip_height = self.calltip_label.winfo_reqheight()

                if y + height + calltip_height + self.pop_up_y > screen_height:
                    y -= (calltip_height + self.pop_up_y + height)
                else:
                    y -= (calltip_height)
                if calltip_height <= 6:
                    print(calltip_height)
                    self.calltip_label.configure(height=calltip_height)
                else:
                    self.calltip_label.configure(height=6)

                self.calltip_label.configure(state="normal")
                self.calltip_label.delete("1.0", "end")
                self.calltip_label.insert("1.0", calltip)
                self.calltip_label.configure(state="disabled")
                self.calltip_popup.geometry(f"+{x}+{y}")
                self.calltip_popup.deiconify()
        else:
            self.hide_calltip()

    def hide_calltip(self):
        self.calltip_popup.withdraw()
    def update_detail_calltip(self, event=None):
        if self.autocomplete_bool:
            try:
                selected_item = self.pop_up.selection_get()
                script = jedi.Script(self.master.get("1.0", "end-1c"))
                completions = script.complete(*self.get_cursor_position())
                for comp in completions:
                    if comp.name == selected_item:
                        docstring = comp.docstring()
                        if docstring.strip():
                            self.detail_calltip_label.configure(state="normal")
                            self.detail_calltip_label.delete("1.0", "end")
                            self.detail_calltip_label.insert("1.0", docstring)
                            self.detail_calltip_label.configure(state="disabled")

                            bbox = self.master.bbox("insert")
                            if bbox:
                                x, y, width, height = bbox
                                x += self.master.winfo_rootx()
                                y += self.master.winfo_rooty() + 25

                                self.detail_calltip_popup.geometry(f"+{x + 300}+{y}")
                                self.detail_calltip_popup.deiconify()
                                
                        else:
                            self.hide_detail_calltip()
            except tk.TclError:
                pass

    def hide_detail_calltip(self):
        self.detail_calltip_popup.withdraw()


    def add_option_to_master(self, event=None):
        if self.autocomplete_bool:
            self.master.delete("insert -1c wordstart", "insert -1c wordend")
            self.master.insert("insert", self.pop_up.selection_get())
            self.hide_autocomplete()
            return 'break'


if __name__ == "__main__":
    def enter(event=None):
        if auto_complet.autocomplete_bool:
            auto_complet.add_option_to_master()
            auto_complet.place_forget()
        else:
            editor.insert("insert","\n")
            editor.see("insert")
        return "break"
    root = tk.Tk()

    editor = tk.Text(root,font=("Consolas",15),bg="grey20",fg="white",insertbackground="white") 
    editor.pack()
    auto_complet = Autocomplete(master=editor)

    auto_complet.pop_up.add_command_for_element = enter
    editor.bind("<KeyRelease>",auto_complet.on_key_release)
    editor.bind("<Return>",enter)



    root.mainloop()