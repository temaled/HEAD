from scipy.signal import butter
import numpy as np
from sox.transform import Transformer
FILE_NAME_PATH = "/home/dereje/Desktop/TestFolder/Test.wav"
CUTFREQ = 4000
def happy_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([-200,140,-57.333,0.001,0.001],ndmin=1)
	func = np.polyfit(time,fixed_cents,4)
	inflect_func = np.poly1d(func)
	cents = inflect_func(normalized_time_stamps)
	return cents.tolist()
def afraid_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([120,-200,208,192,-192],ndmin=1)
	func = np.polyfit(time,fixed_cents,4)
	inflect_func = np.poly1d(func)
	cents = inflect_func(normalized_time_stamps)
	return cents.tolist()
def happy_tensed_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([-200,0.001,82.667,-82.667,0.001],ndmin=1)
	func = np.polyfit(time,fixed_cents,4)
	inflect_func = np.poly1d(func)
	cents = inflect_func(normalized_time_stamps)
	return cents.tolist()
def normalize_function(utterance_time_stamps):
	normal = max(utterance_time_stamps) - min(utterance_time_stamps)
	utterance_time_stamps = (utterance_time_stamps-min(utterance_time_stamps))/normal
	normal_two = 0.5 - 0.01
	normailzed_utterance  = (utterance_time_stamps * normal_two) + 0.01
	return normailzed_utterance 
def start_end_times(utterance_begin):
	start_time_now = []
	end_time_now = []
	for i in range(len(utterance_begin)):
		start_time_now.append(utterance_begin[i][:-1])
		end_time_now.append(utterance_begin[i][1:])
	start_time_now = np.asarray(start_time_now)
	end_time_now = np.asarray(end_time_now)
	return start_time_now,end_time_now
def happy_cents_for_utterance(start_time_now):
	cents = []
	for i in range(len(start_time_now)):
		cents.append(happy_inflection_function(normalize_function(start_time_now[i])))
	cents = np.concatenate(cents)
	cents = cents.tolist()
	return cents
def afraid_cents_for_utterance(start_time_now):
	cents = []
	for i in range(len(start_time_now)):
		cents.append(afraid_inflection_function(normalize_function(start_time_now[i])))
	cents = np.concatenate(cents)
	cents = cents.tolist()
	return cents
def happy_tensed_cents_for_utterance(start_time_now):
	cents = []
	for i in range(len(start_time_now)):
		cents.append(happy_tensed_inflection_function(normalize_function(start_time_now[i])))
	cents = np.concatenate(cents)
	cents = cents.tolist()
	return cents
def concatenate_list(start_time_now,end_time_now):
	start_time_now = np.concatenate(start_time_now)
	end_time_now = np.concatenate(end_time_now)
	start_time_now = start_time_now.tolist()
	end_time_now = end_time_now.tolist()
	return start_time_now,end_time_now
def sox_init(filenameout,n_semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,Gain,Qfactor):
	patch = Transformer()
	patch.pitch(n_semitones,False)
	patch.bend(number_of_bends,start_time_now,end_time_now,cents,50)			
	patch.treble(Gain,CUTFREQ,0.5)
	patch.equalizer(CUTFREQ,Qfactor,Gain)
	patch.build(FILE_NAME_PATH,filenameout)
	return patch
def afraid_sox_init(speed,depth,number_of_bends,start_time_now,end_time_now,cents,filenameout):
	patch = Transformer()
	patch.tremolo(speed,depth)
	patch.bend(number_of_bends,start_time_now,end_time_now,cents,50)			
	patch.build(FILE_NAME_PATH,filenameout)
	return patch
def sad_sox_init(n_semitones,Gain,CUTFREQ,filenameout):
	CUTFREQ = 3500
	patch = Transformer()
	patch.pitch(n_semitones,False)
	patch.treble(Gain,CUTFREQ,0.5)	
	patch.build(FILE_NAME_PATH,filenameout)
	return patch


def happy_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = happy_cents_for_utterance(start_time_now)
	start_time_now,end_time_now=concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	happy_patch = sox_init(filenameout,n_semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,Gain,Qfactor)
	return happy_patch

def happy_tensed_patch(sampleFrequency,n_semitones,Qfactor,Gain,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = happy_tensed_cents_for_utterance(start_time_now)
	start_time_now,end_time_now=concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	happy_tensed_patch = sox_init(filenameout,n_semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,Gain,Qfactor)
	return happy_tensed_patch


def sad_patch(sampleFrequency,n_semitones,Qfactor,Gain):
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	sad_patch = sad_sox_init(n_semitones,Gain,CUTFREQ,filenameout)
	return sad_patch


def afraid_patch(sampleFrequency,speed,depth,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = afraid_cents_for_utterance(start_time_now)
	start_time_now,end_time_now = concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	afraid_patch = afraid_sox_init(speed,depth,number_of_bends,start_time_now,end_time_now,cents,filenameout)
	return afraid_patch
