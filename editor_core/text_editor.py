import customtkinter as ctk
import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_for_filename, PythonLexer
from pygments.styles import get_style_by_name

class AdvancedEditor(ctk.CTkTextbox):
    def __init__(self, master, file_path=None, **kwargs):
        theme_data = kwargs.pop("theme", None) 
        super().__init__(master, **kwargs)
        self.file_path = file_path
        self.font_size = 14
        self.configure(font=("Consolas", self.font_size))
        
        self.text_widget = self._textbox 
        
        self.apply_theme(theme_data)

        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<Control-MouseWheel>", self.change_font_size)

        if self.file_path:
            self.load_file()

    def apply_theme(self, theme_data=None):
        if not theme_data:
            theme_data = {
                "fg": "#f8f8f2", "bg": "#282a36", "select": "#44475a",
                "keyword": "#ff79c6", "func": "#50fa7b", "string": "#f1fa8c", "comment": "#6272a4"
            }
        
        self.configure(text_color=theme_data["fg"], fg_color=theme_data["bg"])
        self.tag_colors = {
            'Token.Keyword': theme_data["keyword"],
            'Token.Name.Function': theme_data["func"],
            'Token.Literal.String': theme_data["string"],
            'Token.Comment': theme_data["comment"],
            'Token.Name.Class': theme_data["func"],
            'Token.Operator': theme_data["keyword"],
        }
        
        for token_type, color in self.tag_colors.items():
            self.text_widget.tag_config(str(token_type), foreground=color)
        
        self.highlight_syntax()

    def load_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.delete("0.0", "end")
            self.insert("0.0", content)
            self.highlight_syntax()
        except Exception as e:
            self.insert("0.0", f"Error: {e}")

    def on_key_release(self, event=None):
        if event.keysym in ['Return', 'space', 'BackSpace', 'Delete'] or event.char in [':', '(', ')']:
            self.highlight_syntax()

    def highlight_syntax(self):
        content = self.get("0.0", "end-1c")
        
        for tag in self.tag_colors.keys():
            self.text_widget.tag_remove(str(tag), "1.0", "end")

        try:
            if self.file_path:
                lexer = get_lexer_for_filename(self.file_path)
            else:
                lexer = PythonLexer()
        except:
            lexer = PythonLexer()

        self.text_widget.mark_set("range_start", "1.0")
        
        for token, text in lex(content, lexer):
            self.text_widget.mark_set("range_end", f"range_start + {len(text)} chars")
            
            token_str = str(token)
            
            tag_to_apply = None
            if token_str in self.tag_colors:
                tag_to_apply = token_str
            elif "Keyword" in token_str:
                tag_to_apply = 'Token.Keyword'
            elif "String" in token_str:
                tag_to_apply = 'Token.Literal.String'
            elif "Comment" in token_str:
                tag_to_apply = 'Token.Comment'
            elif "Function" in token_str:
                tag_to_apply = 'Token.Name.Function'
            
            if tag_to_apply:
                self.text_widget.tag_add(tag_to_apply, "range_start", "range_end")
            
            self.text_widget.mark_set("range_start", "range_end")

    def change_font_size(self, event):
        if event.delta > 0:
            self.font_size += 1
        else:
            self.font_size = max(8, self.font_size - 1)
        
        self.configure(font=("Consolas", self.font_size))
        return "break"
