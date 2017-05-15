import numpy as np
from sox.transform import Transformer
FILE_NAME_PATH = "/home/dereje/Desktop/TestFolder/Test.wav"
	
def happy_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"
	
	start_time = [-0.127,-0.197489,-0.128,-0.110404]
	end_time = [-0.069489,0.000,0.017596,-0.012]
	utterance_begin = np.asarray(utterance_begin)
	
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	n_bend = 4
	cents = [+290,-57.333,-32.667,0.001]
	
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	
	happy_patch = Transformer()
	happy_patch.pitch(n_semitones,False)
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		for i in range(len(utterance_begin)-1):
			happy_patch = Transformer()
			happy_patch.bend(n_bend,inflect_start_times[i],inflect_end_times[i],cents)			
		happy_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_patch.build(FILE_NAME_PATH,filenameout)
	else:
		cutFreq = 8000
	
		for i in range(len(utterance_begin)-1):
			happy_patch.bend(n_bend,inflect_start_times[i],inflect_end_times[i],cents)
		happy_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_patch.build(FILE_NAME_PATH,filenameout)
	return happy_patch

def happy_tensed_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	start_time = [-0.127,-0.197489,-0.128,-0.110404]
	end_time = [-0.069489,0.000,0.017596,-0.012]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	
	n_bend = 4
	cents = [0.001,0.001,+82.667,-82.667]
	happy_tensed_patch = Transformer()
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	happy_tensed_patch  = Transformer()
	happy_tensed_patch.pitch(n_semitones,False)
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		for i in range(len(utterance_begin)-1):
			happy_tensed_patch = Transformer()
			happy_tensed_patch.bend(n_bend,inflect_start_times[i],inflect_end_times[i],cents)			
		happy_tensed_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_tensed_patch.build(FILE_NAME_PATH,filenameout)
	else:
		cutFreq = 8000
		for i in range(len(utterance_begin)-1):
			happy_tensed_patch.bend(n_bend,inflect_start_times[i],inflect_end_times[i],cents)			
		happy_tensed_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_tensed_patch.build(FILE_NAME_PATH,filenameout)
	return happy_tensed_patch

def sad_patch(sampleFrequency,n_semitones,Qfactor,Gain):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	sad_patch = Transformer()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2.5 
		sad_patch.pitch(n_semitones,False)
		sad_patch.equalizer(cutFreq,Qfactor,Gain)
		sad_patch.build(FILE_NAME_PATH,filenameout)
	else:
		cutFreq = 8000
		sad_patch.pitch(n_semitones,False)
		sad_patch.equalizer(cutFreq,Qfactor,Gain)
		sad_patch.build(FILE_NAME_PATH,filenameout)

	return sad_patch

def afraid_patch(sampleFrequency,speed,depth,utterance_begin):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	
	
	start_time = [-0.127,-0.144138,-0.161,-0.035649]
	end_time = [-0.016138,-0.033,-0.035649,-0.012]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	
	n_bend =4
	cents = [-200,+208,+192,-200]

	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	
	afraid_patch = Transformer()
	afraid_patch.tremolo(speed,depth)
	for i in range(len(utterance_begin)-1):
			afraid_patch = Transformer()
			afraid_patch.bend(n_bend,inflect_start_times[i],inflect_end_times[i],cents)			
	afraid_patch.build(FILE_NAME_PATH,filenameout)
	afraid_patch.build(FILE_NAME_PATH,filenameout)

	return afraid_patch
