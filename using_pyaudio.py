import numpy as np
import pyaudio
from time import sleep
import sys, os, fcntl

fl = fcntl.fcntl(sys.stdin.fileno(),fcntl.F_GETFL)
fcntl.fcntl(sys.stdin.fileno(),fcntl.F_SETFL,fl | os.O_NONBLOCK)

pyaud = pyaudio.PyAudio()

stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 44100,
    input = True)

while True:
    try:
        rawsamps = stream.read(1024)
        samps = np.fromstring(rawsamps, dtype=np.int16)
    except: print "failed"
    indices = np.where(np.diff(np.sign(samps)))[0]
    freq = 1024.0/np.mean(np.diff(indices))
    print freq
    try:
        stdin = sys.stdin.read()
        if "\n" in stdin or "\r" in stdin:
            break
    except IOError: pass
