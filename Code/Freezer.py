import Modify as KDE

class Freezer():

    def __init__(self):
        self.onDuration = []
        self.offDuration = []
        self.onWatt = []
        self.offWatt = []
        self.numSimultaion = 0
        self.total_consumption = {}
        for i in range(1440):
            self.total_consumption[i] = []

    def checkEmpty(self):
        if len(self.onDuration) == 0 or len(self.offDuration) == 0: return True
        else: return False

    def getSimulation(self):
        return self.numSimultaion

    def smoothData(self):

        if len(self.onDuration) == 0 or len(self.offDuration) == 0: return

        self.onDuration = KDE.applyKDE(0, max(self.onDuration)+1, max(self.onDuration)+1, self.onDuration)

        self.offDuration = KDE.applyKDE(0, max(self.offDuration)+1, max(self.offDuration)+1, self.offDuration)

        self.onWatt = KDE.applyKDE(0, max(self.onWatt)+1, max(self.onWatt)+1, self.onWatt)

        self.offWatt = KDE.applyKDE(0, max(self.offWatt)+1, max(self.offWatt)+1, self.offWatt)