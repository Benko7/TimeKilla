import tkinter as tk
from tkinter import ttk
from datetime import datetime, time

class TimeKillaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Time Killa")
        
        # Centering the window on the screen
        window_width = 400
        window_height = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Adding a big red title
        title_font = ("Helvetica", 24, "bold")
        self.label_title = ttk.Label(self.master, text="TIME KILLA", font=title_font, foreground="red")
        self.label_title.pack(pady=10)
        
        self.label_entry = ttk.Label(self.master, text="Enter minutes remaining:")
        self.label_entry.pack(pady=10)
        
        self.entry_minutes = ttk.Entry(self.master)
        self.entry_minutes.pack()
        
        self.button_start = ttk.Button(self.master, text="Start Time Killa", command=self.start_time_killa)
        self.button_start.pack(pady=10)
        
        self.checkboxes_frame = ttk.Frame(self.master)
        self.checkboxes_frame.pack(fill=tk.BOTH, expand=True)
        
        self.checkboxes = []
        self.minutes_remaining = 0
        
        self.make_draggable()
    
    def make_draggable(self):
        # Allows the window to be moved around the screen
        self.master.bind("<ButtonPress-1>", self.start_move)
        self.master.bind("<ButtonRelease-1>", self.stop_move)
        self.master.bind("<B1-Motion>", self.on_motion)
    
    def start_move(self, event):
        self.master.x = event.x
        self.master.y = event.y
    
    def stop_move(self, event):
        self.master.x = None
        self.master.y = None
    
    def on_motion(self, event):
        deltax = event.x - self.master.x
        deltay = event.y - self.master.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")
    
    def start_time_killa(self):
        try:
            self.minutes_remaining = int(self.entry_minutes.get())
            if self.minutes_remaining <= 0:
                raise ValueError("Minutes should be greater than 0")
            
            self.label_title.destroy()
            self.label_entry.destroy()
            self.entry_minutes.destroy()
            self.button_start.destroy()
            
            self.label_time = ttk.Label(self.master, text=f"{self.minutes_remaining} minutes left until 3:04 PM")
            self.label_time.pack(pady=10)
            
            self.scrollbar = ttk.Scrollbar(self.checkboxes_frame, orient=tk.VERTICAL)
            self.checklist = tk.Canvas(self.checkboxes_frame, yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.checklist.yview)
            
            for minute in range(1, self.minutes_remaining + 1):
                var = tk.IntVar()
                checkbox = ttk.Checkbutton(self.checklist, text=f"Minute {minute}", variable=var)
                self.checklist.create_window(0, minute * 25, anchor=tk.NW, window=checkbox)
                self.checkboxes.append((minute, var))
            
            self.checklist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.update_timer()
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def update_timer(self):
        remaining_checkboxes = sum(var.get() == 0 for _, var in self.checkboxes)
        
        if remaining_checkboxes > 0:
            self.label_time.config(text=f"{remaining_checkboxes} minutes left until 3:04 PM")
        else:
            self.label_time.config(text="HOODOOS LAD")
        
        # Check if all checkboxes are checked
        if remaining_checkboxes == 0:
            self.label_time.config(fg="green")
        
        self.master.after(1000, self.update_timer)

def main():
    root = tk.Tk()
    app = TimeKillaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
