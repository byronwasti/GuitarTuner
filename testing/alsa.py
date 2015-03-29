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
    DATA.append(data)
    cross = audioop.cross(data, 2)
    print cross, ' ',
    if cross > 0:
        print (44100.0/5.0)/cross
    print 
    time.sleep(5.0/sample_rate)

for i in DATA:
    inp.write(data)

print len(DATA)

#plot(DATA)
#show()
