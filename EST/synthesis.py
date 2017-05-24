from scipy.signal import butter
import numpy as np
from sox.transform import Transformer
FILE_NAME_PATH = "/home/dereje/Desktop/TestFolder/Test.wav"
CUTFREQ = 4000
QFACTOR = 1
PARAMETER_CONTROL = 1
def appended_utterance_time_stamps(CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block):
	utterance_time_stamps = []
	for i in range(len(selected_inflect_block)):
		utterance_time_stamps.append(TIME_STAMPS[selected_inflect_block[i][:CONSECUTIVE_BLOCKS]])
	utterance_time_stamps = np.asarray(utterance_time_stamps)
	return utterance_time_stamps
def happy_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([0.001,140,82.667,-82.667,0.001],ndmin=1)
	func = np.polyfit(time,fixed_cents,4)
	inflect_func = np.poly1d(func)
	cents = inflect_func(normalized_time_stamps)
	return cents.tolist()
def afraid_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([120,0.01,8,192,-192],ndmin=1)
	func = np.polyfit(time,fixed_cents,4)
	inflect_func = np.poly1d(func)
	cents = inflect_func(normalized_time_stamps)
	return cents.tolist()
def happy_tensed_inflection_function(normalized_time_stamps):
	time = np.array([0.01,0.058511,0.255319,0.401596,0.500],ndmin=1)
	fixed_cents = np.array([0.001,0.001,82.667,-82.667,0.001],ndmin=1)
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
def happy_sox_init(filenameout,semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,gain,QFACTOR):
	patch = Transformer()
	patch.pitch(semitones,False)
	patch.bend(number_of_bends,start_time_now,end_time_now,cents,50)			
	patch.treble(gain,CUTFREQ,0.5)
	patch.equalizer(CUTFREQ,QFACTOR,gain)
	patch.build(FILE_NAME_PATH,filenameout)
	return patch
def afraid_sox_init(speed,depth,number_of_bends,start_time_now,end_time_now,cents,filenameout):
	patch = Transformer()
	patch.tremolo(speed,depth)
	patch.bend(number_of_bends,start_time_now,end_time_now,cents,50)			
	patch.build(FILE_NAME_PATH,filenameout)
	return patch
def sad_sox_init(semitones,gain,CUTFREQ,filenameout):
	CUTFREQ = 3500
	patch = Transformer()
	patch.pitch(semitones,False)
	patch.treble(gain,CUTFREQ,0.5)	
	patch.build(FILE_NAME_PATH,filenameout)
	return patch


def happy_patch(sampleFrequency,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappy.wav"
	gain = 3.0
	semitones = 1.0 * PARAMETER_CONTROL
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = happy_cents_for_utterance(start_time_now)
	start_time_now,end_time_now=concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	happy_patch = happy_sox_init(filenameout,semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,gain,QFACTOR)
	return happy_patch

def happy_tensed_patch(sampleFrequency,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestTensedHappy.wav"
	gain = 3.0
	semitones = 2.0 * PARAMETER_CONTROL
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = happy_tensed_cents_for_utterance(start_time_now)
	start_time_now,end_time_now=concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	happy_tensed_patch = happy_sox_init(filenameout,semitones,number_of_bends,start_time_now,end_time_now,cents,CUTFREQ,gain,QFACTOR)
	return happy_tensed_patch


def sad_patch(sampleFrequency):
	filenameout = "/home/dereje/Desktop/TestFolder/TestSad.wav"
	gain = 0.25
	semitones = -1.5 * PARAMETER_CONTROL
	sad_patch = sad_sox_init(semitones,gain,CUTFREQ,filenameout)
	return sad_patch


def afraid_patch(sampleFrequency,utterance_begin):
	filenameout = "/home/dereje/Desktop/TestFolder/TestAfraid.wav"
	speed = 8.5
	depth = 1 + (60 * PARAMETER_CONTROL)
	start_time_now,end_time_now=start_end_times(utterance_begin)
	cents = afraid_cents_for_utterance(start_time_now)
	start_time_now,end_time_now = concatenate_list(start_time_now,end_time_now)
	number_of_bends = len(start_time_now)
	afraid_patch = afraid_sox_init(speed,depth,number_of_bends,start_time_now,end_time_now,cents,filenameout)
	return afraid_patch
