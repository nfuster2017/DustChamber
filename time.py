import datetime as dt
import time as t
#gets start and end time
def test_time():
    hrs=10
    mins=10
    start_time=dt.datetime.now()
    tdelta=dt.timedelta(hours=hrs,minutes=mins)
    end_time=start_time + tdelta
    return end_time,tdelta

tdelta=dt.timedelta(hours=10,minutes=10)

test_time()
print(tdelta)









