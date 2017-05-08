from scipy.io import wavfile
from sox.transform import Transformer
from scipy.signal import *
import Voiced_Unvoiced as voi
from matplotlib import pyplot as plt
from pysptk import swipe
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
def EmotiveSpeech(fs,filename,typeOfEmotion):
	if typeOfEmotion=="Happy":
		sep= filename.split("/")
		rootName = ""
		for i in range(1,len(sep)-1):
			rootName= str(rootName) + "/" + str(sep[i])
		print "Root-Path: " + str(rootName)
		name = sep[len(sep)-1].split(".")[0]
		print "Filename:" + str(name)
		filenameHappy = str(rootName) + "/" + str(name) + "Happy.wav"
		filenameInflection = str(rootName) + "/" + str(name) + "Inflection.wav"
		filenamePitchShift = str(rootName) + "/" + str(name) + "Test1PitchShiftUp.wav"
		
		
		#x = np.abs(x)
		#---------------------Pitch Shift------------------------------------#
		Semitones = 1.5
		pitch_Shifted_snd_array = ps.Happy_pitchshift(Semitones)
		
		fs,x = wavfile.read(pitch_Shifted_snd_array[1])
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
		

		
		# --------------------Inflection-------------------------------------#
		Voiced_Data_Regions = X[IBS]
		Voiced_Frequency_Regions = f0[IBS]

		

		inflected_snd_array = inflect.happy_Inflection_module(fs,Ts,x,Voiced_Data_Regions,Chunk_Size,Voiced_Frequency_Regions)
		inflected_snd_array_block = np.resize(inflected_snd_array,(len(IBS),Chunk_Size))
		wavfile.write(filenameInflection,fs,np.array(inflected_snd_array))
		
		#----------------------Concatinative Synthesis-----------------------#
		

		X[IBS] =  inflected_snd_array_block
		
		#----------------------Filter----------------------------------------#
		
		snd_array = X.flatten()
		filtered_snd_array = ft.Happy_Filter(fs,snd_array)
		wavfile.write(filenameHappy,fs,np.int16(filtered_snd_array))
		
	if typeOfEmotion=="HappyTensed":	
		sep= filename.split("/")
		rootName = ""
		for i in range(1,len(sep)-1):
			rootName= str(rootName) + "/" + str(sep[i])
		print "Root-Path: " + str(rootName)
		name = sep[len(sep)-1].split(".")[0]
		print "Filename:" + str(name)
		filenameHappyTensed = str(rootName) + "/" + str(name) + "HappyTensed.wav"
		filenameInflectionTensed = str(rootName) + "/" + str(name) + "InflectionTensed.wav"
		
		
		
		#x = np.abs(x)
		#---------------------Pitch Shift------------------------------------#
		Semitones = 2.0
		pitch_Shifted_snd_array = ps.Happy_pitchshift(Semitones)
		
		fs,x = wavfile.read(pitch_Shifted_snd_array[1])
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
		
		
		
		# --------------------Inflection-------------------------------------#
		Voiced_Data_Regions = X[IBS]
		Voiced_Frequency_Regions = f0[IBS]
		
		inflected_snd_array = inflect.happy_Tensed_Inflection_module(fs,Ts,x,Voiced_Data_Regions,Chunk_Size,Voiced_Frequency_Regions)
		
		inflected_snd_array_block = np.resize(inflected_snd_array,(len(IBS),Chunk_Size))
		
		wavfile.write(filenameInflectionTensed,fs,np.array(inflected_snd_array))
	
		#----------------------Concatinative Synthesis-----------------------#
		

		X[IBS] =  inflected_snd_array_block
		
		#----------------------Filter----------------------------------------#
		
		snd_array = X.flatten()
		filtered_snd_array = ft.Happy_Filter(fs,snd_array)
		wavfile.write(filenameHappyTensed,fs,np.int16(filtered_snd_array))

	if typeOfEmotion=="Sad":	
		sep= filename.split("/")
		rootName = ""
		for i in range(1,len(sep)-1):
			rootName= str(rootName) + "/" + str(sep[i])
		print "Root-Path: " + str(rootName)
		name = sep[len(sep)-1].split(".")[0]
		print "Filename:" + str(name)
		filenameSad = str(rootName) + "/" + str(name) + "Sad.wav"
		
		#---------------------Pitch Shift------------------------------------#
		Semitones = -0.5
		snd_array = ps.Sad_pitchshift(Semitones)
		
		#----------------------Filter----------------------------------------#
		filtered_snd_array = ft.Sad_Filter(fs,snd_array)
		wavfile.write(filenameSad,fs,np.int16(filtered_snd_array))


if __name__ == '__main__':
	filename = "/home/dereje/Desktop/TestFolder/Test.wav"
	fs,x = wavfile.read(filename)
	EmotiveSpeech(fs,filename,"Happy")
