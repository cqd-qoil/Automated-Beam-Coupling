
#OptimizationAlgorithm Libraries
from abc import ABC, abstractmethod
#Logic16 Libraries
import sys
import time
import clr

#Adding Logic16 driver to path ensure this is 64bit version and that you have selected allow permissions
sys.path.append('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release')
clr.AddReference('C:\\Users\\lab\\Downloads\\CD V2.35.01\\Applications\\TimeTagExplorer\\Release_2_35_64Bit\\Release\\ttInterface.dll')

#Time Tagging Libraries
from System import Array, Byte, Int64, Int32
from TimeTag import TTInterface, Logic

class Detector:
    @abstractmethod
    def read(self):
        pass

class PowerMeter(Detector):
    def init(self, COM_port):
        self.solution = 0
        self.address = COM_port
        pass
    def read(self):
        pass

class Logic16(Detector):
    def __init__(self):
        # Initialization code, including opening the tagger
        self.MyTagger = TTInterface()
        self.MyTagger.Open
        
        # Configure the channel for measurement
        self.timeInterval = 0.5
        self.channel = 2
        self.MyTagger.SetInputThreshold(self.channel, 0.5)
        
        # Activate the Logic Mode
        self.MyLogic = Logic(self.MyTagger)
        self.MyLogic.SwitchLogicMode()
        
        self.TimerCounter1 = Int32
        self.clearBuffer()

    def clearBuffer(self):
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()

    def readCounts(self, timeInterval, channel):
        #Let Logic16 collect data for timeInterval [s]
        time.sleep(timeInterval)
        #Read count off logic
        self.MyLogic.ReadLogic()
        #Get exact time of collection
        TimeCounter1 = self.MyLogic.GetTimeCounter()
        counts=self.MyLogic.CalcCountPos(2**(channel-1))
        #Normalise counts to 1 second
        delta_t=(TimeCounter1)*5e-9
        return counts, delta_t

    def getAvgPhotonCount(self, timeInterval, channel):
        counts_list = []
        num_counts = 10
        for i in range(1, num_counts):
            self.clearBuffer()
            counts, delta_t = self.readCounts(timeInterval, channel)
            counts_list.append(counts / delta_t)
        counts_avg = sum(counts_list) / len(counts_list)
        return counts_avg, delta_t

    def read(self):
        avg_photon_count = self.getAvgPhotonCount(self.timeInterval, self.channel)
        return avg_photon_count
