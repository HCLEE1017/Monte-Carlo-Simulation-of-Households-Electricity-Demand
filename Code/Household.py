import TV as tv
import Kettle as kt
import Microwave as micro
import Toaster as ter
import WashingMachine as wm
import TumbleDryer as td
import Dishwasher as dw
import Fridge as fri
import Freezer as fre


class Household():

    def __init__(self):
        self.DeviceMap = {}

    def addDevice(self, deviceName, deviceObject):
        self.DeviceMap[deviceName] = deviceObject
        return self.DeviceMap

    def creatDeviceObject(self, device):
        if device == 'TV': 
            self.TV = tv.TV()
            return self.TV
        elif device == 'Kettle': 
            self.KT = kt.Kettle()
            return self.KT
        elif device == 'Microwave': 
            self.MICRO = micro.Microwave()
            return self.MICRO
        elif device == 'Toaster': 
            self.TER = ter.Toaster()
            return self.TER
        elif device == 'Washing_Machine': 
            self.WM = wm.WashingMachine()
            return self.WM
        elif device == 'Tumble_Dryer': 
            self.TD = td.TumbleDryer()
            return self.TD
        elif device == 'Dishwasher': 
            self.DW = dw.Dishwasher()
            return self.DW
        elif device == 'Fridge': 
            self.FRI = fri.Fridge()
            return self.FRI
        elif device == 'Freezer': 
            self.FRE = fre.Freezer()
            return self.FRE

    







    

