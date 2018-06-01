import tkinter as tk
from timerfunction import *
class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.clock()
        Timer(self.root)
        self.root.configure(background='black')
        sw = Timer(self.root)
        sw.pack(side=TOP)
        Button(self.root, text='Start', command=sw.Start).pack(side=LEFT)
        Button(self.root, text='Stop', command=sw.Stop).pack(side=LEFT)
        Button(self.root, text='Reset', command=sw.Reset).pack(side=LEFT)
        Button(self.root, text='Quit', command=self.root.quit).pack(side=RIGHT)
        self.root.mainloop()

    def clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.after(1000, self.clock)

App()