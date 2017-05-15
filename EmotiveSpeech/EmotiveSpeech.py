from __future__ import unicode_literals
from scipy.io import wavfile
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

def EmotiveSpeech(filename,typeOfEmotion):
	if typeOfEmotion=="Happy":
		sep= filename.split("/")
		rootName = ""
		for i in range(1,len(sep)-1):
			rootName= str(rootName) + "/" + str(sep[i])
		print "Root-Path: " + str(rootName)
		name = sep[len(sep)-1].split(".")[0]
		print "Filename:" + str(name)
		filenameHappy = str(rootName) + "/" + str(name) + "Happy.wav"
		filenameInflection = str(rootName) + "/" + str(name) + "InflectionHappy.wav"
		filenameInflectionDown = str(rootName) + "/" + str(name) + "InflectionHappyDown.wav"
		filenameInflectionUp = str(rootName) + "/" + str(name) + "InflectionHappyUp.wav"
		filenameWOUTInflection = str(rootName) + "/" + str(name) + "HappyWOUTInflection.wav"
		fs,x = wavfile.read(filename)
		Chunk_Size = 1024
		num_blocks = int(np.ceil(len(x)/Chunk_Size)) 
		
		#x = np.abs(x)
		


		
		# Blocks of Data by Windowing Through Chunk Size
		X = voi.Data_Blocks(x,Chunk_Size)
		# Fundamental Frequency 
		
		f0 = alysis.pitch_detect(x,fs,Chunk_Size)
		# Starting Info of Voiced/Unvoiced Regions

		vSig = voi.startinginfo(x,f0,fs,Chunk_Size)
		# Voiced Regions 
		
		Voiced_Regions = voi.Voiced_regions(x,f0,vSig,Chunk_Size)
		#-----Unvoiced Regions-----#
		# UnVoiced_Regions = voi.UnVoiced_regions(x,f0,vSig,Chunk_Size)

		
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
		#print f0[IBS]
		

		CriticalPoints = [0,-0.6,0.6,-0.4,0]
		Ypts = [-200,140,82.667,0,0]
		Xpts = [0,58.511,255.319,401.596,500]
		plt.plot(Xpts , InflectionPts)
		plt.show()   

		A = np.array(np.arange(num_blocks))
		B = np.array(IBS.flatten())
		DiffArrays = np.array(list(set(A)-set(B)))
		
		
		#WindowSize = int((Chunk_Size * 0.01)/Ts)
		#HopSize = WindowSize/4
		
		
		#---------------------Pitch Shift------------------------------------#
		# n= 1 + (+50Cents *1Semitone /100cents) = 1.5Semitones
		new_snd	= np.int16(pv.pitchshift(x,1,512,256))
		write(filenameInflection,fs,np.array(new_snd))
		# --------------------Inflection-------------------------------------#
		fs,xnew = wavfile.read(filenameInflection)
		Xa = voi.Data_Blocks(xnew,Chunk_Size)
		
		DownArrayIndex = IBS[np.arange(0,len(IBS),3)]
		DownArray = Xa[DownArrayIndex[0]]
	
		UpArrayIndex = (IBS[np.arange(1,len(IBS),3)])
		UpArray = Xa[UpArrayIndex[0]]
	
		NormArrayIndex = IBS[np.arange(2,len(IBS),3)]
		NormArray =Xa[NormArrayIndex[0]]
	

		xInflectDown = np.int16(pv.pitchshift(x,-2,512,256))
		write(filenameInflectionDown,fs,np.array(xInflectDown))
		fs,xnewID = wavfile.read(filenameInflectionDown)
		XaID = voi.Data_Blocks(xnewID,Chunk_Size)
		
		
		xInflectUp = np.int16(pv.pitchshift(x,1.4,512,256))
		write(filenameInflectionUp,fs,np.array(xInflectUp)) 
		fs,xnewIU = wavfile.read(filenameInflectionUp)
		XaIU = voi.Data_Blocks(xnewIU,Chunk_Size)


		xInflect = [] 
		xInflect.extend(XaID[DownArrayIndex[1]])
		xInflect.extend(XaIU[UpArrayIndex[1]])
		
		#-------------------ConcativeSynthesis------------------------------#
		xbefore =(Xa[:(DownArrayIndex[1])]).flatten()
		xafter = (Xa[(UpArrayIndex[1]+1):]).flatten()
		new_snd = []
		new_snd.extend(np.int16(xbefore))
		new_snd.extend(xInflect)
		new_snd.extend((np.int16(xafter).flatten()))

		write(filenameInflection,fs,np.array(new_snd))
		
		#--------------------Filter----------------------------------------#
		nyq = 0.5 * fs
		cutFreq = 1000/nyq
		order = 5
		b, a = butter(order,cutFreq , btype='highpass')
		snd_high_shelf = lfilter(b, a, new_snd)
		new_sndarray_high_shelf = np.array(np.int16(snd_high_shelf))
		write(filenameInflection,fs,np.array(new_sndarray_high_shelf))
		
		
		
if __name__ == '__main__':
	filename = "/home/dereje/Desktop/HarvardSentences/Test1.wav"
	fs,x = wavfile.read(filename)
	EmotiveSpeech(filename,"Happy")
