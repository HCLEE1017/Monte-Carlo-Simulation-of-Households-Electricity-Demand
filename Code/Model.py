from getData import getData
from setup import * 
import Random as rd
import copy
from operator import add

class Model():

    def __init__(self):
        initDurationMinute()
        initTargetTime()
        initResultDict()


    def coordinateData(self, deviceList, days):
        self.DayDict = getData(deviceList, days).DayDict
        for day, household_name in self.DayDict.items():
            for name, device_object in self.DayDict[day].items():
                for deviceName, deviceObject in self.DayDict[day][name].items():
                    deviceObject.smoothData()
        
    

    def runModel(self, deviceList, days, numSim):
        def drawDeviceConsumption(deviceList, day, simulation, decidedIteration):
            counter = 0
            for deviceName in deviceList:
                getObjectList = lookupDevice(deviceName, day, simulation, decidedIteration)
                if len(getObjectList) == int(0): 
                    counter += 1
                    continue
                varname = str(deviceName) + '_Consumption'
                if deviceName == 'TV' or deviceName == 'Kettle' or deviceName == 'Microwave' or deviceName == 'Toaster': getDirUseRand(varname, getObjectList, deviceName)
                if deviceName == 'Washing_Machine' or deviceName == 'Tumble_Dryer' or deviceName == 'Dishwasher': getFixUseRand(varname, getObjectList)
                if deviceName == 'Fridge' or deviceName == 'Freezer': getContinUseRand(varname, getObjectList)
            if counter == len(deviceList): return True
            else: return False


        def lookupDevice(device, day, simulation, decidedIteration):
            objectList = []
            for name, device_object in self.DayDict[day].items():
                for deviceName, deviceObject in self.DayDict[day][name].items():
                    if deviceName == device and deviceObject.checkEmpty() == False and decidedIteration == True: 
                        objectList.append(deviceObject)
                    elif deviceName == device and deviceObject.checkEmpty() == False and int(simulation) < int(deviceObject.getSimulation()) : 
                        objectList.append(deviceObject)
                    else: continue
            return objectList

        def getDirUseRand(varname, objectList, deviceName):
            for Object in objectList:
                rd.getRanDirUseDevice(time, minute, Object, deviceName)
            
            
        def getFixUseRand(varname, objectList):
            for Object in objectList: 
                rd.getRandomFixedProgram(time, Object)
                
        
        def getContinUseRand(varname, objectList):
            for Object in objectList: 
                rd.getRanContinDevice(Object)


        totalConsume = [0]*1440
        deviceConsume = [0]*1440
        deviceOn = []
        totalOn = []

        for day in days:
            ### Perform Monte Carlo Simulation
            simulation = 0
            if numSim == '':
                var = 1
                while var == 1:
                    if drawDeviceConsumption(deviceList, day, simulation, False) == False: 
                        simulation += 1  
                        continue
                    else: break
                        
            else: 
                while simulation < int(numSim):
                    drawDeviceConsumption(deviceList, day, simulation, True)
                    simulation += 1 

            ### Obtain the Aggregate result for each device
            for i in range(len(list(deviceList))):
                for name, device_object in self.DayDict[day].items():
                    if str(list(deviceList)[i]) not in self.DayDict[day][name].keys(): 
                        continue
                    deviceCon = self.DayDict[day][name][str(list(deviceList)[i])].total_consumption
                    for keys, values in deviceCon.items():
                        totalOn +=  list(map(int, deviceCon[keys]))
                        if numSim == '': totalSim = self.DayDict[day][name][str(list(deviceList)[i])].numSimultaion
                        else: totalSim = int(numSim)
                        if len(list(map(int, deviceCon[keys]))) != int(0): deviceConsume[keys] = sum(list(map(int, deviceCon[keys])))/totalSim
                        else: deviceConsume[keys] = 0
                    totalConsume = list(map(add, totalConsume, deviceConsume))
                    deviceConsume = [0]*1440
                result[str(list(deviceList)[i]) + '_consumption_' + str(day)] = copy.deepcopy(totalConsume)
                result[str(list(deviceList)[i]) + '_probdensity_' + str(day)] = copy.deepcopy(totalOn)
                totalConsume = [0]*1440
                totalOn.clear()

    def getTargetTime(self):
        return targetTime

    def getResult(self):
        return result

