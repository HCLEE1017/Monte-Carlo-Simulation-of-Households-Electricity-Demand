import sqlite3
import collections
import Household as household
import datetime 
import calendar 
import copy


class getData(object):

    def __init__(self, device, Days):

        def dict_factory(cursor, row):
            d = {}
            for index, col in enumerate(cursor.description):
                d[col[0]] = row[index]
            return d

        ### get number of household
        def getNumOfHousehold(table, numOfHousehold, device):
            for row in table:
                if list(row.values())[0] not in self.Community.keys(): 
                    deviceObject = household.Household().creatDeviceObject(device)
                    self.Community[list(row.values())[0]] = copy.deepcopy(household.Household().addDevice(device, deviceObject))
                elif device not in self.Community[list(row.values())[0]].keys():
                    deviceObject = household.Household().creatDeviceObject(device)
                    self.Community[list(row.values())[0]][device] = copy.deepcopy(deviceObject)
                numOfHousehold = numOfHousehold + list(row.values())
            return numOfHousehold


        def decideDay(date): 
            born = datetime.datetime.strptime(date, '%Y/%m/%d').weekday() 
            return (calendar.day_name[born]) 

        
        def getDeviceData(table, time, Watt, device, deviceObject):
            for row in table:
                time.append(row['Time'].strip())
                Watt.append(row['Watt'].strip())
            
            if device == 'TV': storeDirectUseDevice(time, Watt, deviceObject)
            elif device == 'Kettle': storeDirectUseDevice(time, Watt, deviceObject)
            elif device == 'Microwave': storeDirectUseDevice(time, Watt, deviceObject)
            elif device == 'Toaster': storeDirectUseDevice(time, Watt, deviceObject)
            elif device == 'Washing_Machine': storeProgramCycleData(time, Watt, deviceObject)
            elif device == 'Tumble_Dryer': storeProgramCycleData(time, Watt, deviceObject)
            elif device == 'Dishwasher': storeProgramCycleData(time, Watt, deviceObject)
            elif device == 'Fridge':
                deviceObject.numSimultaion += 1
                storeContinuousDevice(Watt, deviceObject)
            elif device == 'Freezer': 
                deviceObject.numSimultaion += 1
                storeContinuousDevice(Watt, deviceObject)


        def storeInforIntoClass(setDay, numOfHousehold, device):
            for i in range(0, len(numOfHousehold), 2):
                today = str(decideDay(numOfHousehold[i+1]))
                if today == 'Monday' or today == 'Tuesday' or today == 'Wednesday' or today == 'Thursday' or today == 'Friday': day = 'WorkingDay'
                else: day = "WeekEnd"
                if str(day) != str(setDay): continue
                else:
                    deviceObject = self.Community[numOfHousehold[i]][device]
                    time, Watt = ([] for i in range(2)) 
                    cur.execute("select Time,Watt from '%s' where Household_Id = '%s' AND Date = '%s'" % (device , numOfHousehold[i], numOfHousehold[i+1]))
                    table = cur.fetchall()
                    getDeviceData(table, time, Watt, device, deviceObject)


        ### Store washing program into the class of fixed program devices
        def storeProgramCycle(device, listOfWatt):
            getPass = False
            for keys, values in device.washingProgram.items():
                ### check whether this fixed program has been already stored
                if collections.Counter(listOfWatt) == collections.Counter(list(device.washingProgram[keys].values())): 
                    getPass = True
                    break
                else: continue
            if getPass == False:
                programDuration = {}
                for j in range(len(listOfWatt)):
                    programDuration[str(j+1)] = listOfWatt[j]
                device.washingProgram[len(device.washingProgram)+1] = programDuration

        ### Store start time into the class of fixed program devices
        def storeObject(deviceObject, start_time, listOfWatt, curLoc):
            deviceObject.start_time.append(start_time)
            if curLoc != 1439: storeProgramCycle(deviceObject, listOfWatt)

        ### Check whether the washing program is last more than 15 mins and has more than 1kW
        def checkOperatingProgram(j, counter, time, Watt, deviceObject):
            start = j
            while (int(Watt[start]) != int(0)): 
                counter += 1
                start += 1
                if start == 1439: break
                
            if counter < 15 or sum(list(Watt[j:start])) < int(1000): 
                j = start
                return j
            storeObject(deviceObject, int(time[j][:2])*60+int(time[j][3:]), list(Watt[j:start]), start)
            j = start
            return j

        ### Check the change of watt for fixed use device and store number of time into the class of fixed program devices
        def storeProgramCycleData(time, Watt, deviceObject):
            j = numOfUse = 0
            Watt = list(map(int, Watt)) 
            ### remove overnight electricity use
            for watt in Watt: 
                if int(watt) != int(0): j += 1
                else: break
            while (j < len(time)-1):
                counter = 0
                if int(Watt[j]) == int(0): j += 1
                else: j = checkOperatingProgram(j, counter, time, Watt, deviceObject)
            if len(deviceObject.start_time) != int(0):
                if len(deviceObject.numOfTime) == 0: numOfUse += len(deviceObject.start_time)
                else: numOfUse += len(deviceObject.start_time) - sum(deviceObject.numOfTime)
            deviceObject.numOfTime.append(numOfUse)


        ### Used to decide the standby mode of the device
        def getStandByMode(deviceObject, Watt):
            mostWatt = [i[0] for i in collections.Counter(Watt).most_common(2)]
            if int(0) in set(mostWatt) and int(1) in set(mostWatt):
                firstSBWatt = int(0)
                secondSBWatt = int(1)
            elif Watt.count(int(0)) > 5: firstSBWatt = secondSBWatt = int(0)
            else: 
                firstSBWatt = int(mostWatt[0])
                secondSBWatt = int(mostWatt[1])
                if (secondSBWatt > firstSBWatt and secondSBWatt - firstSBWatt != 1) or (firstSBWatt > secondSBWatt and firstSBWatt - secondSBWatt != 1):
                    secondSBWatt = firstSBWatt + 1
            return firstSBWatt, secondSBWatt

        ### Check the change of watt for direct use device
        def storeDirectUseDevice(time, Watt, deviceObject):
            Watt = list(map(int, Watt)) 
            firstSBWatt, secondSBWatt = getStandByMode(deviceObject, Watt)
            deviceObject.standbyMode = firstSBWatt
            startLoc = numOfTime = counter = 0
            for watt in Watt: 
                if int(watt) != int(firstSBWatt) and int(watt) != int(secondSBWatt): startLoc += 1
                else: break
            getTime, getWatt = ([] for i in range(2)) 
            for i in range(startLoc, len(time)-1):
                if (int(Watt[i]) == firstSBWatt or int(Watt[i]) == secondSBWatt) and (int(Watt[i+1]) != firstSBWatt and int(Watt[i+1]) != secondSBWatt):
                    getTime.append(int(time[i+1][:2])*60+int(time[i+1][3:]))
                if (int(Watt[i]) != firstSBWatt and int(Watt[i]) != secondSBWatt) and ((int(Watt[i+1]) != firstSBWatt and int(Watt[i+1]) != secondSBWatt) or (int(Watt[i-1]) != firstSBWatt and int(Watt[i-1]) != secondSBWatt)):
                    counter += 1
                    getWatt.append(int(Watt[i]))
                if (int(Watt[i]) != firstSBWatt and int(Watt[i]) != secondSBWatt) and (int(Watt[i+1]) == firstSBWatt or int(Watt[i+1]) == secondSBWatt):
                    if counter >= 2: 
                        getTime.append(int(time[i][:2])*60+int(time[i][3:]))
                        numOfTime += 1
                        counter = 0
                    else: getTime.pop()
            storeInDirUseClass(deviceObject, getTime, numOfTime, getWatt)
                
            
        ### Store data into the class of direct use device
        def storeInDirUseClass(deviceObject, getTime, numOfTime, getWatt):
            if len(getTime)%2 != 0: 
                getTime.append(1439)
                numOfTime += 1
            for j in range(0, len(getTime)-1, 2):
                if j == 0 or j%2 == 0: 
                    deviceObject.start_time.append(getTime[j])
                deviceObject.duration.append(getTime[j+1]-getTime[j]+1)
            deviceObject.Watt += getWatt
            deviceObject.numOfTime.append(numOfTime)

        ### Function used to check the change of watt for continue use devices
        def storeContinuousDevice (Watt, deviceObject):
            Watt = list(map(int, Watt)) 
            firstSBWatt, secondSBWatt = getStandByMode(deviceObject, Watt)
            getFirstDuration = False
            start = count = 0
            getList, spareList, storeList = ([] for i in range(3)) 
            for i in range(len(Watt)-1):
                if (int(Watt[i]) == firstSBWatt or int(Watt[i]) == secondSBWatt) and (int(Watt[i+1]) != firstSBWatt and int(Watt[i+1]) != secondSBWatt):
                    getList = Watt[start:i+1]
                    start = i+1
                    storeList = storeCompressorDur(getList, Watt, i, storeList, deviceObject.onDuration, deviceObject.onWatt)
                    
                elif (int(Watt[i]) != firstSBWatt and int(Watt[i]) != secondSBWatt) and (int(Watt[i+1]) == firstSBWatt or int(Watt[i+1]) == secondSBWatt):
                    getList =  Watt[start:i+1]
                    start = i+1
                    storeList = storeCompressorDur(getList, Watt, i, storeList, deviceObject.offDuration, deviceObject.offWatt)
                
                if len(deviceObject.onDuration) == 1 and len(deviceObject.offDuration) == 0 and getFirstDuration == False:
                    deviceObject.onDuration.pop()
                    getFirstDuration = True

                elif len(deviceObject.offDuration) == 1 and len(deviceObject.onDuration) == 0 and getFirstDuration == False:
                    deviceObject.offDuration.pop()
                    getFirstDuration = True

                spareList = Watt[start:i+1]
            if len(spareList) != int(0): storeEndingList(deviceObject, spareList, firstSBWatt, secondSBWatt)
            if len(storeList) != int(0): storeEndingList(deviceObject, storeList, firstSBWatt, secondSBWatt)
            

        ### Storing the rest of data into the class of continuous use device 
        def storeEndingList(deviceObject, endingList, firstSBWatt, secondSBWatt):
            addIntoList = "on"
            getMaxSecList = most_frequent(endingList)
            if int(getMaxSecList) == int(firstSBWatt) or int(getMaxSecList) == int(secondSBWatt):
                averOfList = float(sum(deviceObject.offDuration)/len(deviceObject.offDuration))
                addIntoList = "off"
            else: averOfList = float(sum(deviceObject.onDuration)/len(deviceObject.onDuration))
            if len(endingList) >= int(averOfList):
                if addIntoList == "off":
                    deviceObject.offDuration.append(len(endingList))
                    deviceObject.offWatt += endingList
                else: 
                    deviceObject.onDuration.append(len(endingList))
                    deviceObject.onWatt += endingList

 
        ### Store the duration and watt into the class of continuous use device
        def storeCompressorDur(getList, Watt, i, storeList, durationList, wattList):
            if len(storeList) == 0: storeList = copy.deepcopy(getList)
            elif (len(getList) < 5 and len(storeList) != 0): storeList += getList
            elif (len(getList) > 4 and len(storeList) != 0): 
                getMaxList = most_frequent(storeList)
                getMaxSecList = most_frequent(getList)
                if (int(getMaxList) == int(0) and int(getMaxSecList) == int(0)): storeList += getList
                else:
                    durationList.append(len(storeList))
                    wattList += storeList
                    storeList = copy.deepcopy(getList)
            return storeList
                        

        ### Function used to check which element has the most occurence inside the list
        def most_frequent(List): 
            return max(set(List), key = List.count) 

                    
    
        ### Whole process of constructing the data structure
        self.DayDict = {}

        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        print("cur is ", cur)

        for day in Days:
            self.Community = {}
            for i in range(len(device)):
                numOfHousehold = []
                cur.execute("select Distinct Household_Id, Date from '%s'" % (device[i]))
                table = cur.fetchall()
                numOfHousehold = getNumOfHousehold(table, numOfHousehold, device[i])
                storeInforIntoClass(day, numOfHousehold, device[i])
            self.DayDict[day] = copy.deepcopy(self.Community)
        
        con.commit()
        con.close()

        
        