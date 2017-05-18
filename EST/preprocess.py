import numpy as np
from numpy import nan
from scipy.io import wavfile
import warnings
warnings.filterwarnings('ignore')
from scipy.fftpack import rfft,irfft,fftfreq

def stft(x,Chunk_Size,overlap=1):
	import scipy
	hop = Chunk_Size / overlap
	w = scipy.hanning(Chunk_Size+1)[:-1]
	cnt = 0
	return np.array([np.fft.rfft(w*x[i:i+Chunk_Size]) for i in range (0,len(x)-Chunk_Size,hop)])
def root_mean_square(x,Chunk_Size,fs):
	num_blocks = int(np.ceil(len(x)/Chunk_Size))
	timestamps = (np.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
	rms = []
	for i in range(0,num_blocks-1):
		start = i*Chunk_Size
		stop = np.min([(start + Chunk_Size -1),len(x)])
		rms_seg = np.sqrt(np.mean(x[start:stop]**2))
		rms.append(rms_seg)
	#---This is a computation for the RMS values, This will help in identifying which blocks are used for inflection----#
	return np.nan_to_num(np.asarray(rms))
def wave_file_read(filename):
	fs,x = wavfile.read(filename)
	return fs , x
def utterance_region_begin_samples(voiced_samples):
	voice_sample_begin = []
	voice_sample_index = []
	for i in range(len(voiced_samples)):
		if np.abs((voiced_samples[i] - voiced_samples[i-1]))>1:
			voice_sample_begin.append(voiced_samples[i])
			voice_sample_index.append(i)
	return np.asarray(voice_sample_begin),np.asarray(voice_sample_index)
def utterance_chunk(voiced_samples,voice_sample_index):
	voiced_chunk_samples = []
	for i in range (len(voice_sample_index)-1):
		voiced_chunk_samples.append(voiced_samples[voice_sample_index[i]:voice_sample_index[i+1]])
	voiced_chunk_samples.append(voiced_samples[voice_sample_index[-1]:voiced_samples[-1]])
	return voiced_chunk_samples
def pre_process(Voiced_Samples):
	inflection_voices_samples = np.array(Voiced_Samples)
	return np.asarray(inflection_voices_samples)

def potential_inflection_fundamental_frequency(Fundamental_Frequency_of_Voiced_Samples): 
	inflect_frequency = np.array(Fundamental_Frequency_of_Voiced_Samples)	
	return inflect_frequency

def matrix_of_sample_numbers(RMS,inflection_voices_samples):     	
	InSamp = []
	for i in range(0,len(inflection_voices_samples)-1):
	  	if (RMS[i]<np.mean(RMS) or (RMS[i]==0)):
	 		InSamp.append(inflection_voices_samples[i])
	# [InSamp] This matrix contains sample numbers for a difference 
	# of voiced samples that are less than the mean of the RMS values. 
	# According to D.A.V.I.D, this samples are recorded as attack  
	# Since we will be applying inflection on new utterance,
	# This will help for classifications amongst voiced samples.  
	return np.asarray(InSamp)
def consecutive_blocks_for_inflection(InSamp,Conblocks):
	#---"inflect_blocks" is the consecutive blocks for inflection----#
	inflect_blocks =[]
	for i in range(len(InSamp)):
		inflect_blocks.append(InSamp[i] + np.arange(Conblocks))
	inflect_blocks = np.array(inflect_blocks)		 
	return inflect_blocks
def alteration_of_discrete_data(InSamp,Conblocks,inflect_blocks):
	
	selected_inflect_block = []
	for i in range(len(InSamp)):
		if (np.abs(inflect_blocks[i][0] - inflect_blocks[i-1][0]))> 2*(Conblocks-1):
			selected_inflect_block.append(inflect_blocks[i])
	selected_inflect_block = np.array(selected_inflect_block)
	if (selected_inflect_block==[]):
		selected_inflect_block = inflect_blocks[0]
	
	# 'selected_inflect_block' are the selected blocks that are used for inflection.
	# They are selected by comparing the first element of the Inflect block.
	# 'selected_inflect_block' are blocks selected in such a way that 
	# overlappig/consecutive blocks are not used during inflection.
	# It contains 21 consecutive blocks.
	return selected_inflect_block
def consecutive_blocks_in_selected_blocks(selected_inflect_block,Conblocks):
	n = (Conblocks/(Conblocks/3)) * len(selected_inflect_block)
	# n are the consecutive blocks within the 'selected_inflect_block' 
	# Are blocks that can be  altered with Pitch Up followed by Pitch Down then resolve to normal.
	return n
def reshaped_inflection_blocks(n,selected_inflect_block,Conblocks):
	Inflection_Block_Samples = (np.reshape(selected_inflect_block,(n,Conblocks/3))).flatten()
	# Inflection_Block_Samples is the reshaped Inflection Blocks for the purpose of categorizing blocks for Inflection 
	# Based on 'n' The Inflection_Block_Samples is used for the classification of:  
	return Inflection_Block_Samples
def difference_arrays(num_blocks,Inflection_Block_Samples):
	A = np.array(np.arange(num_blocks))
	B = np.array(Inflection_Block_Samples.flatten())
	DiffArrays = np.array(list(set(A)-set(B)))
	return DiffArrays

	