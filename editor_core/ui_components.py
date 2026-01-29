import customtkinter as ctk
import os
from datetime import datetime
from editor_core.text_editor import AdvancedEditor

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, file_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_callback = file_callback
        self.current_path = os.getcwd()
        
        self.logo_label = ctk.CTkLabel(self, text="Antigravity", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.dir_btn = ctk.CTkButton(self, text="Klasör Aç", command=self.open_folder_dialog)
        self.dir_btn.pack(padx=20, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Dosyalar")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_file_tree()

    def open_folder_dialog(self):
        folder = ctk.filedialog.askdirectory()
        if folder:
            self.current_path = folder
            self.refresh_file_tree()

    def refresh_file_tree(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            items = os.listdir(self.current_path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(self.current_path, x)), x.lower()))

            for item in items:
                path = os.path.join(self.current_path, item)
                is_dir = os.path.isdir(path)
                icon = "📁 " if is_dir else "📄 "
                
                btn = ctk.CTkButton(
                    self.scroll_frame, 
                    text=f"{icon}{item}", 
                    fg_color="transparent", 
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30"),
                    anchor="w",
                    command=lambda p=path: self.on_item_click(p)
                )
                btn.pack(fill="x", padx=5, pady=2)
        except Exception as e:
            print(f"Error reading directory: {e}")

    def on_item_click(self, path):
        if os.path.isdir(path):
            self.current_path = path
            self.refresh_file_tree()
        else:
            if self.file_callback:
                self.file_callback(path)

class EditorTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.editors = {} 
        self.current_theme = None
        self.untitled_count = 0

    def open_file(self, path):
        filename = os.path.basename(path)
        
        if path in self.editors:
            self.set(filename)
            return

        self.add(filename)
        self.set(filename)

        editor = AdvancedEditor(self.tab(filename), file_path=path, theme=self.current_theme)
        editor.pack(fill="both", expand=True)
        
        self.editors[path] = editor
        
    def new_file(self):
        self.untitled_count += 1
        filename = f"Adsız{self.untitled_count}"
        
        self.add(filename)
        self.set(filename)
        
        editor = AdvancedEditor(self.tab(filename), file_path=None, theme=self.current_theme)
        editor.pack(fill="both", expand=True)
        
        self.editors[f"::{filename}"] = editor 

    def save_current_file(self):
        try:
            current_tab_name = self.get()
            target_path = None
            editor_widget = None
            
            for path, widget in self.editors.items():
                if path == f"::{current_tab_name}": 
                    editor_widget = widget
                    target_path = ctk.filedialog.asksaveasfilename(defaultextension=".txt")
                    if target_path:
                        del self.editors[path]
                        self.editors[target_path] = widget
                        
                        # Rename tab (destroy and recreate tab usually needed in ctk, but we might just update title if possible. 
                        # CTKTabview doesn't support easy renaming. We will just save content.)
                        # For simplicity, we just save and log.
                        pass
                    break
                elif os.path.basename(path) == current_tab_name:
                    target_path = path
                    editor_widget = widget
                    break
            
            if target_path and editor_widget:
                content = editor_widget.get("0.0", "end-1c")
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Saved: {target_path}")
        except Exception as e:
            print(f"Save error: {e}")

    def apply_theme(self, theme_data):
        self.current_theme = theme_data 
        for editor in self.editors.values():
            editor.apply_theme(theme_data)

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        
        self.info_label = ctk.CTkLabel(self, text="Ready", font=("Arial", 12))
        self.info_label.pack(side="left", padx=10)
        
        self.stats_label = ctk.CTkLabel(self, text="CPU: 0% | RAM: 0%", font=("Arial", 12))
        self.stats_label.pack(side="right", padx=10)

    def set_status(self, text):
        self.info_label.configure(text=text)
    
    def update_stats(self, cpu, ram):
        self.stats_label.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
