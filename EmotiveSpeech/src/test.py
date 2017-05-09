from scipy.io import wavfile
from numpy import inf
import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt
import Analysis as alysis
import Voiced_Unvoiced as voi

filename = "/home/dereje/Desktop/HarvardSentences/Test1.wav"
fs,x = wavfile.read(filename)
Chunk_Size = 1024
f0 = alysis.pitch_detect(x,fs,Chunk_Size)
#CriticalPoints = [0,-0.6,0.6,-0.4,0]
#Ypts = [-200,140,82.667,0,0]

Xpts = np.array([0,58.511,255.319,401.596,500],ndmin=1)
Ypts = np.array([-200,140,82.667,0,0],ndmin=1)

Func = np.polyfit(Xpts,Ypts,4)

InflectFunc = np.poly1d(Func)
Regions = np.arange(0,500,25)

InflectRegions = np.array(InflectFunc(Regions[np.arange(0,len(Regions)-1)]))

oldFreq = f0[51:70]
newFreq = oldFreq + InflectRegions
Threshold = (newFreq/oldFreq).flatten()
Threshold[Threshold == inf] = 1
#print Threshold


xold = x[51*Chunk_Size:70*Chunk_Size]
old_Data_Frequency_obj = {"Xold":xold,"Freqold":oldFreq}
Xold = voi.Data_Blocks(xold,Chunk_Size)

cnt = 0
ModifiedX = []
for i in range(len(newFreq)):
	ModifiedX.append(Xold[i] * Threshold[i])
	cnt+=1
ModifiedX =np.int16(np.array(ModifiedX))
ModifiedX = ModifiedX.flatten()
#print ModifiedX


xp = np.linspace(0,500,25)


filename1 = "/home/dereje/Desktop/HarvardSentences/Testxold.wav"
filename2 = "/home/dereje/Desktop/HarvardSentences/TestxModified.wav"

wavfile.write(filename1,fs,np.array(xold))
wavfile.write(filename2,fs,np.array(ModifiedX))
#----------------------------------------------New-------------------------------------#
