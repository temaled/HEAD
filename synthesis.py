import numpy as np
from sox.transform import Transformer
def happy_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"
	start_time = [0.001,0.058511,0.255319,0.401596]
	end_time = [0.058511,0.255319,0.401596,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	n_bend = len(utterance_begin[0])
	cents = [-200,+140,82.667,0.001]
	happy_patch = Transformer()
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		happy_patch.pitch(n_semitones,False)
		happy_patch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		happy_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_patch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		happy_patch.pitch(n_semitones,False)
		happy_patch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		happy_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_patch.build(filenamein,filenameout)
		
	return happy_patch

def happy_tensed_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	start_time = [0.001,0.255319,0.401596]
	end_time = [0.058511,0.401596,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	n_bend = 3
	cents = [-200,82.667,0.001]
	happy_tensed_patch = Transformer()
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2
		happy_tensed_patch.pitch(n_semitones,False)
		happy_tensed_patch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		happy_tensed_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_tensed_patch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		happy_tensed_patch.pitch(n_semitones,False)
		happy_tensed_patch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
		happy_tensed_patch.equalizer(cutFreq,Qfactor,Gain)
		happy_tensed_patch.build(filenamein,filenameout)

	return happy_tensed_patch

def sad_patch(sampleFrequency,n_semitones,Qfactor,Gain):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	sad_patch = Transformer()
	if (sampleFrequency<=16000):
		cutFreq = sampleFrequency/2.5 
		sad_patch.pitch(n_semitones,False)
		sad_patch.equalizer(cutFreq,Qfactor,Gain)
		sad_patch.build(filenamein,filenameout)
	else:
		cutFreq = 8000
		sad_patch.pitch(n_semitones,False)
		sad_patch.equalizer(cutFreq,Qfactor,Gain)
		sad_patch.build(filenamein,filenameout)

	return sad_patch

def afraid_patch(sampleFrequency,speed,depth,utterance_begin):
	filenamein = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	
	start_time = [0.001,0.111862,0.223777,0.348351]
	end_time = [0.111862,0.223777,0.348351,0.500]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	
	n_bend = len(utterance_begin[0])
	cents = [120,-200,8,200]

	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	
	afraid_patch = Transformer()
	afraid_patch.tremolo(speed,depth)
	afraid_patch.bend(n_bend,inflect_start_times[0],inflect_end_times[0],cents)
	afraid_patch.build(filenamein,filenameout)

	return afraid_patch