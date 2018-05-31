import tkinter as tk
import time


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.update_clock()
        self.set_timer()
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def set_timer(self):
        set_time = tk.Button(self.root, text="Set timer")
        test_time = tk.Entry()
        test_time.pack()
        set_time.pack()


app=App()