from scipy.io import wavfile
from numpy import inf
import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt
import Analysis as alysis
import Voiced_Unvoiced as voi
from scipy.io.wavfile import write
from sox.transform import Transformer
filename = "/home/dereje/Desktop/HarvardSentences/Test1.wav"
filenameout = "/home/dereje/Desktop/HarvardSentences/TestVibr.wav"
fs,x = wavfile.read(filename)
Chunk_Size = 1024

Vibrato = Transformer()
Vibrato.tremolo(8.5,100)
Vibrato.build(filename,filenameout)


