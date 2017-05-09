import numpy as np
from sox.transform import Transformer
from operator import add
from operator import sub
import time
def HappyPatch(sampleFrequency,n_semitones,Qfactor,Gain,Utterance_Begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"
	start_time = [0.001,0.058511,0.255319,0.401596]
	end_time = [0.058511,0.255319,0.401596,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	Utterance_Begin = np.asarray(Utterance_Begin)
	n_bend = len(Utterance_Begin[0])
	cents = [-200,+140,82.667,0.001]
	HappyPatch = Transformer()
	inflect_start_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + start_time
	inflect_end_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		HappyPatch.pitch(n_semitones,False)
		HappyPatch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		HappyPatch.equalizer(cutFreq,Qfactor,Gain)
		HappyPatch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		HappyPatch.pitch(n_semitones,False)
		HappyPatch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		HappyPatch.equalizer(cutFreq,Qfactor,Gain)
		HappyPatch.build(filenamein,filenameout)
	return HappyPatch

def HappyTensedPatch(sampleFrequency,n_semitones,Qfactor,Gain,Utterance_Begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	start_time = [0.001,0.255319,0.401596]
	end_time = [0.058511,0.401596,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	Utterance_Begin = np.asarray(Utterance_Begin)
	n_bend = 3
	cents = [-200,82.667,0.001]
	HappyTensedPatch = Transformer()
	inflect_start_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + start_time
	inflect_end_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		HappyTensedPatch.pitch(n_semitones,False)
		HappyTensedPatch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		HappyTensedPatch.equalizer(cutFreq,Qfactor,Gain)
		HappyTensedPatch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		HappyTensedPatch.pitch(n_semitones,False)
		HappyTensedPatch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		HappyTensedPatch.equalizer(cutFreq,Qfactor,Gain)
		HappyTensedPatch.build(filenamein,filenameout)
	return HappyTensedPatch

def SadPatch(sampleFrequency,n_semitones,Qfactor,Gain):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	SadPatch = Transformer()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2.5 
		SadPatch.pitch(n_semitones,False)
		SadPatch.equalizer(cutFreq,Qfactor,Gain)
		SadPatch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		SadPatch.pitch(n_semitones,False)
		SadPatch.equalizer(cutFreq,Qfactor,Gain)
		SadPatch.build(filenamein,filenameout)
	return SadPatch

def AfraidPatch(sampleFrequency,speed,depth,Utterance_Begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	
	start_time = [0.001,0.111862,0.223777,0.348351]
	end_time = [0.111862,0.223777,0.348351,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	Utterance_Begin = np.asarray(Utterance_Begin)
	
	n_bend = len(Utterance_Begin[0])
	cents = [120,-200,8,200]

	inflect_start_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + start_time
	inflect_end_times = Utterance_Begin[np.arange(len(Utterance_Begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	
	AfraidPatch = Transformer()
	#AfraidPatch.flanger(0,depth,0,30,speed,'sine')
	AfraidPatch.tremolo(speed,depth)
	AfraidPatch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
	AfraidPatch.build(filenamein,filenameout)
	
	
	return AfraidPatch