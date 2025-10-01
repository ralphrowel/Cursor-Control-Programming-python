import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import CursorControl  # your backend scanner

class CursorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cursor Control Program")
        self.running = False
        self.thread = None

        # --- Buttons ---
        self.start_btn = tk.Button(root, text="Start", command=self.start)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        # --- Log window ---
        self.log_area = scrolledtext.ScrolledText(root, width=50, height=15, state=tk.DISABLED)
        self.log_area.pack(padx=10, pady=10)

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def run_backend(self):
        self.log("Backend started...")
        while self.running:
            try:
                CursorControl.scan_and_act()
            except Exception as e:
                self.log(f"Error: {e}")
            time.sleep(CursorControl.SEARCH_INTERVAL)
        self.log("Backend stopped.")

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_backend, daemon=True)
            self.thread.start()
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)

    def stop(self):
        if self.running:
            self.running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CursorUI(root)
    root.mainloop()
