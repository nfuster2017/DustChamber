from tkinter import *
import time
class Timer(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0
        self._elapsedtime = 0
        self._running = False
        self.timestr = StringVar()
        self.makeWidgets()
    def _setTime(self, elapsed):
        minutes = int(elapsed / 60)
        seconds = int(elapsed - minutes * 60)
        hundredths = int((elapsed - ((minutes * 60) + seconds)) * 100)
        self.timestr.set('%02d:%02d.%02d' % (minutes, seconds, hundredths))
    def makeWidgets(self):
        l = Label(self, textvariable=self.timestr, fg='green', bg='black', width=10, height=2)
        l.config(font=('Courier', 32))
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)
    def _update(self):
        testing_time=10
        self._elapsedtime = testing_time - (time.time() - self._start)
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    def _setTime(self, elapsed):
        if self._elapsedtime>=0:
            hours= int(elapsed/3600)
            minutes = int(elapsed / 60)
            seconds = int(elapsed - minutes * 60)
            self.timestr.set('%02d:%02d:%02d' % (hours,minutes, seconds))
    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0
    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
def main():
    root = Tk()
    root.configure(background='black')
    sw = Timer(root)
    sw.pack(side=TOP)
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    root.mainloop()
if __name__ == '__main__':
    main()