import tkinter as tk
from tkinter import ttk
from timerfunction import *
import RPi.GPIO as GPIO
global root
root= tk.Tk()
global label
label = tk.Label(text="")
global tot, fan1, fan2, fan3,light,vacuum, alarm,tot_pos,vacuum_pos
light_pos= 35
fan1_pos= 36
fan2_pos = 37
fan3_pos = 38
tot_pos=20
vacuum_pos=21
fan1=False
fan2=False
fan3=False
light=False
tot= False
vacuum= False
alarm= False
#GPIO configuration

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(fan1, GPIO.OUT)
GPIO.setup(fan2, GPIO.OUT)
GPIO.setup(fan3, GPIO.OUT)

def clock():
    now = time.strftime("%H:%M")
    time_clock=label.configure(text=now)
    root.after(1000, clock)

def warm_ups(event):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    GPIO.setup(41, GPIO.OUT)
    GPIO.output(40, 1)
    time.sleep(1)
    tot=1
    print('Totalizer Warmed-up')
    GPIO.output(41, 1)
    time.sleep(1)
    print('Vacuum Stable')
    if tot==1:
        tot_ready=Label(root, text='Totalizer ready')
        tot_ready.pack(side=TOP)
        print('works')
    #return tot
warmup_button=Button(root, text='Commence Warm up')
warmup_button.pack()
warmup_button.bind('<Double-Button-1>', warm_ups)
sw = Timer(root)



clock()
sw.pack(side=TOP)
hr_label = tk.Label(text="Hours:").pack(side=LEFT)
hrs_entry=Entry(root)
hrs_entry.pack(side=LEFT)
min_label = tk.Label(text="Mins:").pack(side=LEFT)
min_entry=Entry(root)
min_entry.pack(side=LEFT)
def get_test_time(h_entry,m_entry):

    hrs_content =h_entry.get()
    min_content =m_entry.get()
    #test_time=(hrs_content,min_content)
    #return test_time
    return hrs_content,min_content
submitBtn = ttk.Button(root, text='Submit')
submitBtn.bind('<Button-1>', get_test_time(hrs_entry,min_entry))
submitBtn.pack(side=LEFT)



Button(root, text='Start', command=sw.Start).pack(side=LEFT)
Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
if Timer.alarm== True:
    label = tk.Label(text="ALARM ALARM").pack()

root.mainloop()

