'''
Demonstrates some audio effects.
Assume the WAV file is mono, not stereo.
'''
import numpy as np
from scipy.io import wavfile
from audio_util import write_wav_16_bits
from effect_chorus import chorus
from effect_distortion import distortion
from effect_echo import echo
from effect_flanger import flanger
from effect_overdrive import overdrive
from effect_reverb import reverb
from effect_wahwah import wahwah

# get from command line:
# 1) input file name  
# 2) output file name and
# 3) string indicating the desired audio effect
#optional for some effects such as reverb
# 4) input file name with impulse response

# assume temporary strings for testing:
input_file_name = '../test_wav_files/sample-16bits.wav'
output_file_name = 'test_effect.wav'
#chosen_effect = 'flanger'
#chosen_effect = 'echo'
#chosen_effect = 'chorus'
#chosen_effect = 'overdrive'
#chosen_effect = 'reverb'
chosen_effect = 'wahwah'
impulse_response_file_name = '../impulse_responses/kingtubby-fl2a-16bits.wav'

# open the WAV file, confirm it is mono and read the signal
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
sample_rate, original_signal = wavfile.read(input_file_name)
#signal has a shape (100,2) in case of a stereo signal with 100 samples
#or (100,) if that original_signal has a single channel (mono)
num_channels = len(original_signal.shape)
if num_channels != 1:
    raise Exception("Signal must be mono!")

#if original_signal is represented in 16 bits, convert to real numbers to facilitate manipulation
#signal = original_signal.astype(np.float) # `np.float` is a deprecated alias for the builtin `float` (). suggestion: np.float64
signal = original_signal.astype(np.float64) 
#normalize it to have amplitues in the range [-1, 1]
signal /= np.max(np.abs(signal))

# apply the chosen audio effect and generate a new signal
if chosen_effect == 'echo':
    new_signal = echo(signal, sample_rate, 0.3, gain=0.7)
elif chosen_effect == 'chorus':
    new_signal = chorus(signal, 1.0/sample_rate)
elif chosen_effect == 'overdrive':
    new_signal = overdrive(signal)
elif chosen_effect == 'reverb':
    ir_sample_rate, impulse_response = wavfile.read(impulse_response_file_name)
    assert(sample_rate == ir_sample_rate) #sample rates must be the same
    new_signal = reverb(signal, impulse_response)
elif chosen_effect == 'distortion':
    new_signal = distortion(signal)
elif chosen_effect == 'wahwah':
    new_signal = wahwah(signal, sample_rate)
else:
    raise Exception("Chosen effect is not valid!")    

# write the new signal as a 16-bits WAV file. Handle normalization properly
write_wav_16_bits(output_file_name, sample_rate, new_signal)

print('Wrote file', output_file_name, 'using effect', chosen_effect)
