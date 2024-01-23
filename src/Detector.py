
#OptimizationAlgorithm Libraries
from abc import ABC, abstractmethod
from collections.abc import Sequence
#Logic16 Libraries
import sys
import time
import clr

#Adding Logic16 driver to path ensure this is 64bit version and that you have selected allow permissions
sys.path.append('.')
clr.AddReference('.\\bin\\ttInterface.dll')

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

def binary_code(channel):
    """
    For use in Logic16
    """
    if isinstance(channel, Sequence):
        return sum([binary_code(k) for k in channel])
    else:
        return 2**(channel-1)

class Logic16(Detector):
    def __init__(self, logic_mode=True):
        self.MyTagger = TTInterface()
        self.MyTagger.Open()
        self._resolution = self.MyTagger.GetResolution()
        self._logic_mode = False
        if logic_mode == True:
            self._logic_mode = True
            self.MyLogic = Logic(self.MyTagger)
            self.MyLogic.SwitchLogicMode()

        self._total_channels = self.MyTagger.GetNoInputs()
        self._integration_window = 0.5 # same as self.timeInterval
        self._coincidence_window = 1e-9
        self.singles = None
        self.coincidences = None

        self.TimerCounter1 = Int32
        self.clear_buffer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.MyTagger.Close()

    def set_channels(self, singles, coincidences=None):
        assert isinstance(singles, Sequence)
        self.singles = singles
        self._bsingles = [binary_code(channel) for channel in singles]
        if coincidences is not None:
            assert isinstance(coincidences[0], Sequence)
            self.coincidences = coincidences
            self._bcoincidences = [binary_code(pair) for pair in coincidences]

    def set_delays(self, channel_delay_dict=dict(), default_delay=100):
        if hasattr(self,'delays'):
            for k,v in channel_delay_dict.items():
                assert k in range(1, self._total_channels+1)
                self.delays.update({k:v})
                self.MyTagger.SetDelay(k, (v*1e-9)/self._resolution)
        else:
            self.delays = {k:default_delay for k in range(1, self._total_channels+1)}
            self.set_delays(channel_delay_dict=channel_delay_dict)

    def set_input_threshold(self,channel_threshold_dict=None,default_threshold=0.5):
        # Configure the channel for measurement
        if channel_threshold_dict is not None:
            for k,v in channel_threshold_dict.items():
                assert k in range(1, self._total_channels+1)
                # Does the channel is the actual channel or the binary-coded channel?
                self.MyTagger.SetInputThreshold(k, v)
        else:
            for k in range(1, self._total_channels+1): # 16 channels if low-resolution
                self.MyTagger.SetInputThreshold(k, default_threshold)

    def set_coincidence_window(self, window):
        assert self._logic_mode
        self._coincidence_window = window*1e-9
        self.MyLogic.SetWindowWidth(self._coincidence_window/self._resolution)

    def get_status(self):
        msg = '>>> Logic16 counting card\n'
        msg += '> FPGA version:\t\t{}\n'.format(self.MyTagger.GetFpgaVersion())
        msg += '> Resolution:\t\t{}\n'.format(self._resolution)
        msg += '> Input channels:\t{}\n'.format(self.MyTagger.GetNoInputs())
        msg += '> Integration window:\t{} s\n'.format(self._integration_window)
        msg += '> Coincidence window:\t{} ns\n'.format(self._coincidence_window*1e9)
        # msg += '> Singles in [{}]'.format(self.singles)
        print(msg)

    def clear_buffer(self):
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()

    def read_counts(self, channel_pos, channel_neg=0, normalize=False):
        """
        Reads Counts for time interval
        """
        self.MyLogic.ReadLogic()
        TimeCounter1 = self.MyLogic.GetTimeCounter()

        def calc_single_count(pos, neg):
            return self.MyLogic.CalcCount(binary_code(pos), binary_code(neg))

        if isinstance(channel_pos[0], Sequence):
            if channel_neg == 0:
                channel_neg = [0]*len(channel_pos)
            counts = []
            for pos, neg in zip(channel_pos, channel_neg):
                iter_counts = calc_single_count(pos, neg)
                counts.append(iter_counts)
        else:
            counts = calc_single_count(channel_pos, channel_neg)
        return counts, TimeCounter1

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
