import alsaaudio, time , audioop
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
l_d = []
data_l = []
for x in xrange(5000):
    l, data = inp.read()
    for i in np.fromstring(data, 'Int16'):
        data_l.append(i)
    #if l:
    #    l_d.append(audioop.max(data,2))

    time.sleep(.001)

t = arange(0,len(l_d), 1)

#plot(t, l_d)
#print data_l
plot(data_l)
show()
