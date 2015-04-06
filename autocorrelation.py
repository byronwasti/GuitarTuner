from numpy.fft import rfft, irfft
from scipy.signal import fftconvolve
from matplotlib.mlab import find
import numpy as np
import pyaudio
from time import sleep
import sys, os, fcntl
import serial
import struct

''' VARIABLE DEFINITIONS '''
num_samples = 10
FREQ = [0]*num_samples
MORE_SAMP = [0] * num_samples
GUITAR_STRINGS = { 'E2':82.41, 'A2':110.00, 'D3':146.83, 'G3':196.00,'B3':246.94, 'E4':329.63 }
GUITAR_STRINGS_K = { 82.41:'E2', 110.00:'A2', 146.83:'D3', 196.00:'G3', 246.94:'B3', 329.63:'E4'}
GFREQ = [ 82.41, 110.00, 146.83, 196.00, 246.94, 329.63 ]
THRESH = 2

''' UNIX STDIN SETUP '''
fl = fcntl.fcntl(sys.stdin.fileno(),fcntl.F_GETFL)
fcntl.fcntl(sys.stdin.fileno(),fcntl.F_SETFL,fl | os.O_NONBLOCK)

''' SETTING UP PYAUDIO '''
pyaud = pyaudio.PyAudio()
stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input = True)

s = serial.Serial('/dev/ttyACM0',9600, timeout=50)
sleep(2)

''' PARABOLIC '''
def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
   
    f is a vector and x is an index for that vector.
   
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
   
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
   
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
   
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
   
    """
    xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

''' THE MAIN LOOP '''
while True:
    samps = []
    for x in xrange(num_samples):
        try:
            rawsamps = stream.read(1024)
            sampler = np.fromstring(rawsamps, dtype=np.int16)
            for i in sampler:
                samps.append(i)
        except: pass #print "failed"
        
    corr = fftconvolve(samps, samps[::-1], mode='full')
    corr = corr[len(corr)/2:]

    d = np.diff(corr)
    start = find(d > 0)[0]

    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)
    
    avg = 44100.0/px
    if int(avg) == 82: break
    if avg < 100:
        print str(int(avg))
        s.write(struct.pack('>B',avg))
        tmp = s.readline()
        print tmp
    

    '''
    for i in GFREQ:
        if i - THRESH < avg < i + THRESH:
            print GUITAR_STRINGS_K[i], avg
            pass
    '''

    try:
        stdin = sys.stdin.read()
        if "\n" in stdin or "\r" in stdin:
            break
    except IOError: pass
