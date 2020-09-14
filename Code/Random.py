import random
import datetime


def runRandomDraw (listOfResult, listOfDistribution):
    random_number = random.choices(listOfResult, listOfDistribution)
    return random_number[0]

def drawNumberOfTime(start_point, end_point):
    getNumberOfTime = random.randint(start_point, end_point)
    return getNumberOfTime

def getStartMinute(getStartTime):
    return int(getStartTime[:2])*60 + int(getStartTime[3:5])

def checkPossible(listOfActivity, getStartTime, getDuration, getPass):
    for keys, values in listOfActivity.items():
        if (getStartMinute(getStartTime) > int(keys) and getStartMinute(getStartTime) < int(keys)+int(len(values))) or (getStartMinute(getStartTime)+getDuration > int(keys) and getStartMinute(getStartTime)+getDuration < int(keys)+int(len(values))):
            return 
    getPass = True
    return getPass

def convertIntoTime (listOfActivity):
    newListOfActivity = {}
    for keys, values in listOfActivity.items():
        convertIntoTime = datetime.datetime.strptime(str(formTimeString(keys // 60) + ":" + formTimeString(keys % 60)) + ":00", "%H:%M:%S")
        newListOfActivity[str(convertIntoTime.time())] = int(listOfActivity[keys])
    return newListOfActivity

def formTimeString (time):
    if int(time) < 10: getStringTime = "0" + str(time)
    else: getStringTime = str(time)
    return getStringTime

def storeIntoList(dict, result, standbyMode, standbyWatt):
    for keys, values in dict.items():
        startLoc = keys
        for watt in list(dict[keys].values()):
            if standbyMode == True: result[startLoc].pop()
            result[startLoc].append(watt)
            startLoc += 1 
            if startLoc == 1440: break
    return result


def getRandomFixedProgram(time, deviceObject):
    k = 0
    listOfActivity = {}
    ### Generate lists of elements for number of time
    frequencyUse = preparePropData(deviceObject.numOfTime)
    getNumOfTime = runRandomDraw(frequencyUse, deviceObject.numOfTime)
    while (k < getNumOfTime):
        getPass = False
        getStartTime = runRandomDraw(time, deviceObject.start_time)
        numOfProgram = drawNumberOfTime(1, len(deviceObject.washingProgram))
        if not bool(listOfActivity) == False: 
            getPass = checkPossible(listOfActivity, getStartTime,len(deviceObject.washingProgram[numOfProgram]), getPass)
        if (not bool(listOfActivity)== True or getPass == True):
            listOfActivity[getStartMinute(getStartTime)] = deviceObject.washingProgram[numOfProgram]
        k += 1
    deviceObject.total_consumption = storeIntoList(listOfActivity, deviceObject.total_consumption, False, 0)


def drawWatt(device, getDuration, WattList, wattDis):
    DurationDict = {}
    for i in range(int(getDuration)):
        DurationDict[i] = int(runRandomDraw(wattDis, WattList))
    return DurationDict

def storeStandbyMode(standbyWatt, totalconsume, standbyMode):
    if standbyWatt == int(0): return totalconsume, standbyMode
    else: 
        standbyMode = True
        for time, watt in totalconsume.items():
            totalconsume[time].append(int(standbyWatt))
    return totalconsume, standbyMode

### Function used toproduce the element list for random sampling
def preparePropData(smoothList):
    probDis = []
    for i in range(len(smoothList)):
        probDis.append(int(i))
    return probDis


def getRanDirUseDevice(time, minute, deviceObject, deviceName):
    k = 0
    haveStandByMode = False
    listOfActivity = {}
    ### Generate lists of elements for number of time and watt
    frequencyUse = preparePropData(deviceObject.numOfTime)
    wattDis = preparePropData(deviceObject.Watt)
    getNumOfTime = runRandomDraw(frequencyUse, deviceObject.numOfTime)
    deviceObject.total_consumption, haveStandByMode = storeStandbyMode(deviceObject.standbyMode, deviceObject.total_consumption, haveStandByMode)
    while (k < getNumOfTime):
        getPass = False
        getStartTime = runRandomDraw(time, deviceObject.start_time)
        if deviceName == "TV" or deviceName == "Microwave": 
            if deviceObject.DurationMap[getStartMinute(getStartTime)].count(0) == 600: continue
            getDuration = runRandomDraw(minute, deviceObject.DurationMap[getStartMinute(getStartTime)])
        else: 
            durationDis = preparePropData(deviceObject.duration)
            getDuration = runRandomDraw(durationDis, deviceObject.duration)
        if not bool(listOfActivity) == False: 
            getPass = checkPossible(listOfActivity, getStartTime, getDuration, getPass)
        if (not bool(listOfActivity)== True or getPass == True):
            DurationDict = drawWatt(deviceObject, getDuration, deviceObject.Watt, wattDis)
            listOfActivity[getStartMinute(getStartTime)] = DurationDict
        k += 1
    deviceObject.total_consumption = storeIntoList(listOfActivity, deviceObject.total_consumption, haveStandByMode, deviceObject.standbyMode)


def getOnOffDuration (time, deviceObject, durationDis, durationList, wattDis, wattList, listOfActivity):
    originalTime = time
    getDur = runRandomDraw(durationDis, durationList)
    time += getDur
    if (time > 1439): 
        getDur = getDur - (time - 1439)
        time = 1439
    DurationDict = drawWatt(deviceObject, getDur, wattList, wattDis)
    listOfActivity[originalTime] = DurationDict
    return listOfActivity, time

def getRanContinDevice(deviceObject):
    listOfActivity = {}
    time = 0
    ### Generate four lists of elements for random sampling
    onDurationDis = preparePropData(deviceObject.onDuration)
    offDurationDis = preparePropData(deviceObject.offDuration)
    onWattDis = preparePropData(deviceObject.onWatt)
    offWattDis = preparePropData(deviceObject.offWatt)
    while(time < 1440):
        listOfActivity, time = getOnOffDuration (time, deviceObject, offDurationDis, deviceObject.offDuration, offWattDis, deviceObject.offWatt, listOfActivity)
        if int(time) >= int(1439): break
        listOfActivity, time = getOnOffDuration (time, deviceObject, onDurationDis, deviceObject.onDuration, onWattDis, deviceObject.onWatt, listOfActivity)
    deviceObject.total_consumption = storeIntoList(listOfActivity, deviceObject.total_consumption, False, 0)


