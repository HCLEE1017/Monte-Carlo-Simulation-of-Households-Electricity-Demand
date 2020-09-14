import Modify as KDE
import copy



class Kettle():

    def __init__(self):
        self.numOfTime = []
        self.start_time = []
        self.duration = []
        self.Watt = []
        self.numSimultaion = 0
        self.standbyMode = 0
        self.total_consumption = {}
        for i in range(1440):
            self.total_consumption[i] = []

    def checkEmpty(self):
        if len(self.start_time) == 0 or len(self.numOfTime) == 0: return True
        else: return False

    def getStart_Time(self): 
        return self.start_time

    def insertList(self, num):
        self.start_time.append(num)

    def getSimulation(self):
        return self.numSimultaion


    def smoothData(self):
        if len(self.start_time) == 0 or len(self.numOfTime) == 0: return 
        
        self.start_time = KDE.applyKDE(0, 1440, 1440, self.start_time)

        self.duration = KDE.applyKDE(0, max(self.duration)+1, max(self.duration)+1, self.duration)

        self.numSimultaion = copy.deepcopy(len(self.numOfTime)-1)

        self.numOfTime = KDE.applyKDE(0, max(self.numOfTime)+1, max(self.numOfTime)+1, self.numOfTime)

        self.Watt = KDE.applyKDE(0, max(self.Watt)+1, max(self.Watt)+1, self.Watt)


