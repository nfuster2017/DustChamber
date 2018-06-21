# import binhex
# Here Im importing all of the modules from libraries, and previously written code.
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
import RPi.GPIO as GPIO

# defining some global variables, as well as initialization
global root, F1OFF, F1ON
global settings, first, second, third, fourth, count
count = 1
first = 5
second = 5
third = 5
fourth = 5

root = tk.Tk()
global label
label = tk.Label(text="")
global tot, fan1, fan2, fan3, light, vacuum, alarm, tot_pos, vacuum_pos
light_pos = 35
fan1_pos = 40
fan2_pos = 38
fan3_pos = 36
tot_pos = 32
vacuum_pos = 37
# these are alarms, that will be configured when we startt doing the currency stuff
fan1 = False
fan2 = False
fan3 = False
light = False
tot = False
vacuum = False
alarm = False

# v=int()
# GPIO configuration

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light_pos, GPIO.OUT)
GPIO.setup(fan1_pos, GPIO.OUT)
GPIO.setup(fan2_pos, GPIO.OUT)
GPIO.setup(fan3_pos, GPIO.OUT)


# Timer Function, this is the setup for the time functions in the application
class Timer(Frame):
    global test_time, _start, seq_1, seq_2, seq_3

    # initializes some of the variables
    def __init__(self, parent=None, **kw):

        self.testing_time = 0
        Frame.__init__(self, parent, kw)
        alarm = False
        self._pausetime = 0
        self._start = 0
        self._elapsedtime = 0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()

    # warms up the totalizer and vaccum, *times need to be eventually set to 5 and 6mins

    def warm_ups(event):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(tot_pos, GPIO.OUT)
        GPIO.setup(vacuum_pos, GPIO.OUT)
        GPIO.output(tot_pos, 1)
        time.sleep(5)
        tot = 1
        print('Totalizer Warmed-up')
        GPIO.output(vacuum_pos, 1)
        time.sleep(5)
        print('Vacuum Stable')
        if tot == 1:
            tot_ready = Label(root, text='Totalizer ready')
            tot_ready.pack(side=TOP)
            print('works')
            tot += 1
        # return tot

    # this gets the user entries for test time
    def get_intentry(event):
        try:
            hrs_content = hrs_entry.get()
            min_content = min_entry.get()
            test_time = (int(hrs_content) * 3600) + (int(min_content) * 60)
            return test_time
        except:
            print('WHOOOOPS')
            # here we are forgeting about the entry boxes so they dont clog the screen

    def pack_f(self):

        hr_label.pack_forget()
        min_label.pack_forget()
        hrs_entry.pack_forget()
        min_entry.pack_forget()

    # setting up some of the visuals for the timer
    def makeWidgets(self):
        l = Label(self, textvariable=self.timestr, fg='green', bg='white', width=10, height=2)
        l.config(font=('Courier', 32))
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=YES, pady=2, padx=2)

    # this evokes some of the other functions and keeps the clock updating, using the after function
    def _update(self):

        self.testing_time = self.get_intentry()
        self._elapsedtime = self.testing_time - (time.time() - self._start) + self._pausetime
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    # sets up the time regex stuff
    def _setTime(self, elapsed):
        if self._elapsedtime >= 0:
            hours = int(elapsed / 3600)
            minutes = int(elapsed / 60) - (hours * 60)
            seconds = int(elapsed - int(elapsed / 60) * 60)
            if hours == 0 and minutes == 0 and seconds == 0:
                alarm = True
            self.timestr.set('%02d:%02d:%02d' % (hours, minutes, seconds))

    # function used when pressing start
    def Start(self):
        self._running = 1
        self.pack_f()
        self.testing_time = Timer.get_intentry
        self._start = time.time()
        self._update()
        print('Alvin swims like a seabass')

    # fucntions used for pause button, also tracks time was paused for to feed the elapsed time
    def Stop(self):
        # pause

        self.after_cancel(self._timer)
        self._pause = time.time()
        self.testing_time = self.testing_time - self._elapsedtime
        # self._elapsedtime = (self.testing_time - (time.time() - self._start))
        self._setTime(self._elapsedtime)
        self.after_cancel(self._timer)
        self.update()

        self._running = 0

    # does reset clock
    def Reset(self, ):
        # play
        # self._start=time.time()
        self.running = 1
        # self._start2 = time.time()-self._elapsedtime2
        self._pausetime = (time.time() - self._pause)
        print(self._pausetime)
        # self._elapsedtime +=(self._pause-time.time())
        self._setTime(self._elapsedtime)
        self._update()

    def get_elap(self):
        return self._elapsedtime


# some more global variable declaration

global f1Off, f1ON, f2OFF, f2ON, f3ON, f3OFF, Fan1_btn, Fan2_btn, Fan3_btn
f1ON = (5 * 60)
f1OFF = (5 * 60)
f2ON = (5 * 60)
f2OFF = (5 * 60)
f3ON = (5 * 60)
f3OFF = (5 * 60)


# this is the mnue for the settings

class fansettings(Frame):

    def __init__(self, parent=None, **kw):
        self.testing_time = 0
        Frame.__init__(self, parent, kw)

    def fan_settings(event=None):
        settings = tk.Tk()

        def fan_cycling():

            def first_round():
                first = seq_1.get()
                return first

            def second_round():
                second = seq_2.get()
                return second

            def third_round():
                third = seq_3.get()
                return third

            def fourth_round():
                fourth = seq_3.get()
                return fourth

            first_round()
            second_round()
            third_round()
            fourth_round()

        # toggle functions for turning fans on and off manually

        def toggle(tog=[0]):
            tog[0] = not tog[0]
            if tog[0]:
                Fan1_btn.config(text='ON')
                GPIO.output(fan1_pos, 1)


            else:
                Fan1_btn.config(text='OFF')
                GPIO.output(fan1_pos, 0)

        def toggle2(tog=[0]):
            tog[0] = not tog[0]
            if tog[0]:
                Fan2_btn.config(text='ON')
                GPIO.output(fan2_pos, 1)
            else:
                Fan2_btn.config(text='OFF')
                GPIO.output(fan2_pos, 0)

        def toggle3(tog=[0]):
            tog[0] = not tog[0]
            if tog[0]:
                Fan3_btn.config(text='ON')
                GPIO.output(fan3_pos, 1)
            else:
                Fan3_btn.config(text='OFF')
                GPIO.output(fan3_pos, 0)

        # tkinter applying for buttons
        Fan1_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle)
        Fan1_btn.pack(side=LEFT)

        Fan2_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle2)
        Fan2_btn.pack(side=LEFT)

        Fan3_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle3)
        Fan3_btn.pack(side=LEFT)

        seq_1 = tk.Spinbox(settings, from_=0, to=60, increment=1)
        seq_1.pack(side=TOP)
        seq_2 = tk.Spinbox(settings, from_=0, to=60, increment=1)
        seq_2.pack(side=TOP)
        seq_3 = tk.Spinbox(settings, from_=0, to=60, increment=1)
        seq_3.pack(side=TOP)
        seq_4 = tk.Spinbox(settings, from_=0, to=60, increment=1)
        seq_4.pack(side=TOP)

        Button(settings, text='Set Durations', command=fan_cycling).pack()

    # tkinter menu stuff

    menu = Menu(root)
    root.config(menu=menu)
    submen = Menu(menu)
    menu.add_cascade(label='settings', menu=submen)
    submen.add_command(label='Fan Durations', command=fan_settings)


# Fan sequence class *this is where we are currently stuck
class Fan_Stuff():
    # setting board up
    def Fan_sequence(self):
        GPIO.setup(fan1_pos, GPIO.OUT)
        GPIO.setup(fan2_pos, GPIO.OUT)
        GPIO.setup(fan3_pos, GPIO.OUT)

    # different fan outputs

    # We cannot constantly be checking to see if the time condition has changed because program will bug, How do we go about changing the sequence when the time has changed
    def sequence1(self):
        f1 = GPIO.output(fan1_pos, 1)
        f2 = GPIO.output(fan2_pos, 0)
        f3 = GPIO.output(fan3_pos, 0)
        print(fourth)
        return f1

    def sequence2(self):
        f1 = GPIO.output(fan1_pos, 0)
        f2 = GPIO.output(fan2_pos, 1)
        f3 = GPIO.output(fan3_pos, 0)

    def sequence3(self):
        f1 = GPIO.output(fan1_pos, 0)
        f2 = GPIO.output(fan2_pos, 0)
        f3 = GPIO.output(fan3_pos, 1)

    def sequence4(self):
        f1 = GPIO.output(fan1_pos, 1)
        f2 = GPIO.output(fan2_pos, 1)
        f3 = GPIO.output(fan3_pos, 0)

    # fanny_sequences=[sequence1(),sequence2(),sequence3(),sequence4()]
    # looping through the sequences
    def loop_fan(self):
        # xw.get_elap
        while sw.get_elap() > 0:
            # if sw.testing_time-first<=sw.get_elap():
            count = 1
            t1 = sw.get_elap() > sw.testing_time - first
            if sw.get_elap() > sw.testing_time - first:
                if f1 == GPIO.output(fan1_pos, 1):
                    print('seq1')
                    break
                else:
                    self.sequence1()
                    print('seq2')
                    break
            if t1 > sw.get_elap() > sw.testing_time - (count * (first + second)):
                self.sequence2()
                print('seq2')
            t2 = sw.testing_time - (count * (first + second))
            if t2 > sw.get_elap() > sw.testing_time - (count * (first + second + third)):
                self.sequence3()
                print('seq3')
            t3 = sw.testing_time - (count * (first + second + third))
            if t3 > sw.get_elap() > sw.testing_time - (count * (first + second + third + fourth)):
                self.sequence4()
                print('seq4')
            count += 1

            print('Mr Nicolas')
        '''       while Timer._elapsedtime != 0 or Timer._running != 0:
           seq1 = int(Timer._elapsedtime - first)
           while seq1 != int(Timer._elapsedtime):
               self.sequence1()
           seq2 = int(Timer._elapsedtime - second)
           while seq2 != int(Timer._elapsedtime):
               self.sequence2()
           seq3 = int(Timer._elapsedtime - third)
           while seq3 != int(Timer._elapsedtime):
               self.sequence3()
           seq4 = int(Timer._elapsedtime - fourth)
           while seq4 != int(Timer._elapsedtime):
               self.sequence4()
       print('Hola ')'''


# tkinter buttons for warm up and entry boxes
xw = Fan_Stuff()

warmup_button = Button(root, text='Commence Warm up')
warmup_button.pack()
warmup_button.bind('<Double-Button-1>', Timer.warm_ups)

hr_label = tk.Label(text="Hours:")
hr_label.pack(side=LEFT)
hrs_entry = tk.Spinbox(root, from_=0, to=8, increment=1)

hrs_entry.pack(side=LEFT)
min_label = tk.Label(text="Mins:")
min_label.pack(side=LEFT)
min_entry = tk.Spinbox(root, from_=0, to=60, increment=1)

min_entry.pack(side=LEFT)

# calling our timer class and packing it

sw = Timer(root)
sw.pack(side=TOP)

btext = 'Start/Reset'
star_reset = Button(root, text=btext, command=sw.Start)
star_reset.pack(side=LEFT)
Button(root, text='Fans Running', command=xw.loop_fan).pack()
pbutt = Button(root, text='Play', command=sw.Reset)
pbutt.pack(side=LEFT)

pause_but = Button(root, text='Pause', command=sw.Stop)
pause_but.pack(side=LEFT)

Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
if alarm == True:
    label = tk.Label(text="ALARM ALARM").pack()

root.mainloop()
GPIO.cleanup()
