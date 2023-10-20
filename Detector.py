
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
    def init(self, COM_port):
        #Parameter shoudl be connection method COM or USB

        self.solution = 0
        self.address = self.get_power_meter_adress(COM_port)
        self.pm = self.power_meter_init(780)

    def get_power_meter_address(connection_method, COM_port=None):
        """
        Takes connection_method argument ('USB' or 'COM') and optionally COM_port='COM#' if using COM
        """
        rm = visa.ResourceManager()
        pm_addr = None
        
        # Dictionary for different connection methods and their address formats
        address_formats = {
            'USB': 'USB0::0x0000::0x0000::0::INSTR',
            'COM': f'ASRL{COM_port}::INSTR'
        }
        
        # Get the corresponding address format
        address = address_formats.get(connection_method)
        
        if address is None:
            print(f"Invalid connection method: {connection_method}")
            return None
        
        if 'COM' in connection_method and COM_port is not None:
            address = address.format(COM_port=COM_port)

        try:
            inst = rm.open_resource(address)
            idn = inst.query('*IDN?').strip()
            print(f"VISA Resource: {address}, IDN: {idn}")  # Print information about detected device
            if 'PM100D' in idn:  # Replace 'PM100D' with the specific model of your power meter
                return address
        except Exception as e:
            print(f"Error querying VISA resource {address}: {e}")
            print("Power meter not found.")
            return None

    def power_meter_init(self, wv):
        """
        Function initialises power meter COMPORT and configures PM returns pm object or none if not found 
        """
        rm = visa.ResourceManager()
        if self.address != 0:
            inst = rm.open_resource(self.address)

            power_meter = ThorlabsPM100.ThorlabsPM100(inst=inst)
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
        return pMean, pStd

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
