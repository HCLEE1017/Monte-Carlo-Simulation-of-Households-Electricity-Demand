import Modify as KDE
import copy

class Dishwasher(object):
    def __init__(self):
        self.start_time = []
        self.numOfTime = []
        self.standbyMode = []
        self.numSimultaion = 0
        self.washingProgram = {}
        self.total_consumption = {}
        for i in range(1440):
            self.total_consumption[i] = []

    def checkEmpty(self):
        if len(self.start_time) == 0 or len(self.numOfTime) == 0: return True
        else: return False

    def getSimulation(self):
        return self.numSimultaion
        
    def smoothData(self):
        if len(self.start_time) == 0 or len(self.numOfTime) == 0: return

        self.start_time = KDE.applyKDE(0, 1440, 1440, self.start_time)
        
        self.numSimultaion = copy.deepcopy(len(self.numOfTime)-1)
        
        self.numOfTime = KDE.applyKDE(0, max(self.numOfTime)+1, max(self.numOfTime)+1, self.numOfTime)
 


