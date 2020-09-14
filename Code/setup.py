import datetime

minute = [0]*600
targetTime = [0]*1440
time = [0]*1440
result = {}

### build the lists of time and targetTime before Monte Carlo Simulation
def initTargetTime():
    start_time = datetime.datetime(100,1,1,00,00)
    for i in range(1440):
        targetTime[i] = datetime.datetime.strptime(str(start_time.time()), "%H:%M:%S")
        time[i] = str(start_time.time())
        start_time += datetime.timedelta(0,60)

def initResultDict():
    result = {}

### initialise list of minute
def initDurationMinute():
    ### define start time and end time
    start_time = datetime.datetime(100,1,1,00,00)
    endOfDay = datetime.datetime(100,1,2,00,00)
    for j in range(1, 600):
        minute[j] = j