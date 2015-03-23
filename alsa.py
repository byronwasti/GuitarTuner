import alsaaudio, time, audioop
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

sample_rate = 44100
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(sample_rate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(1600)

DATA = []

for x in xrange(10000):
    l, data = inp.read()
    for i in np.fromstring(data, 'Int16'):
        DATA.append(i)

    time.sleep(5.0/sample_rate)


print len(DATA)

#plot(DATA)
#show()
