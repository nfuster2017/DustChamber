import tkinter as tk
from timerfunction import *
import RPi.GPIO as GPIO
from warmup import *

class App():
    def __init__(self):
        #Timer.alarm==False
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.clock()
        Button(self.root, text='Commence Warm up',command=self.warmups()).pack()
        #warmup_button.pack_forget()
        Timer(self.root)
        #Timer._setTime()
        self.root.configure(background='black')
        sw = Timer(self.root)
        sw.pack(side=TOP)
        Entry(self.root).pack(side=LEFT)
        Button(self.root, text='Start', command=sw.Start).pack(side=LEFT)
        Button(self.root, text='Stop', command=sw.Stop).pack(side=LEFT)
        Button(self.root, text='Reset', command=sw.Reset).pack(side=LEFT)
        Button(self.root, text='Quit', command=self.root.quit).pack(side=RIGHT)
        '''if Timer.alarm== True:
            self.root.destroy()
            self.label = tk.Label(text="ALARM ALARM")
            self.label.pack()'''
        self.root.mainloop()

    def clock(self):
        now = time.strftime("%H:%M")
        self.label.configure(text=now)
        self.root.after(1000, self.clock)
        #self.root.destroy()

    def warmups(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        GPIO.setup(41, GPIO.OUT)
        GPIO.output(40, 1)
        time.sleep(1)
        GPIO.output(41, 1)
        time.sleep(1)


App()