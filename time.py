import datetime as dt
import time as t

now=dt.datetime.now()
year='0000'
month='05'
days='00'
hrs='03'
mins='02'
sec='00'
millsec='000000'

t_time_plug=dt.timedelta(days=7)
print(t_time_plug, now)
print(now + t_time_plug)


