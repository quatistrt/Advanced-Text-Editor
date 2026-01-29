import customtkinter as ctk
import tkinter as tk
import sys
import psutil
from editor_core.ui_components import Sidebar, EditorTabs, StatusBar
from editor_core.theme_manager import ThemeManager
from editor_core.terminal import SimpleTerminal

class AntigravityEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QuatisYT Editor")
        self.geometry("1200x800")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        self.header = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.sidebar = Sidebar(self, width=250, corner_radius=0, file_callback=self.open_file)
        self.sidebar.grid(row=1, column=0, rowspan=2, sticky="nsew")

        self.editor_tabs = EditorTabs(self)
        self.editor_tabs.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10, 0))

        self.terminal = SimpleTerminal(self, height=150, corner_radius=0)
        self.terminal.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        self.terminal_visible = True

        self.statusbar = StatusBar(self)
        self.statusbar.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.create_header_buttons()
        
        self.zen_mode = False

        self.bind("<Control-s>", lambda e: self.editor_tabs.save_current_file())
        self.bind("<Control-k>", self.wait_for_second_key)
        self.bind("<Control-grave>", self.toggle_terminal)
        
        self.change_theme("Dracula")

        self.update_system_stats()

    def create_header_buttons(self):
        file_btn = ctk.CTkOptionMenu(
            self.header, 
            values=["Dosya", "Yeni", "Aç", "Kaydet", "Çıkış"],
            command=self.handle_file_menu,
            width=80
        )
        file_btn.pack(side="left", padx=5, pady=5)
        file_btn.set("Dosya")

        theme_btn = ctk.CTkOptionMenu(
            self.header, 
            values=ThemeManager.list_themes(), 
            width=120,
            command=self.change_theme
        )
        theme_btn.pack(side="left", padx=5, pady=5)
        theme_btn.set("Dracula")

        view_btn = ctk.CTkOptionMenu(
            self.header, 
            values=["Görünüm", "Odak", "Terminal Aç/Kapa"], 
            command=self.handle_view_menu,
            width=100
        )
        view_btn.pack(side="left", padx=5, pady=5)
        view_btn.set("Görünüm")

        help_btn = ctk.CTkOptionMenu(
            self.header,
            values=["Yardım"],
            command=self.handle_help_menu,
            width=80
        )
        help_btn.pack(side="left", padx=5, pady=5)
        help_btn.set("Yardım")

        producer_btn = ctk.CTkButton(
            self.header,
            text="Yapımcı",
            width=80,
            command=self.show_producer_info,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        producer_btn.pack(side="left", padx=5, pady=5)
        
        self.zen_btn = ctk.CTkButton(self.header, text="Odak", command=self.toggle_zen_mode, fg_color="#E91E63", hover_color="#C2185B", width=80)
        self.zen_btn.pack(side="right", padx=10, pady=5)

    def show_producer_info(self):
        msg = "Yapımcı: quatisytt\nDiscord: quatisytt"
        tk_msg = tk.messagebox.showinfo("Yapımcı Bilgisi", msg)

    def handle_file_menu(self, choice):
        if choice == "Çıkış":
            self.destroy()
        elif choice == "Kaydet":
            self.editor_tabs.save_current_file()
        elif choice == "Aç":
            path = ctk.filedialog.askopenfilename()
            if path:
                self.open_file(path)
        elif choice == "Yeni":
            self.editor_tabs.new_file()
        
        file_menu = self.header.winfo_children()[0]
        if isinstance(file_menu, ctk.CTkOptionMenu):
            file_menu.set("Dosya")
    
    def handle_view_menu(self, choice):
        if choice == "Odak":
            self.toggle_zen_mode()
        elif choice == "Terminal Aç/Kapa":
            self.toggle_terminal()
            
        view_menu = self.header.winfo_children()[2]
        if isinstance(view_menu, ctk.CTkOptionMenu):
            view_menu.set("Görünüm")

    def handle_help_menu(self, choice):
        if choice == "Yardımcı":
            print("Yardımcı başlatılıyor...")
        
        help_menu = self.header.winfo_children()[3]
        if isinstance(help_menu, ctk.CTkOptionMenu):
            help_menu.set("Yardım")

    def change_theme(self, theme_name):
        theme_data = ThemeManager.get_theme(theme_name)
        self.editor_tabs.apply_theme(theme_data)

    def open_file(self, path):
        self.editor_tabs.open_file(path)
        self.statusbar.set_status(f"Opened: {path}")

    def wait_for_second_key(self, event):
        self.bind("<z>", self.toggle_zen_mode_event)

    def toggle_zen_mode_event(self, event=None):
        self.toggle_zen_mode()
        self.unbind("<z>") 

    def toggle_zen_mode(self):
        self.zen_mode = not self.zen_mode
        
        if self.zen_mode:
            self.header.grid_remove()
            self.sidebar.grid_remove()
            self.statusbar.grid_remove()
            self.terminal.grid_remove()
            
            self.grid_columnconfigure(0, weight=0) 
            self.editor_tabs.grid(row=0, column=0, columnspan=2, rowspan=4, sticky="nsew", padx=0, pady=0)
        else:
            self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.sidebar.grid(row=1, column=0, rowspan=2, sticky="nsew")
            self.statusbar.grid(row=3, column=0, columnspan=2, sticky="ew")
            
            self.grid_columnconfigure(0, weight=0)
            self.editor_tabs.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10, 0))
            if self.terminal_visible:
                self.terminal.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        
    def toggle_terminal(self, event=None):
        self.terminal_visible = not self.terminal_visible
        if self.terminal_visible:
            self.terminal.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        else:
            self.terminal.grid_remove()

    def update_system_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        self.statusbar.update_stats(cpu, ram)
        self.after(2000, self.update_system_stats)

if __name__ == "__main__":
    app = AntigravityEditor()
    app.mainloop()
