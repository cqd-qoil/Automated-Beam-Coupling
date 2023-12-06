
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

#PM Library
import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100
import numpy as np

class Detector:
    @abstractmethod
    def read(self):
        pass

class PowerMeter(Detector):
    def __init__(self, device_name):
        self.address = self.get_power_meter_address(device_name)
        self.pm = self.power_meter_init(780)

    def get_power_meter_address(self, device_name):
        """
        Takes device name argument and returns address if it exists

        Sometimes the registered name may vary from the actual name to list all connected device names run list_all_addresses()
        """
        rm = visa.ResourceManager()
        pm_addr = None

        for item in rm.list_resources():
            try:
                inst = rm.open_resource(item)
                idn = inst.query('*IDN?').strip()
                print("\nVISA Resource: ",item, ", IDN: ",idn)  # Print information about detected devices
                if device_name in idn:  # Search for device model
                    pm_addr = item
                    break
            except Exception as e:
                print(f"Error querying VISA resource {item}: {e}")

        if pm_addr:
            print("Power meter VISA address: ", pm_addr)
            return pm_addr
        else:
            print("Power meter not found.")
            return 0

    def list_all_addresses(device_name):
        """
        Takes device name argument and searches through resources for it
        Sometimes the registered name may vary from the actual name to list all connected device names run XXXX
        """
        rm = visa.ResourceManager()
        pm_addr = None

        for item in rm.list_resources():
            try:
                inst = rm.open_resource(item)
                idn = inst.query('*IDN?').strip()
                print("\nVISA Resource: ",item, ", IDN: ",idn)  # Print information about detected devices
            except Exception as e:
                print(f"Error querying VISA resource {item}: {e}")

    def power_meter_init(self, wv):
        """
        Function initialises power meter COMPORT and configures PM returns pm object or none if not found
        """
        rm = visa.ResourceManager()
        if self.address != 0:
            inst = rm.open_resource(self.address)

            power_meter = ThorlabsPM100(inst=inst)
            power_meter.configure.scalar.power()

            #Configure device wavelength param wavelength otherwise default to 780
            power_meter.sense.correction.wavelength = 780

            return power_meter
        else:
            print("power meter address not found")
            return None

    def read(self):
        """
        Function to sample power reading off power meter. Samples n measurements
        then returns avg power and standard deviation in power

        Input:
        Output: pMean: Avg power over n interval, pStd: Standard deviation in measurement
        """
        power_samples = 30
        power = np.array([self.pm.read for i in range(power_samples)])
        pMean = power.mean()
        pStd = power.std()
        return pMean

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
        """
        Reads Counts for time interval
        """
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
        """
        Performs 10 counts over timeInterval then returns avg result
        """
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
