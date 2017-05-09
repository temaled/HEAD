import numpy as np
from scipy.io import wavfile
import warnings
warnings.filterwarnings('ignore')
from scipy.fftpack import rfft,irfft,fftfreq
import pysptk
def pitch_detect(sndarray,fs, chunk_size):
    new_sndarray = np.asarray(np.float64(sndarray))
    f0 = pysptk.swipe(np.asarray(new_sndarray), fs, chunk_size, 65,500,0.001,1) 
    return f0
def stft(x,Chunk_Size,overlap=1):
	import scipy
	hop = Chunk_Size / overlap
	w = scipy.hanning(Chunk_Size+1)[:-1]
	cnt = 0
	return np.array([np.fft.rfft(w*x[i:i+Chunk_Size]) for i in range (0,len(x)-Chunk_Size,hop)])
def root_mean_square(wavedata,Chunk_Size,fs):
	num_blocks = int(np.ceil(len(wavedata)/Chunk_Size))
	timestamps = (np.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))

	rms = []
	for i in range(0,num_blocks-1):
		start = i*Chunk_Size
		stop = np.min([(start + Chunk_Size -1),len(wavedata)])

		rms_seg = np.sqrt(np.mean(wavedata[start:stop]**2))
		rms.append(rms_seg)
	return np.asarray(rms), np.asarray(timestamps)
def wavefileread(filename):
	fs,x = wavfile.read(filename)
	return fs , x

	fs,x = wavfile.read(filename)
	Chunk_Size = 1024
	num_blocks = int(np.ceil(len(x)/Chunk_Size)) 
def Preprocess(Voiced_Samples):
	IVS = np.array(vSig['VSamp'])
	return IVS

def Potential_Inflection_Fundamental_Frequency(Fundamental_Frequency_of_Voiced_Samples): 
	Freqin = np.array(f0[IVS])	
	return Freqin

def Matrix_of_Sample_Numbers(IVS):     	
	InSamp = []
	for i in range(0,len(IVS)-1):
	  	if RMS[i] <= np.nanmean(RMS):
	 		InSamp.append(IVS[i])
	# [InSamp] This matrix contains sample numbers for a difference 
	# of voiced samples that are less than the mean of the RMS values. 
	# According to D.A.V.I.D, this samples are recorded as attack  
	# Since we will be applying inflection on new utterance,
	# This will help for classifications amongst voiced samples.  
	return InSamp
def Consecutive_Blocks_for_Inflection(InSamp,Conblocks):
	#---"Iblocks" is the consecutive blocks for inflection----#
	Iblocks =[]
	for i in range(0 , len(InSamp)-1):
		Iblocks.append(InSamp[i] + np.arange(Conblocks))
	Iblocks = np.array(Iblocks)		 
	return Iblocks
def Alteration_of_Discrete_Data(InSamp,Conblocks,Iblocks):
	
	IblocksSelected = []
	for i in range(len(InSamp)-1):
		if (np.abs(Iblocks[i][0] - Iblocks[i-1][0]))> 2*(Conblocks-1):
			IblocksSelected.append(Iblocks[i])
	IblocksSelected = np.array(IblocksSelected)
	# 'IblocksSelected' are the selected blocks that are used for inflection.
	# They are selected by comparing the first element of the Iblock.
	# 'IblocksSelected' are blocks selected in such a way that 
	# overlappig/consecutive blocks are not used during inflection.
	# It contains 21 consecutive blocks.
	return IblocksSelected
def Consecutive_Blocks_In_Selected_Blocks(IblocksSelected,Conblocks):
	n = (Conblocks/(Conblocks/3)) * len(IblocksSelected)
	# n are the consecutive blocks within the 'IblocksSelected' 
	# Are blocks that can be  altered with Pitch Up followed by Pitch Down then resolve to normal.
	return n
def Reshaped_Inflection_Blocks(n,IblocksSelected,Conblocks):
	IBS = (np.reshape(IblocksSelected,(n,Conblocks/3))).flatten()
	# IBS is the reshaped Inflection Blocks for the purpose of categorizing blocks for Inflection 
	# Based on 'n' The IBS is used for the classification of:  
	return IBS
def Difference_Arrays(num_blocks,IBS):
	A = np.array(np.arange(num_blocks))
	B = np.array(IBS.flatten())
	DiffArrays = np.array(list(set(A)-set(B)))
	return DiffArrays
if __name__ == '__main__':
	filename = "/home/dereje/Desktop/SoundFolder/Test.wav" 
	fs,x = wavfile.read(filename)
	Chunk_Size = 1024
	Spectral_Analysis = stft(x,Chunk_Size)
	rmsx = root_mean_square(x,Chunk_Size,fs)
	