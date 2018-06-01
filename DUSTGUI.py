import tkinter as tk
import time


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.update_clock()
        self.set_timer()
        self.remaining = 0
        self.countdown(10)
        self.root.mainloop()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

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