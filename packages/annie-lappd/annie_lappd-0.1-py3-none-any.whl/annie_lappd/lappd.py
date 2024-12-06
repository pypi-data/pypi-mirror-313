import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tqdm import tqdm
import time, sys

# Define the sequence of numbers (mapping ACDC to strip)
ACDC_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]
STRIP_INDEX = [0, 5, 4, 3, 2, 1, 12, 11, 10, 9, 8, 7, 18, 17, 16, 15, 45, 44, 55, 54, 53, 52, 51, 50, 61, 60, 59, 58, 57, 56, 36, 31, 6, 25, 26, 27, 28, 29, 30, 19, 20, 21, 22, 23, 24, 13, 14, 46, 47, 48, 49, 38, 39, 40, 41, 42, 43, 32, 33, 34, 35, 37, 62, 63]

INDEX_ACDC = np.array(ACDC_INDEX)
INDEX_STRIP = np.array(STRIP_INDEX)

class LAPPD:
    def __init__(self, data, pedestals) -> None:
        self.data = data
        self.pedestals = pedestals
        self.event_data = self.loadData()

    def loadFile(self, file_input):
        return pd.read_csv(file_input, sep=' ', header=None)
    
    def loadData(self):
        data = self.loadFile(self.data)
        lines_per_event = 256
        num_events = len(data) // lines_per_event
        return data.values.reshape((num_events, lines_per_event, -1))
    
    def getEvents(self):
        return self.event_data

    @property
    def pedestalSubtraction(self):
        pedestal1 = self.loadFile(self.pedestals[0]) 
        pedestal2 = self.loadFile(self.pedestals[1]) 
       
        # reshape the pedestal data to match the shape of the event data
        pedestal1_values = pedestal1.values.reshape(1, -1, 30).astype(float)
        pedestal2_values = pedestal2.values.reshape(1, -1, 30).astype(float)

        self.event_data[:, :, 1:31] -= pedestal1_values
        self.event_data[:, :, 32:62] -= pedestal2_values
        print(f"[+] Done Pedestal Substraction.... \n")

    @property
    def convertADCtoVoltage(self):
        # Multiply by 0.3 to convert ADC to Voltage
        # -1 to 0.3 is to invert the waveforms
        self.event_data[:, :, 1:31]  = np.multiply(self.event_data[:, :, 1:31],-0.3) 
        self.event_data[:, :, 32:62] = np.multiply(self.event_data[:, :, 32:62],-0.3)
        #return self.event_data
        print("[+] Done Converting to Voltage.... \n")

    @property
    def correctingACDCmetadata(self):
        # Reorder ACDC meta 
        num_events = self.event_data.shape[0]

        bs1 = int("0000000000000111", 2)
        shift_values = np.array([bs1 & int(x, 16) for x in self.event_data[:,10,31]])
        shift_values = np.multiply(shift_values, 32)

        shift_global = np.full(num_events, 80)

        # Create a range of indices along the rows axis
        row_indices = np.arange(self.event_data.shape[1])
        # Expand the meta array to match the shape of event_data along the rows axis
        expanded_meta = np.expand_dims(-shift_values, axis=1)
        # Calculate the rolled indices using broadcasting
        rolled_indices = (row_indices - expanded_meta) % self.event_data.shape[1]
        # Use advanced indexing to roll the event_data array
        self.event_data = self.event_data[np.arange(len(-shift_values))[:, None], rolled_indices]

        # Shift 80 time units (Matt?)
        # Expand the meta array to match the shape of event_data along the rows axis
        expanded_meta = np.expand_dims(-shift_global, axis=1)
        # Calculate the rolled indices using broadcasting
        rolled_indices = (row_indices - expanded_meta) % self.event_data.shape[1]
        # Use advanced indexing to roll the event_data array
        self.event_data = self.event_data[np.arange(len(-shift_global))[:, None], rolled_indices]
        #return self.event_data
        print("[+] Done Metadata correction....\n")
    
    @property
    def convertACDCtoStripIndex(self):
        # ACDC channels index to Strip index
        self.event_data = self.event_data[:, :, STRIP_INDEX]
        print("[+] Done mapping ACDC to Strip....\n") 

    def baselineCorrection(self, arbitrary_value=200):
        # Baseline correction
        # ToDo: Arbitrary it is set the mean from 200ns to 220ns
        # Calculate the baseline for each row
        #baseline1 = np.mean(event_data[:,0:255,1:31], axis=1, keepdims=True)
        #baseline1 = np.mean(self.event_data[:,100:120,1:31], axis=1, keepdims=True)
        baseline1 = np.mean(self.event_data[:,arbitrary_value:arbitrary_value+20,1:31], axis=1, keepdims=True)
        self.event_data[:, :, 1:31] -= baseline1 

        #baseline2 = np.mean(event_data[:,0:255,32:62], axis=1, keepdims=True)
        #baseline2 = np.mean(self.event_data[:,100:120,32:62], axis=1, keepdims=True)
        baseline2 = np.mean(self.event_data[:,arbitrary_value:arbitrary_value+20,32:62], axis=1, keepdims=True)
        self.event_data[:, :, 32:62] -= baseline2
        print(f"[!] WARNING Baseline Substraction with arbitrary value picked from {arbitrary_value} to {arbitrary_value + 20}ns.....\n")

    @property
    def filterFFT(self, cutoff_frequency=50):
        sampling_rate = 256  # Adjust according to your actual sampling rate
        #cutoff_frequency = 50  # Cutoff frequency in Hz
        filtered_waveforms1 = np.zeros_like(self.event_data[:, :, 1:31])
        filtered_waveforms2 = np.zeros_like(self.event_data[:, :, 32:62])

        for i in range(self.event_data[:, :, 1:31].shape[0] - 2):
            for j in range(self.event_data[:, :, 1:31].shape[2]):
                ct = i + 1
                cj = j + 1

                waveform = np.array(self.event_data[ct:ct+1, :, cj:cj+1],dtype=float).flatten()

                if len(waveform) == 0:
                    print(ct,":",ct+1," waveform is empty. Cannot perform FFT.", cj,":",cj+1)
                else:
                    fft_result = np.fft.fft(waveform)

                # Create the filter
                freqs = np.fft.fftfreq(len(waveform), d=1/sampling_rate)
                filter_mask = np.abs(freqs) < cutoff_frequency

                # Apply the filter
                filtered_fft_result = fft_result * filter_mask

                # Inverse FFT to get back to time domain
                filtered_waveform = np.fft.ifft(filtered_fft_result)

                # Store the filtered waveform
                filtered_waveforms1[i, :, j] = filtered_waveform.real

        
        for i in range(self.event_data[:, :, 32:62].shape[0] - 2):
            for j in range(self.event_data[:, :, 32:62].shape[2]):
                ct = i + 1
                cj = 31 + j + 1

                waveform = np.array(self.event_data[ct:ct+1, :, cj:cj+1],dtype=float).flatten()

                if len(waveform) == 0:
                    print(ct,":",ct+1," waveform is empty. Cannot perform FFT.", cj,":",cj+1)
                else:
                    fft_result = np.fft.fft(waveform)

                # Create the filter
                freqs = np.fft.fftfreq(len(waveform), d=1/sampling_rate)
                filter_mask = np.abs(freqs) < cutoff_frequency

                # Apply the filter
                filtered_fft_result = fft_result * filter_mask

                # Inverse FFT to get back to time domain
                filtered_waveform = np.fft.ifft(filtered_fft_result)

                # Store the filtered waveform
                filtered_waveforms2[i, :, j] = filtered_waveform.real
        
        self.event_data[:, :, 1:31] = filtered_waveforms1
        self.event_data[:, :, 32:62] = filtered_waveforms2
        print(f"[+] Done FFT with cutoff_frequency of {cutoff_frequency}....")

   
    def getEvent(self, event_id, side, spare_channels):
        if side == 0:
            if spare_channels == 0:
                return self.event_data[event_id,:,2:30]
            else:
                return self.event_data[event_id,:,1:31]
        else:
            if spare_channels == 0:
                return self.event_data[event_id,:,33:61] 
            else:
                return self.event_data[event_id,:,32:62]

