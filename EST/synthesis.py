from scipy.signal import butter
import numpy as np
from sox.transform import Transformer
FILE_NAME_PATH = "/home/dereje/Desktop/TestFolder/Test.wav"

def happy_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"

	start_time = [-0.127,-0.19747,-0.128,-0.110304]
	end_time = [-0.06948,-0.0001,0.017596,0.000]
	utterance_begin = np.asarray(utterance_begin)
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_start_times = np.concatenate(inflect_start_times)
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_end_times = np.concatenate(inflect_end_times)
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	n_bend = len(inflect_start_times)
	cents = [(140 + n_semitones*100 ),-(n_semitones*100 + 57.333),-82.667,-0.003]
	
	
	cents = np.asarray(cents)
	factor = n_bend/4
	cents =np.asarray([cents]* factor)
	cents = np.concatenate(cents)
	cents = cents.tolist()
	happy_patch = Transformer()
	happy_patch.pitch(n_semitones,False)
	cutFreq = sampleFrequency/2
	
	happy_patch.bend(n_bend,inflect_start_times,inflect_end_times,cents,50)				
	
	happy_patch.treble(Gain,cutFreq,0.5)
	#happy_patch.equalizer(cutFreq,Qfactor,Gain)
	happy_patch.build(FILE_NAME_PATH,filenameout)
	
	return happy_patch

def happy_tensed_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	start_time = [-0.127,-0.197489,-0.128,-0.110404]
	end_time = [-0.069490,-0.001,0.017595,-0.012]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	
	
	
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_start_times = np.concatenate(inflect_start_times)
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = np.concatenate(inflect_end_times)
	inflect_end_times = inflect_end_times.tolist()
	
	n_bend = len(inflect_start_times)
	cents = [0.001,0.001,(n_semitones*100 +82.667),-(n_semitones*100 + 82.667)]
	cents = np.asarray(cents)
	factor = n_bend/4
	cents =np.asarray([cents]*factor)
	cents = np.concatenate(cents)
	cents = cents.tolist()

	cutFreq = sampleFrequency/2
	happy_tensed_patch  = Transformer()
	happy_tensed_patch.vad(-1,True,7.0,0.25,1.0,0.25,0.0)
	happy_tensed_patch.pitch(n_semitones,False)
	happy_tensed_patch.treble(Gain,cutFreq,0.5)	
	#happy_tensed_patch.equalizer(cutFreq,Qfactor,Gain)
	happy_tensed_patch.bend(n_bend,inflect_start_times,inflect_end_times,cents,50)			
	happy_tensed_patch.build(FILE_NAME_PATH,filenameout)
	
	return happy_tensed_patch

def sad_patch(sampleFrequency,n_semitones,Qfactor,Gain):
	
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	sad_patch = Transformer()
	cutFreq = sampleFrequency/2.5 
	sad_patch.pitch(n_semitones,False)
	sad_patch.equalizer(cutFreq,Qfactor,Gain)
	sad_patch.build(FILE_NAME_PATH,filenameout)
	return sad_patch

def afraid_patch(sampleFrequency,speed,depth,utterance_begin):
	
	filenameout1 = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	
	start_time = [-0.127,-0.144138,-0.161,-0.035649]
	end_time = [-0.016139,-0.034,-0.035649,-0.012]
	start_time = np.asarray(start_time)
	end_time = np.asarray(end_time)
	utterance_begin = np.asarray(utterance_begin)
	
	
	inflect_start_times = utterance_begin[np.arange(len(utterance_begin))] + start_time
	inflect_start_times = np.concatenate(inflect_start_times)
	inflect_end_times = utterance_begin[np.arange(len(utterance_begin))] + end_time
	inflect_end_times = np.concatenate(inflect_end_times)
	inflect_start_times = inflect_start_times.tolist()
	inflect_end_times = inflect_end_times.tolist()
	
	n_bend = len(inflect_start_times)
	cents = [-200,+208,+192,-200]
	cents = np.asarray(cents)
	factor = n_bend/4
	cents = np.asarray([cents]*factor)
	cents = np.concatenate(cents)
	cents = cents.tolist()

	afraid_patch = Transformer()
	afraid_patch.tremolo(speed,depth)
	afraid_patch.bend(n_bend,inflect_start_times,inflect_end_times,cents,50)			
	afraid_patch.build(FILE_NAME_PATH,filenameout1)

	return afraid_patch
