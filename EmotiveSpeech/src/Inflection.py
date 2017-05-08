from scipy.io import wavfile
from numpy import inf
import numpy as np
from scipy.signal import *
import matplotlib.pyplot as plt
import Analysis as alysis
import Voiced_Unvoiced as voi
import Filter as ft

def cents_to_hertzratio(Cents):
	Raisedto = Cents/(np.float64(1200))
	hertzratio = np.power(2,Raisedto)
	return hertzratio

def happy_Inflection_module(fs,FrameLength,snd_array,VoicedRegions,Chunk_Size,Utterance_Regions):
	Xpts = np.array([0,58.511,255.319,401.596,500],ndmin=1)
	Ypts = np.array([-200,140,82.667,0,0],ndmin=1)

	Func = np.polyfit(Xpts,Ypts,4)

	InflectFunc = np.poly1d(Func)
	
	Regions = (np.arange(0,500,500/np.float32(len(Utterance_Regions))))
		

	InflectRegions = np.float16(InflectFunc(Xpts))
	
	
	f0old = Utterance_Regions.flatten()
	
	FrameLength_in_msec = FrameLength*1000
	
	Threshold = [cents_to_hertzratio(Ypts[0]),
				 cents_to_hertzratio(InflectFunc(FrameLength_in_msec) - Ypts[0]),
				 cents_to_hertzratio(Ypts[2])]
	
	
	
	Utterance_Regions[0] = Utterance_Regions[0] * cents_to_hertzratio(-200)
	for i in range(len(Utterance_Regions)/2 -1):
		Utterance_Regions[i+1] = Utterance_Regions[i] * Threshold[i+1]
	
	
	newFreq = Utterance_Regions
	FreqThreshold = newFreq/f0old
	FreqThreshold = np.nan_to_num(FreqThreshold)
	FreqThreshold = np.abs(FreqThreshold)
	
	

	VoicedRegions = np.float64(VoicedRegions)
	for i in range(len(newFreq)):
		VoicedRegions[i] *=  FreqThreshold[i]

	

	VoicedRegions = np.resize(VoicedRegions,(len(newFreq),Chunk_Size))
	ModifiedX = np.int16(np.array(VoicedRegions))
	ModifiedX = ModifiedX.flatten()

	return ModifiedX
def happy_Tensed_Inflection_module(fs,FrameLength,snd_array,VoicedRegions,Chunk_Size,Utterance_Regions):
	Xpts = np.array([0,58.511,255.319,401.596,500],ndmin=1)
	Ypts = np.array([-200,140,82.667,0,0],ndmin=1)

	Func = np.polyfit(Xpts,Ypts,4)

	InflectFunc = np.poly1d(Func)
	
	Regions = (np.arange(0,500,500/np.float32(len(Utterance_Regions))))
		

	InflectRegions = np.float16(InflectFunc(Xpts))
	
	
	f0old = Utterance_Regions.flatten()
	
	FrameLength_in_msec = FrameLength*1000
	
	Threshold = [cents_to_hertzratio(Ypts[0]),
				 cents_to_hertzratio(Ypts[2])]
	
	
	
	Utterance_Regions[0] = Utterance_Regions[0] * Threshold[0]
	Utterance_Regions[1] = Utterance_Regions[0] * Threshold[1]
		
	
	newFreq = Utterance_Regions
	FreqThreshold = newFreq/f0old
	FreqThreshold = np.nan_to_num(FreqThreshold)
	FreqThreshold = np.abs(FreqThreshold)
	
	

	VoicedRegions = np.float64(VoicedRegions)
	for i in range(len(newFreq)):
		VoicedRegions[i] *=  FreqThreshold[i]

	

	VoicedRegions = np.resize(VoicedRegions,(len(newFreq),Chunk_Size))
	ModifiedX = np.int16(np.array(VoicedRegions))
	ModifiedX = ModifiedX.flatten()

	return ModifiedX