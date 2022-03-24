import numpy as np
from scipy.io.wavfile import write

'''
https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
Take in account that 16 bits allow representing the
range [-32768, 32767] and fit everything in [-32767,32767]
to use almost all dynamic range. 
'''
def write_wav_16_bits(file_name, sample_rate, signal):
    max_abs_value = np.max(np.abs(signal))
    signal /= max_abs_value #normalize to fit [-1,1]
    #print(max_abs_value) #answer is 1
    signal *= 2**15 - 1 #normalize to fit [-32767,32767]
    #print(np.max(np.abs(signal))) #answer is 32767
    write(file_name, sample_rate, signal.astype(np.int16))

'''
Makes sure the duration takes in account the last sample 
represents an interval of sampling_interval.
Avoid numerical errors by first generating discrete-time n
and then multiplying it by sampling_interval to obtain t in 
seconds.
'''
def generate_sin(frequency_Hz, sampling_interval, duration, initial_phase = 0):
    num_samples = round(duration/sampling_interval)
    n=np.arange(0,num_samples)
    t=n*sampling_interval
    x=np.sin(2*np.pi*frequency_Hz*t + initial_phase)
    return x

