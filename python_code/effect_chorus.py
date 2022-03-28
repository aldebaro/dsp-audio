import numpy as np

def chorus(signal,ts,rate = 5000,level = 0.5):
  """
  Function to aplly a chorus effect to a signal. this effect adds
  several delayed copies of the original signal(within the 10-25 ms range)
  using a low frequency oscilator(lfo), function takes the original signal
  and it's time period and returns the signal with chorus applied.
  """
  fs=1.0/ts # signal frequency
  lfo_rate = rate # sine frequency(Hz)
  copy_level = level # effects' amplification

  t = np.arange(0, len(signal)*ts, ts) # 

  #recomended delay is usually defined in a interval between 10 and 25 ms
  min_delay = 0.010
  max_delay = 0.025
  avg_delay = (min_delay + max_delay)/2 

  lfo = (avg_delay*np.sin(2*np.pi*t*(lfo_rate/fs)) + avg_delay)*fs #LFO

  inds = np.arange(len(signal)) #array of indices to apply the delay 
  delay = np.int64(np.ceil(inds - lfo))

  chorus = signal #deep, instead of shallow copy
  # Adding delayed copies of the signal
  for i in np.arange(0, 4*ts, 2*ts,dtype=np.int64):
      chorus += copy_level*(signal[delay - i])# sums multiple delayed copies of the original signal
  return chorus
