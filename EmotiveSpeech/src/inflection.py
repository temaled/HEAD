from scipy.io import wavfile
from numpy import inf
import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt
import Analysis as alysis
import Voiced_Unvoiced as voi


def happy_inflection_module(snd_array,Chunk_Size,Utterance_Regions,detect):
	Xpts = np.array([0,58.511,255.319,401.596,500],ndmin=1)
	Ypts = np.array([-200,140,82.667,0,0],ndmin=1)

	Func = np.polyfit(Xpts,Ypts,4)

	InflectFunc = np.poly1d(Func)
	
	Regions = (np.arange(0,500,500/np.float32(len(Utterance_Regions))))/1
	

	
	InflectRegions = np.array(InflectFunc(Regions[np.arange(0,len(Regions))]))
	
	newFreq = Utterance_Regions + InflectRegions
	Threshold = (newFreq/Utterance_Regions).flatten()
	Threshold[Threshold == inf] = 0.8
	
	
	Xold = voi.Data_Blocks(snd_array,Chunk_Size)
	ModifiedX = []
	for i in range(len(newFreq)-1):
		ModifiedX.append(Xold[i] * Threshold[i])

	ModifiedX =np.int16(np.array(ModifiedX))
	ModifiedX = ModifiedX.flatten()
 
	return ModifiedX