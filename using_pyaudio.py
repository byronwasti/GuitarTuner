import numpy as np
import pyaudio
from time import sleep
import sys, os, fcntl

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

''' THE MAIN LOOP '''
while True:
    for x in xrange(num_samples):
        try:
            rawsamps = stream.read(1024)
            samps = np.fromstring(rawsamps, dtype=np.int16)
        except: print "failed"

        indices = np.where(np.diff(np.sign(samps)))[0]
        freq = 1024.0/np.mean(np.diff(indices))

        FREQ[x] = freq

        avg = sum(FREQ)/float(num_samples)

        for i in GFREQ:
            if i - THRESH < avg < i + THRESH:
                print GUITAR_STRINGS_K[i], avg
                pass

        try:
            stdin = sys.stdin.read()
            if "\n" in stdin or "\r" in stdin:
                break
        except IOError: print "No IO"
