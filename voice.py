import alsaaudio, time , audioop
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

sample_rate = 44100

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(sample_rate)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
l_d = []
while True:
    l, data = inp.read()
    #print audioop.max(data,2)
    if audioop.max(data,2) > 10000:
        #for x in xrange(1000):
            l, data = inp.read()
            data_l = np.fromstring(data, 'Int16')
            
            indices = np.where(np.diff(np.sign(data_l)))[0]
            crossings = indices
            #print float(sample_rate)/np.mean(np.diff(crossings))

            time.sleep(1.0/sample_rate)
            time.sleep(1)
        #break

t = arange(0,len(l_d), 1)

#plot(t, l_d)
#print data_l
#indices = find( (data_l[1:] >= 0) & (data_l[:-1] < 0) )
#indices = find((data_l[1:] >= 0) & (data_l[:-1] < 0))
indices = np.where(np.diff(np.sign(data_l)))[0]
crossings = indices
#crossings = [i - data_l[i] / (data_l[i+1] - data_l[i]) for i in indices]
#print data_l
print float(sample_rate)/np.mean(np.diff(crossings))

#raw_input()
#plot(data_l)
#show()
#plot(np.fft.rfft(data_l, 1000))
#show()
