from audiolab import flacread
import numpy as np
from matplotlib.mlab import find

def freq_from_crossings(sig, fs):
    """Estimate frequency by counting zero crossings
    
    """
    # Find all indices right before a rising-edge zero crossing
    indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
    print indices

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    #crossings = indices

    # More accurate, using linear interpolation to find intersample 
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better. Spline, cubic, whatever

    return fs / np.mean(np.diff(crossings))

#filename = 'freqElow.flac'
filename = 'guitarE.flac'

signal, fs, enc = flacread(filename)
print fs, enc
#print fs
#print freq_from_crossings(signal, fs)
