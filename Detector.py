
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
    def read(self, solution):
        pass

class PowerMeter(Detector):
    def init(self):
        self.solution = 0
        pass
    def read(self, solution):
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
        time.sleep(timeInterval)
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()
        counts=self.MyLogic.CalcCountPos(2**(channel-1))
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

    def evaluate_solution(self):
        avg_photon_count = self.getAvgPhotonCount(self.timeInterval, self.channel)
        return avg_photon_count
