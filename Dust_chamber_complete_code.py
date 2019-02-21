# import binhex
# Here Im importing all of the modules from libraries, and previously written code.
import tkinter as tk
from tkinter import *
import serial
from tkinter import ttk
import time
from smbus import SMBus
import smbus

import RPi.GPIO as GPIO
import threading as TR
# defining some global variables, as well as initialization
global root, F1OFF, F1ON
global settings,count,ser #first, second, third, fourth, count
count = 1
#first = 5
#second = 5
#third = 5
#fourth = 5

ser = serial.Serial( port='/dev/ttyUSB0', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

root = tk.Tk()
#root.geometry("1000x300")
#root.columnconfigure(3,weight=1)
#root.grid_rowconfigure(3,weight=0)

global label
label = tk.Label(text="")
global tot, fan1, fan2, fan3, light, vacuum, alarm, tot_pos, vacuum_pos
light_pos = 35
fan1_pos = 40
fan2_pos = 38
fan3_pos = 36
fan4_pos=  22
fan5_pos=18
fan6_pos=16
tot_pos = 32
vacuum_pos = 37




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light_pos, GPIO.OUT)
GPIO.setup(fan1_pos, GPIO.OUT)
GPIO.setup(fan2_pos, GPIO.OUT)
GPIO.setup(fan3_pos, GPIO.OUT)
GPIO.setup(fan4_pos, GPIO.OUT)
GPIO.setup(fan5_pos, GPIO.OUT)
GPIO.setup(fan6_pos, GPIO.OUT)


# Timer Function, this is the setup for the time functions in the application
class Timer(Frame):
    global test_time, _start, seq_1, seq_2, seq_3

    # initializes some of the variables
    def __init__(self, parent=None, **kw):
        self.qq=Fan_Stuff()
        self.testing_time = 0
        Frame.__init__(self, parent, kw)
        alarm = False
        self._pausetime = 0
        self._start = 0
        self._elapsedtime = 0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()
        self.tot_vol_display=StringVar()
        self.tot_val_display=StringVar()
        self.am_Iwarm=0
        self.playstart=0
        self._pause=0
        self.timepassed=0
        self.paused=True
        self.pausedtime=0

    # warms up the totalizer and vaccum, *times need to be eventually set to 5 and 6mins

    def warm_ups(self):
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(tot_pos, GPIO.OUT)
        GPIO.setup(vacuum_pos, GPIO.OUT)
        GPIO.output(tot_pos, 1)
        #time.sleep(60*6)#here we add 6mins
        tot = 1
        print('Totalizer Warmed-up')
        GPIO.output(vacuum_pos, 1)
        #time.sleep(60*5)#here we add 5 more mins
        print('Vacuum Stable')
        if tot == 1:
            print('ready')
            wbut.grid_forget()
            min_entry.grid(row=0,column=1,sticky='w')
            min_label.grid(row=0,column=0,sticky='w')
            hrs_entry.grid(row=1,column=1,sticky='w')
            hr_label.grid(row=1,column=0,sticky='w')
            #tot_val_L.grid(row=3,column=0,sticky='nsew')
            #tot_vol_L.grid(row=2,column=0,sticky='nsew')
            tot_vol_display.grid(row=4,column=0,sticky='w')
            tot_val_display.grid(row=5,column=0,sticky='w')
            temp_Val.grid(row=2,column=0,sticky='w')
            hum_Val.grid(row=3,column=0,sticky='w')
            sw.grid(row=0,column=0,sticky='w')
            star_reset.grid(row=1,column=0,sticky='w')
            Vac_btn.grid(row=5,column=0,sticky='w')
            light_btn.grid(row=6,column=0,sticky='w')
            pause_but.grid(row=2,column=0,sticky='w')
            tot += 1
            self.am_Iwarm=1

    # this gets the user entries for test time
    def get_intentry(event):
        try:
            hrs_content = hrs_entry.get()
            min_content = min_entry.get()
            test_time = (int(hrs_content) * 3600) + (int(min_content) * 60)
            return test_time
        except:
            print('WHOOOOPS')
            

    # setting up some of the visuals for the timer
    def makeWidgets(self):
        l = Label(self, textvariable=self.timestr, fg='blue', bg='white', width=20, height=2,borderwidth=1,relief="solid")
        l.config(font=('Courier', 22),anchor='center')
        self._setTime(self._elapsedtime)
        l.grid(row=0,column=0)

    # this evokes some of the other functions and keeps the clock updating, using the after function
    def _update(self):

        if self._running==0:
            self._elapsedtime=self.testing_time
        if self._running==1:
            timnow=time.time()
            
            self._elapsedtime =self.testing_time-( timnow-self.playstart)  
        self._setTime(self._elapsedtime)
        self._timer = self.after(150, self._update)

    # sets up the time regex stuff
    def _setTime(self, elapsed):
        if elapsed<0:
            self.Stop()
        else:
            hours = int(elapsed / 3600)
            minutes = int(elapsed / 60) - (hours * 60)
            seconds = int(elapsed - int(elapsed / 60) * 60)
            self.timestr.set('%02d:%02d:%02d' % (hours, minutes, seconds))

    # function used when pressing start
    def Start(self):
        #set
        self.testing_time = self.get_intentry()
        self._running = 0
    #start time should be iniated with play
        self.timepassed=0
        self._update()
        pbutt.grid(row=0,column=0,sticky='nsew')


    # fucntions used for pause button, also tracks time was paused for to feed the elapsed time
    def Stop(self):
        # pause
        if self._running==1:
            self._running = 0
            self._pause = time.time()
            self.testing_time =self.testing_time-(self._pause-self.playstart)
            self.update()
            xw.state=0


    # does reset clock
    def Reset(self):
        # play
        self._running = 1
        self.playstart=time.time()
        xw.Test_start=time.time()
        self.pausedtime=self.playstart-self._pause
        xw.Test_start= time.time() #+self.pausedtime
        xw.tiempo=time.time()+5
        
        
        self._update()

    def get_elap(self):
        return self._elapsedtime


# some more global variable declaration




# this is the mnue for the settings
class fansettings(Frame):
    #settings = tk.Tk()
    def __init__(self, parent=None, **kw):
        self.testing_time = 0
        Frame.__init__(self, parent, kw)
        self.get_first=3
        self.get_second=3
        self.get_third=.5
        self.get_fourth=3
        self.Dset=0
        self.seq_1=DoubleVar()
        self.seq_2=DoubleVar()
        self.seq_3=DoubleVar()
        self.seq_4=DoubleVar()

        
        



#set durations
    def fan_cycling(self):
        self.get_first = int(self.seq_1.get())

        self.get_second = int(self.seq_2.get())

        self.get_third = int(self.seq_3.get())

        self.get_fourth = int(self.seq_4.get())
        print(self.get_first) 


        

    def fan_settings(self):
        settings = tk.Tk()
        self.seq_1 = tk.Spinbox(settings, from_=1.0, to=60.0, increment=1)
        self.seq_1.grid(row=0,column=3)
        s1L=tk.Label(settings,text='Sequence One:')
        s1L.grid(row=0,column=0)
        self.seq_2 = tk.Spinbox(settings, from_=1, to=60, increment=1)
        self.seq_2.grid(row=5,column=3)
        tk.Label(settings,text='Sequence Two:').grid(row=5,column=0)
        self.seq_3 = tk.Spinbox(settings, from_=1, to=60, increment=1)
        self.seq_3.grid(row=8,column=3)
        tk.Label(settings,text='Sequence Three:').grid(row=8,column=0)
        self.seq_4 = tk.Spinbox(settings, from_=1, to=60, increment=1)
        self.seq_4.grid(row=11,column=3)
        tk.Label(settings,text='Sequence Four:').grid(row=11,column=0)
        set_cycl=Button(settings, text='Set Durations', command=fx.fan_cycling)
        set_cycl.grid(row=15,column=3)
class Totalizer():
    def __init__(self, parent=None, **kw):
        self.totx=StringVar()
    def command_tot(self):
        
        com=self.cmd_entry.get()
        moc=str.encode(com)
        new=bytes(moc+(b'\r\n'))
        ser.write(new)
        time.sleep(.5)
        reading=ser.readline()
        time.sleep(.5)
    def zero(self):
        zeros=str.encode('T,Z')
        newzero=bytes(zeros+(b'\r\n'))
        ser.write(newzero)
        zeroreading=ser.readline()

 
    def tot_command(self):
        self.tot_menu=Tk()
        self.tot_menu.geometry=("5000x200")
        self.cmd_entry=Entry(self.tot_menu)
        self.cmd_entry.grid(row=0,column=0) 
        cmdenter=Button(self.tot_menu, text='Enter',command=tot.command_tot)
        cmdenter.grid(row=2,column=0)
        zero_but=Button(self.tot_menu,text='Zero',command=tot.zero)
        zero_but.grid(row=4,column=0)
        
tot=Totalizer()
fx=fansettings()
menu = Menu(root)
root.config(menu=menu)
submen = Menu(menu)
menu.add_cascade(label='settings', menu=submen)
submen.add_command(label='Fan Durations', command=fx.fan_settings)
submen.add_command(label='Totalizer', command=tot.tot_command)

Frame1=Frame(root)

def toggle(tog=[0]):
    tog[0] = not tog[0]
    if tog[0]:
        Vac_btn.config(text='VAC ON',bg='green')
        GPIO.output(vacuum_pos, 1)
    else:
        Vac_btn.config(text='VAC OFF',bg= 'red')
        GPIO.output(vacuum_pos, 0)
Vac_btn = tk.Button(Frame1, text="VAC ON", width=5, height=2, command=toggle)
        # toggle functions for turning fans on and off manually
'''def toggle(tog=[0]):
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
                GPIO.output(fan3_pos, 0)'''

        # tkinter applying for buttons
'''Fan1_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle)
        Fan1_btn.pack(side=LEFT)

        Fan2_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle2)
        Fan2_btn.pack(side=LEFT)

        Fan3_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle3)
        Fan3_btn.pack(side=LEFT)'''

'''class fansettings(Frame):

    def __init__(self, parent=None, **kw):
        self.testing_time = 0
        Frame.__init__(self, parent, kw)
        self.settings = tk.Tk()
 # tkinter applying for buttons
       
    def settings(event=None):
        settings=tk.Tk()
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

        Fan1_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle)
        Fan1_btn.grid(row=0,column=0)
        Fan2_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle2)
        Fan2_btn.grid(row=0,column=1)
        Fan3_btn = tk.Button(settings, text="OFF", width=5, height=2, command=toggle3)
        Fan3_btn.grid(row=0,column=2)
        '''

 
# Fan sequence class
class Fan_Stuff():
    #Whew=fansettings()
    def __init__(self, parent=None, **kw):
        self.state=IntVar()
        self.tiempo=0
        self.xseq1=(60*fx.get_first)
        self.xseq2=(60*fx.get_second)
        self.xseq3=(60*fx.get_third)
        self.xseq4=(60*fx.get_fourth)
        self.Test_start=time.time()

    # different fan outputs

    # We cannot constantly be checking to see if the time condition has changed because program will bug, How do we go about changing the sequence when the time has changed
    def sequence1(self):
        self.state=1
        self.tiempo=time.time()+30
        if sw._running==1:
            f1 = GPIO.output(fan1_pos, 1)
            f2 = GPIO.output(fan2_pos, 1)
            f3 = GPIO.output(fan3_pos, 1)
            f4 =GPIO.output(fan4_pos,1)
            f5=GPIO.output(fan5_pos,0)
            f6=GPIO.output(fan6_pos,0)
    def sequence2(self):
        self.tiempo=time.time()+30
        self.state=2
        if sw._running==1:
            f1 = GPIO.output(fan1_pos, 1)
            f2 = GPIO.output(fan2_pos, 1)
            f3 = GPIO.output(fan3_pos, 1)
            f4 =GPIO.output(fan4_pos,1)
            f5=GPIO.output(fan5_pos,0)
            f6=GPIO.output(fan6_pos,0)        
    def sequence3(self):
        self.tiempo=time.time()+30
        self.state=3
        if sw._running==1:
            f1 = GPIO.output(fan1_pos, 0)
            f2 = GPIO.output(fan2_pos, 0)
            f3 = GPIO.output(fan3_pos, 0)
            f4 =GPIO.output(fan4_pos,0)
            f5=GPIO.output(fan5_pos,1)
            f6=GPIO.output(fan6_pos,1)

    def sequence4(self):        
        self.tiempo=time.time()+30
        self.state=4
        if sw._running==1:
            f1 = GPIO.output(fan1_pos, 1)
            f2 = GPIO.output(fan2_pos, 1)
            f3 = GPIO.output(fan3_pos, 1)
            f4 =GPIO.output(fan4_pos,1)
            f5=GPIO.output(fan5_pos,1)
            f6=GPIO.output(fan6_pos,1)
    

    # looping through the sequences with conditionals based on the idea that 
    def loop_fan(self):
        self.Test_start=time.time()
        while True:
            self.xseq1=(60*fx.get_first)
            self.xseq2=(60*fx.get_second)
            self.xseq3=(60*fx.get_third)
            self.xseq4=(60*fx.get_fourth)
            time.sleep(1)
            if sw._running==1:
                if time.time()< xw.Test_start + (xw.xseq1):
                    formertime=(xw.Test_start+ (xw.xseq1))
                    xw.sequence1()
                if time.time()< (xw.Test_start+(xw.xseq1) +(xw.xseq2)) and time.time()>xw.Test_start+(xw.xseq1):
                    formertime= xw.Test_start+(xw.xseq1)+ (xw.xseq2)
                    xw.sequence2()
                if time.time()<( xw.Test_start+ (xw.xseq1)+ (xw.xseq2)+(xw.xseq3))and time.time()>(xw.Test_start+(xw.xseq1) +(xw.xseq2)):
                    formertime= xw.Test_start+ (xw.xseq3)+(xw.xseq1)+ (xw.xseq2)
                    xw.sequence3()
                if time.time()< xw.Test_start+(xw.xseq1)+ (xw.xseq2)+(xw.xseq3)+ (xw.xseq4)and time.time()> xw.Test_start+ (xw.xseq1)+ (xw.xseq2)+(xw.xseq3):
                    xw.sequence4()
                if time.time()>xw.Test_start+(xw.xseq1)+ (xw.xseq2)+(xw.xseq3)+ (xw.xseq4):
                    xw.Test_start=time.time()

            if sw._running==0:
                GPIO.output(fan1_pos, 0)
                GPIO.output(fan2_pos, 0)
                GPIO.output(fan3_pos, 0)
                GPIO.output(fan4_pos, 0)
                GPIO.output(fan5_pos, 0)
                GPIO.output(fan6_pos, 0)
                time.sleep(2)
            if sw._running==3:
                time.sleep(.5)
                continue 
                
# initalizing some class instances meant for manipulation 
Frame2=Frame(root)
Frame3=Frame(root)
Frame4=Frame(root)
Frame5=Frame(root)
Frame6=Frame(root)
sw = Timer(Frame3)
xw = Fan_Stuff()

# tkinter buttons for warm up and entry boxes

warm_up_tr=TR.Thread(target=sw.warm_ups)

wbut=Button(root, text='Warm up(11min)', command=warm_up_tr.start,fg='Blue',bg='white')
wbut.config(font=('Courier', 32))
wbut.grid(row=2,column=2)

hr_label = tk.Label(Frame4,text="Hours:")
hrs_entry = tk.Spinbox(Frame5, from_=0, to=8,width=3, increment=1)
min_label = tk.Label(Frame4,text="Mins:")
min_entry = tk.Spinbox(Frame5, from_=0, to=60,width=3, increment=1)




#buttons for fans if we ever want to implement 

'''seq_1 = tk.Spinbox(b.settings, from_=0, to=60, increment=1)
seq_1.grid(row=1,column=0)       
seq_2 = tk.Spinbox(b.settings, from_=0, to=60, increment=1)
seq_2.grid(row=1,column=2)
seq_3 = tk.Spinbox(b.settings, from_=0, to=60, increment=1)
seq_3.grid(row=1,column=3)                
seq_4 = tk.Spinbox(b.settings, from_=0, to=60, increment=1)
seq_4.grid(row=1,column=3) 
Fan1_btn = tk.Button(b.settings, text="OFF", width=5, height=2, command=b.toggle)
Fan1_btn.grid(row=0,column=0)
Fan2_btn = tk.Button(b.settings, text="OFF", width=5, height=2, command=b.toggle2)
Fan2_btn.grid(row=0,column=1)
Fan3_btn = tk.Button(b.settings, text="OFF", width=5, height=2, command=b.toggle3)
Fan3_btn.grid(row=0,column=2)'''

# calling our timer class and packing it

#framing


x=TR.Thread(target=xw.loop_fan).start()
btext = 'Set Test Time'
star_reset = Button(Frame1, text=btext, command=sw.Start)
star_reset.configure(font=('Courier',12,'bold'))
pbutt = Button(Frame1, text='Play', command=sw.Reset)
pbutt.configure(font=('Courier',12,'bold'))
pause_but = Button(Frame1, text='Pause', command=sw.Stop)
pause_but.configure(font=('Courier',12,'bold'))

# current detection       **** need to tune this for proper current detection, numbers currently rough estimate ****
def current_sensor():
    bus =SMBus(1)
    bus.write_byte(0x48,1)
    count_sensor=0
    max_reading=1
    error_reading=False 
    time.sleep(5)
    popped=0
    fanerrors=[]
    while True:
        reading=bus.read_byte(0x48)
        time.sleep(.01)
        if sw._running==1:
            if error_reading== True:
                sw._running=3
                
                #proccess of elimination
                
                f1 = GPIO.output(fan1_pos, 1)
                f2 = GPIO.output(fan2_pos, 0)
                f3 = GPIO.output(fan3_pos, 0)
                f4 =GPIO.output(fan4_pos,0)
                f5=GPIO.output(fan5_pos,0)
                f6=GPIO.output(fan6_pos,0) 
                time.sleep(10)
                count_sensor=0
                
                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)
                    
                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        if max_reading>194:
                            print('Fan 1 working',max_reading)
                            count_sensor=0
                            break
                            
                        else:
                            print('Fan 1 not pulling current',max_reading)
                            fanerrors.append('Fan One')
                            break
                            
                f1 = GPIO.output(fan1_pos, 0)
                f2 = GPIO.output(fan2_pos, 1)
                f3 = GPIO.output(fan3_pos, 0)
                f4 =GPIO.output(fan4_pos,0)
                f5=GPIO.output(fan5_pos,0)
                f6=GPIO.output(fan6_pos,0) 
                time.sleep(10)
                count_sensor=0
                max_reading=0
                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)

                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        print(max_reading)
                        if max_reading>194:
                            print('Fan 2 working',max_reading)
                            count_sensor=0
                            break

                        else:
                            print('Fan 2 not pulling current',max_reading)
                            fanerrors.append('Fan Two')

                            break

                f1 = GPIO.output(fan1_pos, 0)
                f2 = GPIO.output(fan2_pos, 0)
                f3 = GPIO.output(fan3_pos, 1)
                f4 =GPIO.output(fan4_pos,0)
                f5=GPIO.output(fan5_pos,0)
                f6=GPIO.output(fan6_pos,0) 
                time.sleep(10)
                count_sensor=0
                max_reading=0

                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)

                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        
                        if max_reading>194:
                            print('Fan 3 working',max_reading)
                            count_sensor=0
                            break
                        else:
                            print('Fan 3 not pulling current',max_reading)
                            fanerrors.append('Fan Three')

                            break
                f1 = GPIO.output(fan1_pos, 0)
                f2 = GPIO.output(fan2_pos, 0)
                f3 = GPIO.output(fan3_pos, 0)
                f4 =GPIO.output(fan4_pos,1)
                f5=GPIO.output(fan5_pos,0)
                f6=GPIO.output(fan6_pos,0) 
                time.sleep(10)
                count_sensor=0
                max_reading=0

                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)

                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        if max_reading>194:
                            print('Fan 4 working',max_reading)
                            count_sensor=0
                            break
                        else:
                            print('Fan 4 not pulling current',max_reading)
                            fanerrors.append('Fan Four')

                            break
                f1 = GPIO.output(fan1_pos, 0)
                f2 = GPIO.output(fan2_pos, 0)
                f3 = GPIO.output(fan3_pos, 0)
                f4 =GPIO.output(fan4_pos,0)
                f5=GPIO.output(fan5_pos,1)
                f6=GPIO.output(fan6_pos,0) 
                time.sleep(10)
                count_sensor=0
                max_reading=0

                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)

                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        if max_reading>194:
                            print('Fan 5 working',max_reading)
                            count_sensor=0
                            break
                        else:
                           print('Fan 5 not pulling current',max_reading)
                           fanerrors.append('Fan Five')

                           break
                f1 = GPIO.output(fan1_pos, 0)
                f2 = GPIO.output(fan2_pos, 0)
                f3 = GPIO.output(fan3_pos, 0)
                f4 =GPIO.output(fan4_pos,0)
                f5=GPIO.output(fan5_pos,0)
                f6=GPIO.output(fan6_pos,1) 
                time.sleep(10)
                count_sensor=0
                max_reading=0

                while True:
                    reading=bus.read_byte(0x48)
                    count_sensor+=1
                    time.sleep(.01)

                    if reading>max_reading:
                        max_reading=reading
                    if count_sensor==100:
                        if max_reading>194:
                            print('Fan 6 working',max_reading)
                            count_sensor=0
                            break
                        else:
                            print('Fan 6 not pulling current',max_reading)
                            fanerrors.append('Fan Six')
                            break
                if len(fanerrors) >0:
                    
                    root.destroy()
                    errortk=Tk()
                    errortk.geometry('700x50')
                    errortk.title('FAN ERROR')
                    GPIO.cleanup()
                    Label(errortk, text=('The Following Fan/s are not functioning: ',fanerrors)).grid(row=0,column=0)
                    errortk.mainloop()
                if len(fanerrors)==0:
                    popped=0
                    sw._running=1
                    error_reading=False
                    
                        
            
        
        if xw.tiempo<time.time():
            continue
        count_sensor+=1
                
        if reading>max_reading:
            max_reading=reading
        if count_sensor==1000:
            count_sensor=0
            print(max_reading)
            if xw.tiempo>time.time():
            
        
                
                if sw._running==0:
                    F1onimage.grid_forget()
                    F2onimage.grid_forget()
                    F3onimage.grid_forget()
                    F4onimage.grid_forget()
                    F5onimage.grid_forget()
                    F6onimage.grid_forget()
                    F1offimage.grid_forget()
                    F2offimage.grid_forget()
                    F3offimage.grid_forget()
                    F4offimage.grid_forget()
                    F5offimage.grid_forget()
                    F6offimage.grid_forget()
                        
                    F1offimage.grid(row=0,column=0)
                    F2offimage.grid(row=1,column=0)
                    F3offimage.grid(row=2,column=0)
                    F4offimage.grid(row=3,column=0)
                    F5offimage.grid(row=4,column=0)
                    F6offimage.grid(row=5,column=0)
                if sw._running== 1: 
                    if xw.state==1:
                        if max_reading>=234:
                            if popped==0:
                                F1onimage.grid_forget()
                                F2onimage.grid_forget()
                                F3onimage.grid_forget()
                                F4onimage.grid_forget()
                                F5onimage.grid_forget()
                                F6onimage.grid_forget()
                                F1offimage.grid_forget()
                                F2offimage.grid_forget()
                                F3offimage.grid_forget()
                                F4offimage.grid_forget()
                                F5offimage.grid_forget()
                                F6offimage.grid_forget()
                                
                                F1onimage.grid(row=0,column=0)
                                F2onimage.grid(row=1,column=0)
                                F3onimage.grid(row=2,column=0)
                                F4onimage.grid(row=3,column=0)
                                F5offimage.grid(row=4,column=0)
                                F6offimage.grid(row=5,column=0)
                                popped=1 
                        else:
                            F1onimage.grid_forget()
                            F2onimage.grid_forget()
                            F3onimage.grid_forget()
                            F4onimage.grid_forget()
                            F5onimage.grid_forget()
                            F6onimage.grid_forget()
                            F1offimage.grid_forget()
                            F2offimage.grid_forget()
                            F3offimage.grid_forget()
                            F4offimage.grid_forget()
                            F5offimage.grid_forget()
                            F6offimage.grid_forget()
                            error_reading=True
                            print('triggered')

                    if xw.state==2:
                        if max_reading>=234:
                            if popped==1:
                                F1onimage.grid_forget()
                                F2onimage.grid_forget()
                                F3onimage.grid_forget()
                                F4onimage.grid_forget()
                                F5onimage.grid_forget()
                                F6onimage.grid_forget()
                                F1offimage.grid_forget()
                                F2offimage.grid_forget()
                                F3offimage.grid_forget()
                                F4offimage.grid_forget()
                                F5offimage.grid_forget()
                                F6offimage.grid_forget()
                                 
                                F1onimage.grid(row=0,column=0)
                                F2onimage.grid(row=1,column=0)
                                F3onimage.grid(row=2,column=0)
                                F4onimage.grid(row=3,column=0)
                                F5offimage.grid(row=4,column=0)
                                F6offimage.grid(row=5,column=0)
                                popped=0
                        else:
                            F1onimage.grid_forget()
                            F2onimage.grid_forget()
                            F3onimage.grid_forget()
                            F4onimage.grid_forget()
                            F5onimage.grid_forget()
                            F6onimage.grid_forget()
                            F1offimage.grid_forget()
                            F2offimage.grid_forget()
                            F3offimage.grid_forget()
                            F4offimage.grid_forget()
                            F5offimage.grid_forget()
                            F6offimage.grid_forget()
                            error_reading=True
                    if xw.state==3:
                        if max_reading>=207 :
                            if popped==0:
                                F1onimage.grid_forget()
                                F2onimage.grid_forget()
                                F3onimage.grid_forget()
                                F4onimage.grid_forget()
                                F5onimage.grid_forget()
                                F6onimage.grid_forget()
                                F1offimage.grid_forget()
                                F2offimage.grid_forget()
                                F3offimage.grid_forget()
                                F4offimage.grid_forget()
                                F5offimage.grid_forget()
                                F6offimage.grid_forget()
                                
                                F1offimage.grid(row=0,column=0)
                                F2offimage.grid(row=1,column=0)
                                F3offimage.grid(row=2,column=0)
                                F4offimage.grid(row=3,column=0)
                                F5onimage.grid(row=4,column=0)
                                F6onimage.grid(row=5,column=0)
                                popped=1
                        else:
                            F1onimage.grid_forget()
                            F2onimage.grid_forget()
                            F3onimage.grid_forget()
                            F4onimage.grid_forget()
                            F5onimage.grid_forget()
                            F6onimage.grid_forget()
                            F1offimage.grid_forget()
                            F2offimage.grid_forget()
                            F3offimage.grid_forget()
                            F4offimage.grid_forget()
                            F5offimage.grid_forget()
                            F6offimage.grid_forget()
                            error_reading=True
                                
                    if xw.state==4:
                        if max_reading>=250:
                            if popped==1:
                                F1onimage.grid_forget()
                                F2onimage.grid_forget()
                                F3onimage.grid_forget()
                                F4onimage.grid_forget()
                                F5onimage.grid_forget()
                                F6onimage.grid_forget()
                                F1offimage.grid_forget()
                                F2offimage.grid_forget()
                                F3offimage.grid_forget()
                                F4offimage.grid_forget()
                                F5offimage.grid_forget()
                                F6offimage.grid_forget()
                 
                                F1onimage.grid(row=0,column=0)
                                F2onimage.grid(row=1,column=0)
                                F3onimage.grid(row=2,column=0)
                                F4onimage.grid(row=3,column=0)
                                F5onimage.grid(row=4,column=0)
                                F6onimage.grid(row=5,column=0)
                                popped=0 
                        else:
                            F1onimage.grid_forget()
                            F2onimage.grid_forget()
                            F3onimage.grid_forget()
                            F4onimage.grid_forget()
                            F5onimage.grid_forget()
                            F6onimage.grid_forget()
                            F1offimage.grid_forget()
                            F2offimage.grid_forget()
                            F3offimage.grid_forget()
                            F4offimage.grid_forget()
                            F5offimage.grid_forget()
                            F6offimage.grid_forget()
                            error_reading=True
                
            max_reading=0

                   
                
            

              
            
 
        # Totlalizer Display from the main application 

tot_vol=StringVar()
tot_val = StringVar()
def tot_displayer():

    while True:
        ser.write(b"f\r\n")
        time.sleep(.5)
        x = ser.readline()
        time.sleep(.5)
        ser.write(b"t,r\r\n")
        time.sleep(.5)
        y = ser.readline()
        x=str(x.decode('utf-8'))
        y=str(y.decode('utf-8'))
        y=y.strip()
        x=x.strip()
        time.sleep(.5)
        tot_vol.set(value=('Volume: '+y.strip('>')))#(("Volume:%s")%(y)))
        tot_val.set(value=('Flow Rate: ' +x.strip('>')))#(("Flow Rate:%s")%(x)))
       


TR.Thread(target=tot_displayer).start()


tot_val_display=Label(Frame3, textvariable=tot_val,fg='green', bg='white', width=20, height=2,borderwidth=1,relief="solid")
tot_val_display.configure(font=('Courier',12),anchor='center')

tot_vol_display=Label(Frame3, textvariable=tot_vol,fg='green', bg='white', width=20, height=2,borderwidth=1,relief="solid")
tot_vol_display.configure(font=('Courier', 12),anchor='center')

tot_vol_L=Label(Frame3, text='Volume:')
tot_vol_L.config(font=('Courier', 12))


tot_val_L=Label(Frame3, text='Flow:')
tot_val_L.config(font=('Courier', 12))













# Fan pictures
F1on=tk.PhotoImage(file="on.png")
F2on=tk.PhotoImage(file="on.png")
F3on=tk.PhotoImage(file="on.png")
F4on=tk.PhotoImage(file="on.png")
F5on=tk.PhotoImage(file="on.png")
F6on=tk.PhotoImage(file="on.png")

F1off=tk.PhotoImage(file="off.png")
F2off=tk.PhotoImage(file="off.png")
F3off=tk.PhotoImage(file="off.png")
F4off=tk.PhotoImage(file="off.png")
F5off=tk.PhotoImage(file="off.png")
F6off=tk.PhotoImage(file="off.png")

errorF1=tk.PhotoImage(file="error.png")
errorF2=tk.PhotoImage(file="error.png")
errorF3=tk.PhotoImage(file="error.png")
errorF4=tk.PhotoImage(file="error.png")
errorF5=tk.PhotoImage(file="error.png")
errorF6=tk.PhotoImage(file="error.png")


F1onimage= tk.Label(Frame6, image=F1on)
F2onimage = tk.Label(Frame6, image=F2on)
F3onimage= tk.Label(Frame6, image=F3on)
F4onimage= tk.Label(Frame6, image=F4on)
F5onimage = tk.Label(Frame6, image=F5on)
F6onimage= tk.Label(Frame6, image=F6on)

F1offimage= tk.Label(Frame6, image=F1off)
F2offimage= tk.Label(Frame6, image=F2off)
F3offimage= tk.Label(Frame6, image=F3off)
F4offimage= tk.Label(Frame6, image=F4off)
F5offimage= tk.Label(Frame6, image=F5off)
F6offimage= tk.Label(Frame6, image=F6off)

errorimage1= tk.Label(Frame6, image=errorF1)
errorimage2= tk.Label(Frame6, image=errorF2)
errorimage3= tk.Label(Frame6, image=errorF3)
errorimage4= tk.Label(Frame6, image=errorF4)
errorimage5= tk.Label(Frame6, image=errorF5)
errorimage6= tk.Label(Frame6, image=errorF6)

#temperature Class
tempC=IntVar()
hum =IntVar()
temp_Val=Label(Frame3,textvariable=tempC,fg='green', bg='white', width=20, height=2,borderwidth=1, relief="solid")
temp_Val.configure(font=('Courier', 12),anchor='center')

hum_Val=Label(Frame3, textvariable=hum,fg='green', bg='white', width=20, height=2, borderwidth=1, relief="solid")
hum_Val.configure(font=('Courier', 12),anchor='center')

class tempcontrol():
    def __init__(self, parent=None, **kw):
        self.humidity3=0
        self.Temp2=0
        self.state=False
        self.temp_set=30
        self.hum_set=55
        self.lighttoggle=0
        self.lightontime=0

    def togglelight(tog=[0]):
        tog[0] = not tog[0]
        if tog[0]:
            tempy.lighttoggle=1
            tempy.lightontime=time.time()
            light_btn.config(text='Light ON',bg='green')
            GPIO.output(light_pos, 1)
        else:
            tempy.lighttoggle=0
            light_btn.config(text='Light OFF',bg= 'red')
            GPIO.output(light_pos, 0)
    



    def heater_on_off(self):
        while True:
            
            time.sleep(1)
            self.humidity3=float(self.humidity3)
            if tempy.lighttoggle==1:
                if time.time()-self.lightontime==(5*60):
                    self.lighttoggle=1
            if self.lighttoggle==0:
                if self.humidity3>self.hum_set:
                    GPIO.output(light_pos, 1)
                if self.humidity3<=self.hum_set:
                    GPIO.output(light_pos, 0)
    def set_parameters(self):
        self.state=True
        self.temp_set=int(self.cels.get())
        self.hum_set=int(self.humspin.get())
    def display(self):
        self.tempsettings=tk.Tk()
        self.tempsettings.geometry("500x200")
        self.cels=Spinbox(self.tempsettings, from_=0, to=100,width=3, increment=1)
        self.cels.configure(font=('Courier', 8))
        self.cels.grid(row=1,column=1)
        celstempL=Label(self.tempsettings, text= 'Set Temp(c*) Parameter to:')
        celstempL.configure(font=('Courier', 8))
        celstempL.grid(row=1,column=0)
        hum_lab=Label(self.tempsettings, text='Set Humidity Parameter to:')
        hum_lab.configure(font=('Courier', 8))
        hum_lab.grid(row=2,column=0)
        self.humspin=Spinbox(self.tempsettings, from_=0, to=100,width=3, increment=1)         
        self.humspin.configure(font=('Courier', 8))
        self.humspin.grid(row=2,column=1)
        set_param=Button(self.tempsettings, text= "set parameters", command=tempy.set_parameters)
        set_param.configure(font=('Courier',8))
        set_param.grid(row=3,column=1)
                
    def Temp_Hum_Sensor(self):
        bus = smbus.SMBus(1)
        count=1
        while True:
            data3 = bus.read_i2c_block_data(0x40, 0xE1, 2)
            time.sleep (0.1)
            bus.write_byte(0x40, 0xF5)
            time.sleep(0.1)
            self.humidity3 = ((data3[0] *256 + data3[1]) * 125 / 65536.0) - 6
            data4 = bus.read_i2c_block_data(0x40, 0xE0, 2)
            time.sleep(0.1)
            bus.write_byte(0x40, 0xF3)
            time.sleep(0.1)
            data0 = bus.read_byte(0x40)
            data1 = bus.read_byte(0x40)
            cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
            fTemp = cTemp * 1.8 + 32
            self.Temp2 = ((data4[0] * 256 + data4[1]) * 175.72 / 65536.0) - 46.85
            fTemp2 = cTemp * 1.8 + 32
            count+=1
            self.humidity3=str(self.humidity3)
            self.Temp2=str(self.Temp2)
            hum.set(value=('Humidity: '+self.humidity3[0:4]+"%"))
            tempC.set(value=('Temp: '+self.Temp2[0:4]+"C"))
#iniatializing class temp
tempy=tempcontrol()
light_btn = tk.Button(Frame1, text="Light", width=5, height=2, command=tempcontrol.togglelight)
# more threading
TR.Thread(target=tempy.Temp_Hum_Sensor).start()
TR.Thread(target=tempy.heater_on_off).start()
TR.Thread(target=current_sensor).start()

#adding another menu cascade for temp control
submen.add_command(label='Temp/Humidity Options', command=tempy.display)
Frame1.grid(row=0,column=0,sticky="n")
Frame2.grid(row=0,column=1,sticky="n")
Frame3.grid(row=0,column=2,sticky="n")
Frame4.grid(row=0,column=3,sticky="n")
Frame5.grid(row=0,column=4,sticky="n")
Frame6.grid(row=0,column=5,sticky="n")

#maintkinter look, and GPIo Cleaning upon program elmination 
root.mainloop()
GPIO.cleanup()

