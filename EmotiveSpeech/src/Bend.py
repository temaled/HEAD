from sox.transform import Transformer
from scipy.io import wavfile
import Voiced_Unvoiced as voi
import numpy as np
filename = "/home/dere/Desktop/TestFolder/Test.wav"
fs,x = wavfile.read(filename)
Chunk_Size = 1024
f0 = voi.pitchdetect(x,fs,Chunk_Size)
X = voi.Data_Blocks(x,Chunk_Size)
IBS = [1,2,3,13,14,15]
Start_times = np.arange(1,10)
End_times = Start_times[-1] + np.arange(1,3) 

PitchBend = Transformer()

picthshifts = [-200,140,82.667,0,0]
PitchBend.bend(x/2,len(x/2),End_times,picthshifts,25,16)
