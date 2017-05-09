from scipy.io import wavfile
from sox.transform import Transformer
from scipy.signal import *
import Voiced_Unvoiced as voi
from matplotlib import pyplot as plt
from pysptk import swipe
import warnings
warnings.filterwarnings('ignore')

import pysptk
import numpy as np
import Analysis as alysis
import Inflection as inflect
import peakdetect as pd
import phasevocoder	as pv
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import PitchShift as ps
import Filter as ft
import HappyPatch as hp
def EmotiveSpeech(fs,filename,typeOfEmotion):
	fs,x = wavfile.read(filename)
	Chunk_Size = 1024
	num_blocks = int(np.ceil(len(x)/Chunk_Size)) 
	# Blocks of Data by Windowing Through Chunk Size
	Ts = 1/float(fs) * Chunk_Size
	X = voi.Data_Blocks(x,Chunk_Size)
	# Fundamental Frequency 
	
	f0 = alysis.pitch_detect(x,fs,Chunk_Size)
	# Starting Info of Voiced/Unvoiced Regions

	vSig = voi.startinginfo(x,f0,fs,Chunk_Size)
	# Voiced Regions 
	
	Voiced_Regions = voi.Voiced_regions(x,f0,vSig,Chunk_Size)
	#-----Unvoiced Regions-----#
	#UnVoiced_Regions = voi.UnVoiced_regions(x,f0,vSig,Chunk_Size)


	#---This is a computation for the RMS values, these will help in identifying which blocks are used for inflection----#
	RMS = np.asarray(alysis.root_mean_square(x,Chunk_Size,fs)[0])
	


	Voiced_Samples = vSig['VSamp']
	# Inflection Voice Samples(IVS) is a matrix containing potential sample points for inflection. 		
	IVS = np.array(Voiced_Samples)
	
	Frequency_of_Voiced_Samples = f0[IVS]
	# Pitches/Fundamental Frequency of Potetnial Inflection samples [Freqin]
	Freqin = np.array(Frequency_of_Voiced_Samples)
	


	# Execution Time/Duration of a Single Block 
	Ts = 1/float(fs) * Chunk_Size
	# Consecutive Blocks during the Inflection Duration
				#	1Block = Ts
	 			#	?Block = Inflect_Duration

	
	Conblocks = 1 + int(0.5 / Ts)
	#----Matrix of Sample Numbers----#  
	cnt = 0
	cnt1 = 0
	InSamp = []
	for i in range(0,len(IVS)-1):
	  	if RMS[i] <= np.nanmean(RMS):
	 		InSamp.append(IVS[i])
	 		cnt += 1
	 	# [InSamp] This matrix contains sample numbers for a difference of voiced samples that are less than the mean of the RMS values. According to D.A.V.I.D, this samples are recorded as attack  
	 	# Since we will be applying inflection on new utterance, This will help for classifications amongst voiced samples.      
	 	else:  
	  		cnt1 +=1
		

	#---"Iblocks" is the consecutive blocks for inflection----#
	Iblocks =[]
	for i in range(0 , len(InSamp)-1):
		Iblocks.append(InSamp[i] + np.arange(Conblocks))
	Iblocks = np.array(Iblocks)		 
	

	#--------------------------------Alteration of Discrete Data for Inflection--------------------------------------------# 
	# 'IblocksSelected' are the selected blocks that are used for inflection.
	# They are selected by comparing the first element of the Iblock.
	# 'IblocksSelected' are blocks selected in such a way that overlappig/consecutive blocks are not used during inflection.
	# It contains 21 consecutive blocks.
	IblocksSelected = []
	for i in range(len(InSamp)-1):
		if (np.abs(Iblocks[i][0] - Iblocks[i-1][0]))> 2*(Conblocks-1):
			IblocksSelected.append(Iblocks[i])
	IblocksSelected = np.array(IblocksSelected)
	
	# n are the consecutive blocks within the 'IblocksSelected' 
	# Are blocks that can be  altered with Pitch Up followed by Pitch Down then resolve to normal.
	n = (Conblocks/(Conblocks/3)) * len(IblocksSelected)
	

	# IBS is the reshaped Inflection Blocks for the purpose of categorizing blocks for Inflection 
	# Based on 'n' The IBS is used for the classification of:  

	
	IBS = (np.reshape(IblocksSelected,(n,Conblocks/3))).flatten()

	
	

	A = np.array(np.arange(num_blocks))
	B = np.array(IBS.flatten())
	DiffArrays = np.array(list(set(A)-set(B)))
	

	
	if typeOfEmotion=="Happy":

		
		fs,x = wavfile.read(filename)
		Chunk_Size = 1024
		num_blocks = int(np.ceil(len(x)/Chunk_Size)) 

		
		# Blocks of Data by Windowing Through Chunk Size
		X = voi.Data_Blocks(x,Chunk_Size)
		# Fundamental Frequency 
		
		f0 = alysis.pitch_detect(x,fs,Chunk_Size)
		# Starting Info of Voiced/Unvoiced Regions

		vSig = voi.startinginfo(x,f0,fs,Chunk_Size)
		# Voiced Regions 
		
		Voiced_Regions = voi.Voiced_regions(x,f0,vSig,Chunk_Size)
		#-----Unvoiced Regions-----#
		#UnVoiced_Regions = voi.UnVoiced_regions(x,f0,vSig,Chunk_Size)

	
		#---This is a computation for the RMS values, these will help in identifying which blocks are used for inflection----#
		RMS = np.asarray(alysis.root_mean_square(x,Chunk_Size,fs)[0])
		

		# Inflection Voice Samples(IVS) is a matrix containing potential sample points for inflection. 		
		IVS = np.array(vSig['VSamp'])
		

		# Pitches/Fundamental Frequency of Potetnial Inflection samples [Freqin]
		Freqin = np.array(f0[IVS])
		


		# Execution Time/Duration of a Single Block 
		Ts = 1/float(fs) * Chunk_Size
		# Consecutive Blocks during the Inflection Duration
					#	1Block = Ts
		 			#	?Block = Inflect_Duration

		
		Conblocks = 1 + int(0.5 / Ts)
		#----Matrix of Sample Numbers----#  
		cnt = 0
		cnt1 = 0
		InSamp = []
		for i in range(0,len(IVS)-1):
		  	if RMS[i] <= np.nanmean(RMS):
		 		InSamp.append(IVS[i])
		 		cnt += 1
		 	# [InSamp] This matrix contains sample numbers for a difference of voiced samples that are less than the mean of the RMS values. According to D.A.V.I.D, this samples are recorded as attack  
		 	# Since we will be applying inflection on new utterance, This will help for classifications amongst voiced samples.      
		 	else:  
		  		cnt1 +=1
			

		#---"Iblocks" is the consecutive blocks for inflection----#
		Iblocks =[]
		for i in range(0 , len(InSamp)-1):
			Iblocks.append(InSamp[i] + np.arange(Conblocks))
		Iblocks = np.array(Iblocks)		 
		

		#--------------------------------Alteration of Discrete Data for Inflection--------------------------------------------# 
		# 'IblocksSelected' are the selected blocks that are used for inflection.
		# They are selected by comparing the first element of the Iblock.
		# 'IblocksSelected' are blocks selected in such a way that overlappig/consecutive blocks are not used during inflection.
		# It contains 21 consecutive blocks.
		IblocksSelected = []
		for i in range(len(InSamp)-1):
			if (np.abs(Iblocks[i][0] - Iblocks[i-1][0]))> 2*(Conblocks-1):
				IblocksSelected.append(Iblocks[i])
		IblocksSelected = np.array(IblocksSelected)
		
		# n are the consecutive blocks within the 'IblocksSelected' 
		# Are blocks that can be  altered with Pitch Up followed by Pitch Down then resolve to normal.
		n = (Conblocks/(Conblocks/3)) * len(IblocksSelected)
		

		# IBS is the reshaped Inflection Blocks for the purpose of categorizing blocks for Inflection 
		# Based on 'n' The IBS is used for the classification of:  
																# IU-Inflecion Up 
																# ID - Inflection Down 
																# N -Normal
		
		IBS = (np.reshape(IblocksSelected,(n,Conblocks/3))).flatten()
	
		
		

		A = np.array(np.arange(num_blocks))
		B = np.array(IBS.flatten())
		DiffArrays = np.array(list(set(A)-set(B)))
		

		
		# --------------------Happy Preset-------------------------------------#
		timestamps = (np.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
		Utterance_time_stamps = timestamps[IblocksSelected]
		Qfactor = 1
		Gain = 3.0
		Semitones = 0.5
		hp.HappyPatch(fs,Semitones,Qfactor,Gain,Utterance_time_stamps)

		
	if typeOfEmotion=="HappyTensed":	
	
	
		fs,x = wavfile.read(filename)
		Chunk_Size = 1024
		num_blocks = int(np.ceil(len(x)/Chunk_Size)) 

		
		# Blocks of Data by Windowing Through Chunk Size
		X = voi.Data_Blocks(x,Chunk_Size)
		# Fundamental Frequency 
		
		f0 = alysis.pitch_detect(x,fs,Chunk_Size)
		# Starting Info of Voiced/Unvoiced Regions

		vSig = voi.startinginfo(x,f0,fs,Chunk_Size)
		# Voiced Regions 
		
		Voiced_Regions = voi.Voiced_regions(x,f0,vSig,Chunk_Size)
		#-----Unvoiced Regions-----#
		#UnVoiced_Regions = voi.UnVoiced_regions(x,f0,vSig,Chunk_Size)

	
		#---This is a computation for the RMS values, these will help in identifying which blocks are used for inflection----#
		RMS = np.asarray(alysis.root_mean_square(x,Chunk_Size,fs)[0])
		

		# Inflection Voice Samples(IVS) is a matrix containing potential sample points for inflection. 		
		IVS = np.array(vSig['VSamp'])

		# Pitches/Fundamental Frequency of Potetnial Inflection samples [Freqin]
		Freqin = np.array(f0[IVS])
		


		# Execution Time/Duration of a Single Block 
		Ts = 1/float(fs) * Chunk_Size
		# Consecutive Blocks during the Inflection Duration
					#	1Block = Ts
		 			#	?Block = Inflect_Duration

		
		Conblocks = int(0.5 / Ts)
		
		#----Matrix of Sample Numbers----#  
		cnt = 0
		cnt1 = 0
		InSamp = []
		for i in range(0,len(IVS)-1):
		  	if RMS[i] <= np.nanmean(RMS):
		 		InSamp.append(IVS[i])
		 		cnt += 1
		 	# [InSamp] This matrix contains sample numbers for a difference of voiced samples that are less than the mean of the RMS values. According to D.A.V.I.D, this samples are recorded as attack  
		 	# Since we will be applying inflection on new utterance, This will help for classifications amongst voiced samples.      
		 	else:  
		  		cnt1 +=1
			

		#---"Iblocks" is the consecutive blocks for inflection----#
		Iblocks =[]
		for i in range(0 , len(InSamp)-1):
			Iblocks.append(InSamp[i] + np.arange(Conblocks))
		Iblocks = np.array(Iblocks)		 
		

		#--------------------------------Alteration of Discrete Data for Inflection--------------------------------------------# 
		# 'IblocksSelected' are the selected blocks that are used for inflection.
		# They are selected by comparing the first element of the Iblock.
		# 'IblocksSelected' are blocks selected in such a way that overlappig/consecutive blocks are not used during inflection.
		# It contains 21 consecutive blocks.
		IblocksSelected = []
		for i in range(len(InSamp)-1):
			if (np.abs(Iblocks[i][0] - Iblocks[i-1][0]))> 2*(Conblocks-1):
				IblocksSelected.append(Iblocks[i])
		IblocksSelected = np.array(IblocksSelected)
		
		# n are the consecutive blocks within the 'IblocksSelected' 
		# Are blocks that can be  altered with Pitch Up followed by Pitch Down then resolve to normal.
		n = (Conblocks/(Conblocks/3)) * len(IblocksSelected)
		

		# IBS is the reshaped Inflection Blocks for the purpose of categorizing blocks for Inflection 
		# Based on 'n' The IBS is used for the classification of:  
																# IU-Inflecion Up 
																# ID - Inflection Down 
																# N -Normal
		
		IBS = (np.reshape(IblocksSelected,(n,Conblocks/3))).flatten()
		
		
		

		A = np.array(np.arange(num_blocks))
		B = np.array(IBS.flatten())
		DiffArrays = np.array(list(set(A)-set(B)))
		
		
		
		# --------------------Happy Tensed Preset-------------------------------------#
		timestamps = (np.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
		Utterance_time_stamps = timestamps[IblocksSelected]
		Qfactor = 1
		Gain = 3.0
		Semitones = 1.0
		hp.HappyTensedPatch(fs,Semitones,Qfactor,Gain,Utterance_time_stamps)
	
	if typeOfEmotion=="Sad":	
		Qfactor = 1
		Gain = 0.25
		Semitones = -0.5
		hp.SadPatch(fs,Semitones,Qfactor,Gain)
	if typeOfEmotion=="Afraid":
		
		speed = 8.5
		depth = 30
		timestamps = (np.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
		Utterance_time_stamps = timestamps[IblocksSelected]
		
		hp.AfraidPatch(fs,speed,depth,Utterance_time_stamps)

if __name__ == '__main__':
	filename = "/home/dereje/Desktop/TestFolder/Test.wav"
	fs,x = wavfile.read(filename)
	EmotiveSpeech(fs,filename,"Happy")
	EmotiveSpeech(fs,filename,"HappyTensed")
	EmotiveSpeech(fs,filename,"Sad")
	EmotiveSpeech(fs,filename,"Afraid")
