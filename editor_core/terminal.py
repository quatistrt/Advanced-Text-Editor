import customtkinter as ctk
import subprocess
import threading
import queue
import os

class SimpleTerminal(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.output_text = ctk.CTkTextbox(self, font=("Consolas", 12), activate_scrollbars=True)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        self.output_text.configure(state="disabled")

        self.input_entry = ctk.CTkEntry(self, font=("Consolas", 12))
        self.input_entry.grid(row=1, column=0, sticky="ew")
        self.input_entry.bind("<Return>", self.run_command)

        self.process = None
        self.queue = queue.Queue()
        self.reading = False

        self.print_output("Terminal Ready\n")

    def print_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", text)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def run_command(self, event):
        command = self.input_entry.get()
        self.input_entry.delete(0, "end")
        
        if not command.strip():
            return

        self.print_output(f"> {command}\n")

        if command.strip() == "clear":
            self.output_text.configure(state="normal")
            self.output_text.delete("0.0", "end")
            self.output_text.configure(state="disabled")
            return
        
        if command.startswith("cd "):
            try:
                dest = command[3:].strip()
                os.chdir(dest)
                self.print_output(f"Changed directory to: {os.getcwd()}\n")
            except Exception as e:
                self.print_output(f"Error: {e}\n")
            return

        threading.Thread(target=self._execute_external, args=(command,), daemon=True).start()

    def _execute_external(self, command):
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.stdout:
                self.queue.put(result.stdout)
            if result.stderr:
                self.queue.put(result.stderr)
                
            self.after(0, self._process_queue)
        except Exception as e:
            self.queue.put(f"Error executing command: {e}\n")
            self.after(0, self._process_queue)

    def _process_queue(self):
        try:
            while True:
                line = self.queue.get_nowait()
                self.print_output(line)
                if not line.endswith("\n"):
                    self.print_output("\n")
        except queue.Empty:
            pass
