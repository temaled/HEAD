from scipy.io import wavfile
import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt
import Analysis as alysis
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
#print InflectRegions
#print f0[51:70]
oldFreq = f0[51:70]
newFreq = oldFreq + InflectRegions
xold = x[51*Chunk_Size:70*Chunk_Size]
old_Data_Frequency_obj = {"Xold":xold,"Freqold":oldFreq}
print old_Data_Frequency_obj
xp = np.linspace(0,500,25)

#plt.plot(Xpts,Ypts,'.',xp,InflectFunc(xp))
#plt.show()
plt.plot(newFreq,oldFreq)

plt.show()
filename1 = "/home/dereje/Desktop/HarvardSentences/Testneww.wav"

wavfile.write(filename1,fs,np.array(x))