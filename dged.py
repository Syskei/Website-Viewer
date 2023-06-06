import time
import random
import tkinter as tk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import filedialog

# Set up Brave browser options
options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Path to Brave browser executable
options.add_argument("--incognito")  # Open in incognito mode

# Define the list of website URLs to choose from
websites = [
    "https://example.example.com",
    "https://example.example.com",
    "https://example.example.com"
    # Add more URLs as needed
]

# Set the duration of execution in seconds (4 hours = 4 * 60 * 60 seconds)
duration = 4 * 60 * 60

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Opener")
        self.geometry("400x300")
        self.configure(bg="#000000")
        self.resizable(False, False)

        # Create a canvas widget for the gradient background
        self.canvas = tk.Canvas(self, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create GUI elements
        self.urls_frame = tk.Frame(self.canvas, bg="#000000")
        self.urls_label = tk.Label(self.urls_frame, text="URLs to visit:", font=("Arial", 12), bg="#000000", fg="white")
        self.urls_text = tk.Text(self.urls_frame, height=5, width=40, font=("Arial", 10), bg="#666666", fg="white")
        self.urls_text.insert(tk.END, "\n".join(websites))
        self.clear_button = tk.Button(self.urls_frame, text="Clear URLs", command=self.clear_urls, font=("Arial", 10), bg="#666666", fg="white")
        self.save_button = tk.Button(self.urls_frame, text="Save", command=self.save_text, font=("Arial", 10), bg="#666666", fg="white")
        self.load_button = tk.Button(self.urls_frame, text="Load", command=self.load_text, font=("Arial", 10), bg="#666666", fg="white")

        self.timer_label = tk.Label(self.canvas, text="Time remaining:", font=("Arial", 12), bg="#000000", fg="white")
        self.timer_value = tk.Label(self.canvas, text="", font=("Arial", 14, "bold"), bg="#000000", fg="white")
        self.counter_label = tk.Label(self.canvas, text="Windows opened:", font=("Arial", 12), bg="#000000", fg="white")
        self.counter_value = tk.Label(self.canvas, text="0", font=("Arial", 14, "bold"), bg="#000000", fg="white")

        self.play_button = tk.Button(self.canvas, text="▶️ Play", command=self.start_execution, font=("Arial", 12), bg="#666666", fg="white", justify='center')
        self.stop_button = tk.Button(self.canvas, text="⏹ Stop", command=self.stop_execution, font=("Arial", 12), bg="#666666", fg="white", justify='center')
        self.subtract_hour_button = tk.Button(self.canvas, text="-1hr", command=self.subtract_hour, font=("Arial", 12), bg="#666666", fg="white", justify='center')
        self.add_hour_button = tk.Button(self.canvas, text="+1hr", command=self.add_hour, font=("Arial", 12), bg="#666666", fg="white", justify='center')

        # Grid layout
        self.urls_frame.grid(row=0, padx=10, pady=10, columnspan=2)
        self.urls_label.grid(row=0, column=0, sticky=tk.W)
        self.urls_text.grid(row=1, column=0, padx=5, pady=5)
        self.clear_button.grid(row=1, column=1, padx=5, pady=5)
        self.save_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.load_button.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

        self.timer_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.timer_value.grid(row=1, column=1, padx=10, pady=5, sticky=tk.E)
        self.counter_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.counter_value.grid(row=2, column=1, padx=10, pady=5, sticky=tk.E)

        self.play_button.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10, sticky=tk.E)
        self.subtract_hour_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.add_hour_button.grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)

        # Set the initial values
        self.remaining_time = duration
        self.windows_opened = 0
        self.is_executing = False
        self.execution_thread = None

        # Update the time remaining and windows opened labels
        self.update_labels()

        # Bind the canvas resize event to update the gradient background
        self.canvas.bind("<Configure>", self.update_canvas)

    def clear_urls(self):
        self.urls_text.delete("1.0", tk.END)

    def start_execution(self):
        if not self.is_executing:
            self.is_executing = True
            self.play_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.urls_text.config(state=tk.DISABLED)
            self.subtract_hour_button.config(state=tk.DISABLED)
            self.add_hour_button.config(state=tk.DISABLED)

            # Get the URLs from the text box
            websites.clear()
            websites.extend(self.urls_text.get("1.0", tk.END).strip().split("\n"))

            # Start the execution in a separate thread
            self.execution_thread = Thread(target=self.execute_websites)
            self.execution_thread.start()
            self.start_timer()  # Start the timer

    def stop_execution(self):
        if self.is_executing:
            self.is_executing = False
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.urls_text.config(state=tk.NORMAL)
            self.subtract_hour_button.config(state=tk.NORMAL)
            self.add_hour_button.config(state=tk.NORMAL)

    def subtract_hour(self):
        self.remaining_time = max(0, self.remaining_time - 3600)
        self.update_labels()

    def add_hour(self):
        self.remaining_time += 3600
        self.update_labels()

    def start_timer(self):
        self.timer_thread = Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while self.is_executing and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_labels()
            time.sleep(1)  # Wait for 1 second

        if self.is_executing:
            self.stop_execution()

    def execute_websites(self):
        start_time = time.time()
        while self.is_executing and (time.time() - start_time) <= self.remaining_time:
            website = random.choice(websites)
            self.open_website(website)
            self.windows_opened += 1
            self.update_labels()
            time.sleep(1)  # Wait for 1 second between opening websites

        self.is_executing = False
        self.play_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.urls_text.config(state=tk.NORMAL)
        self.subtract_hour_button.config(state=tk.NORMAL)
        self.add_hour_button.config(state=tk.NORMAL)

    def open_website(self, url):
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(5)  # Wait for 5 seconds to simulate viewing the website
            driver.quit()
        except Exception as e:
            print("Error opening website:", e)

    def update_labels(self):
        remaining_hours = self.remaining_time // 3600
        remaining_minutes = (self.remaining_time % 3600) // 60
        remaining_seconds = self.remaining_time % 60

        self.timer_value.config(text=f"{remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}")
        self.counter_value.config(text=str(self.windows_opened))

    def save_text(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w") as file:
                file.write(self.urls_text.get("1.0", tk.END))

    def load_text(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "r") as file:
                content = file.read()
                self.urls_text.delete("1.0", tk.END)
                self.urls_text.insert(tk.END, content)

    def update_canvas(self, event):
        self.canvas.delete("gradient")
        width = event.width
        height = event.height
        for i in range(height):
            r = hex(int(255 - i / height * 255))[2:].zfill(2)
            g = hex(int(255 - i / height * 255))[2:].zfill(2)
            b = hex(int(255 - i / height * 255))[2:].zfill(2)
            color = f"#{r}{g}{b}"
            self.canvas.create_line(0, i, width, i, tags=("gradient"), fill=color)

if __name__ == "__main__":
    app = Application()
    app.mainloop()