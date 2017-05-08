from sox.transform import Transformer
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import *
import numpy as np

def Happy_Filter(fs,snd_array):
	Qfactor = 1
	Gain = 3.0
	if (fs<=8000):
		cutFreq = fs/2
		snd_high_shelf_array = equalizer(cutFreq,Qfactor,Gain)
	else:
		cutFreq = 8000
		snd_high_shelf_array = equalizer(cutFreq,Qfactor,Gain)
	return snd_high_shelf_array
def Sad_Filter(fs,snd_array):
	Qfactor = 1
	Gain = 0.25
	if (fs<=8000):
		cutFreq = fs/2
		snd_high_shelf_array = equalizer(cutFreq,Qfactor,Gain)
	else:
		cutFreq = 8000
		snd_high_shelf_array = equalizer(cutFreq,Qfactor,Gain)
	return snd_high_shelf_array
def equalizer(cutFreq,Qfactor,Gain):
	EQ = Transformer()
	EQ.equalizer(cutFreq,Qfactor,Gain)
	filenameIn = "/home/dereje/Desktop/TestFolder/TestHappyPitch.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestFiltered.wav"
	EQ.build(filenameIn,filenameout)
	fs,EqualizedArray = wavfile.read(filenameout)
	return EqualizedArray
