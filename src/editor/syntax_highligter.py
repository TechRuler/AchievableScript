import tkinter as tk
import builtins
import re
import importlib

class SyntaxHighlighter:
    def __init__(self, master=None):
        self.master = master 
        
        
        self.keywords = ['and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 
                         'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 
                         'while', 'with', 'yield']
        self.constants = ['False', 'None', 'True']
        self.builtins = set(dir(builtins))
        self.user_defined_elements = set()  # Store user-defined functions and classes
        self.imported_modules = {}  # Dictionary to store imported modules and their aliases
    def configures(self,method="purple",number="blue",operator="red",circle_brackets="blue",square_brackets="yellow",curlly_brackets="purple",variable_in_parameter="tomato",variables="black",decorator="purple",self_color="blue",keyword="blue",constant="purple",builtin="orange",string="green",comment="red",definition="purple",class_definition="purple"):
        # Configure tags for highlighting
        self.master.tag_configure('keyword', foreground=keyword)
        self.master.tag_configure('constant', foreground=constant)
        self.master.tag_configure('self', foreground=self_color)
        # self.master.tag_configure('parameter', foreground=variable_in_parameter)
        # self.master.tag_configure('variable', foreground=variables)
        self.master.tag_configure('special', foreground=keyword)
        self.master.tag_configure('builtin', foreground=builtin)
        self.master.tag_configure('method', foreground=method)
        self.master.tag_configure('number', foreground=number)
        self.master.tag_configure('oparators',foreground=operator)
        self.master.tag_configure('circle',foreground=circle_brackets)
        self.master.tag_configure('square',foreground=square_brackets)
        self.master.tag_configure('curlly',foreground=curlly_brackets)
        self.master.tag_configure('comment', foreground=comment)
        self.master.tag_configure('string', foreground=string)
        self.master.tag_configure('user_def', foreground=definition)  # New tag for user-defined elements
        self.master.tag_configure('class', foreground=class_definition)
        self.master.tag_configure("variable", foreground="cyan")
        

         # self.text_widget.tag_configure('module', foreground='brown')
        # self.text_widget.tag_configure('user_module', foreground='darkorange')  # New tag for user-defined modules
        
        self.auto_coloring = True

        # Bind the virtual event to the toggle function
        self.master.bind('<<toggle-auto-coloring>>', self.toggle_auto_coloring)
        
        # Start the periodic syntax highlighting
        self.update_highlighting()

    def toggle_auto_coloring(self, event=None):
        self.auto_coloring = not self.auto_coloring
        if self.auto_coloring:
            self.update_highlighting()

    def update_highlighting(self):
        if self.auto_coloring:
            self.highlight_syntax()
            # Schedule the next update in 500 ms (0.5 seconds)
            self.master.after(500, self.update_highlighting)

    def highlight_syntax(self):
        content = self.master.get("1.0", tk.END)
        self.master.mark_set("range_start", "1.0")
        
        # Clear existing tags
        self.clear_tags()
        
        # Tokenize for comments and strings first
        self.tokenize_comments_and_strings(content)
        
        # Tokenize for keywords, builtins, and numbers
        self.tokenize_keywords_builtins_numbers(content)
        
        # Tokenize for function and class definitions
        self.tokenize_definitions(content)

        # Tokenize for imported modules
        self.tokenize_imports(content)
        
        # Highlight imported module aliases throughout the file
        self.highlight_imported_modules(content)

        self.tokenize_variables(content)

    def clear_tags(self):
        tags = ['keyword', 'constant',"variable", 'self','circle','square','curlly','oparators' ,'special', 'builtin', 'method', 'number', 'comment', 'string', 'module', 'user_module', 'user_def', 'class']
        for tag in tags:
            self.master.tag_remove(tag, '1.0', tk.END)

    def tokenize_comments_and_strings(self, content):
        in_string = False
        string_start = None
        string_type = None
        lines = content.splitlines()
        for line_no, line in enumerate(lines):
            pos = 0
            while pos < len(line):
                if not in_string:
                    if line[pos:pos+3] in ["'''", '"""']:
                        in_string = True
                        string_start = pos
                        string_type = line[pos:pos+3]
                        pos += 3
                    elif line[pos] in ["'", '"']:
                        in_string = True
                        string_start = pos
                        string_type = line[pos]
                        pos += 1
                    elif line[pos] == '#':
                        comment_start = pos
                        self.apply_tag(f"{line_no + 1}.{comment_start}", f"{line_no + 1}.{len(line)}", 'comment')
                        break
                    else:
                        pos += 1
                else:
                    if line[pos:pos+3] == string_type:
                        in_string = False
                        self.apply_tag(f"{line_no + 1}.{string_start}", f"{line_no + 1}.{pos+3}", 'string')
                        pos += 3
                    elif line[pos] == string_type:
                        in_string = False
                        self.apply_tag(f"{line_no + 1}.{string_start}", f"{line_no + 1}.{pos+1}", 'string')
                        pos += 1
                    else:
                        pos += 1
            if in_string:
                self.apply_tag(f"{line_no + 1}.{string_start}", f"{line_no + 2}.0", 'string')
                string_start = 0
            else:
                string_start = None
                string_type = None

    def tokenize_keywords_builtins_numbers(self, content):
        token_specification = [
            ('keyword',   r'\b(?:' + '|'.join(self.keywords) + r')\b'),  # Keywords
            ('constant',   r'\b(?:' + '|'.join(self.constants) + r')\b'),  # Constants
            ('builtin',   r'\b(?:' + '|'.join(self.builtins) + r')\b'),  # Built-in functions and constants
            ('number',    r'\b\d+(\.\d*)?\b'),      # Integer or decimal number
            ('method',    r'\b\w+(?=\(\s*)'),
            ('self',      r'\bself\b'),
            # ('parameter', r'\(([^=,\s]+)|,\s*([^=,\s]+)'),
            # ('variable',  r'\b[A-Za-z_]\w+(?=\s*=\s*)'),
            ('circle',    r'[\(\)]'),
            ('square',    r'[\[\]]'),
            ('curlly',    r'[\{\}]'),
            ('oparators', r'[\*\+\-\%=]'),
        ]
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        
        lines = content.splitlines()
        for line_no, line in enumerate(lines):
            for mo in re.finditer(tok_regex, line):
                kind = mo.lastgroup
                start, end = mo.span(kind)
                self.apply_tag(f"{line_no + 1}.{start}", f"{line_no + 1}.{end}", kind)
    
        
    def tokenize_definitions(self, content):
        def_pattern = re.compile(r'^\s*(def)\s+([a-zA-Z_]\w*)', re.MULTILINE)
        class_pattern = re.compile(r'^\s*(class)\s+([a-zA-Z_]\w*)', re.MULTILINE)
        
        for def_match in def_pattern.finditer(content):
            def_name = def_match.group(2)
            self.user_defined_elements.add(def_name)
            start, end = def_match.span(2)
            self.apply_tag(f"{self.get_index(start, content)}", f"{self.get_index(end, content)}", 'user_def')
        
        for class_match in class_pattern.finditer(content):
            class_name = class_match.group(2)
            self.user_defined_elements.add(class_name)
            start, end = class_match.span(2)
            self.apply_tag(f"{self.get_index(start, content)}", f"{self.get_index(end, content)}", 'class')

    def tokenize_imports(self, content):
        import_pattern = re.compile(r'^\s*(import|from)\s+([a-zA-Z_][\w\S+.]*)(?:\s+as\s+([a-zA-Z_]\w*))?', re.MULTILINE)
        import_elements_pattern = re.compile(r'^\s*from\s+[a-zA-Z_][\w.]*\s+import\s+([a-zA-Z_]\w*(?:,\s*[a-zA-Z_]\w*)*)', re.MULTILINE)

        for import_match in import_pattern.finditer(content):
            module_name = import_match.group(2)
            alias_name = import_match.group(3)
            
            # Highlight the main module
            start, end = import_match.span(2)
            if self.is_module_installed(module_name.split('.')[0]):
                self.apply_tag(f"{self.get_index(start, content)}", f"{self.get_index(end, content)}", 'module')
                if alias_name:
                    self.imported_modules[alias_name] = module_name
                else:
                    self.imported_modules[module_name] = module_name
            else:
                self.apply_tag(f"{self.get_index(start, content)}", f"{self.get_index(end, content)}", 'module')
                if alias_name:
                    self.imported_modules[alias_name] = module_name
                else:
                    self.imported_modules[module_name] = module_name

            # Highlight the alias
            if alias_name:
                alias_start, alias_end = import_match.span(3)
                self.apply_tag(f"{self.get_index(alias_start, content)}", f"{self.get_index(alias_end, content)}", 'module')

        for import_elements_match in import_elements_pattern.finditer(content):
            elements = import_elements_match.group(1).split(',')
            for element in elements:
                element = element.strip()
                element_start = content.find(element, import_elements_match.start())
                element_end = element_start + len(element)
                self.apply_tag(f"{self.get_index(element_start, content)}", f"{self.get_index(element_end, content)}", 'module')

    def highlight_imported_modules(self, content):
        for alias in self.imported_modules.keys():
            pattern = re.compile(r'\b' + re.escape(alias) + r'\b')
            lines = content.splitlines()
            for line_no, line in enumerate(lines):
                for mo in pattern.finditer(line):
                    start, end = mo.span()
                    self.apply_tag(f"{line_no + 1}.{start}", f"{line_no + 1}.{end}", 'module')

    def is_module_installed(self, module_name):
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False

    def apply_tag(self, start, end, tag):
        self.master.tag_add(tag, start, end)

    def get_index(self, pos, content):
        """Convert a character position to a Tkinter text index."""
        lines = content[:pos].splitlines()
        line_no = len(lines)
        char_pos = len(lines[-1]) if lines else 0
        return f"{line_no}.{char_pos}"

if __name__ == "__main__":
    root = tk.Tk()
    
    text_widget = tk.Text(root, wrap='word', undo=True)
    text_widget.pack(expand=True, fill='both')
    text_widget.config(font=("Consolas", 15))

    app = SyntaxHighlighter(master=text_widget)
    app.configures()

    # Example of toggling the auto-coloring on and off
    # def toggle_coloring(event):
    #     app.master.event_generate('<<toggle-auto-coloring>>')

    # app.master.bind('<Control-c>', toggle_coloring)
    
    root.mainloop()
