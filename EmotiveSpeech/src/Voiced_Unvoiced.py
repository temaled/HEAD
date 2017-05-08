import sys
import numpy  
import scipy
import pysptk
import scipy
from scipy.io import wavfile 
import warnings
warnings.filterwarnings('ignore')
from scipy.fftpack import rfft,irfft,fftfreq
import Analysis as alysis
def Data_Blocks(x,Chunk_Size):
	num_blocks = int(numpy.ceil(len(x)/Chunk_Size))		
	#X = [[x[i*j] for i in range(0,Chunk_Size-1)] for j in range(1,num_blocks)] 
	X = numpy.resize(x,(num_blocks,Chunk_Size))
	X = numpy.array(X)
	return X
def pitchdetect(sndarray,fs,Chunk_Size):
	new_sndarray = []
	for i in sndarray:
		new_sndarray.append(numpy.float64(i))
	f0 = pysptk.sptk.swipe(numpy.asarray(new_sndarray),fs,Chunk_Size,60,500,0.001,1)
	return f0
def zero_crossing_rate_blocks(wavedata,Chunk_Size,fs):
	num_blocks = int(numpy.ceil(len(wavedata)/Chunk_Size))
	timestamps = (numpy.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
	zcr = []
	for i in range (0,num_blocks -1):
		start = i * Chunk_Size
		stop = numpy.min([(start + Chunk_Size - 1),len(wavedata)])
		zc = 0.5 * numpy.mean(numpy.abs(numpy.diff(numpy.sign(wavedata[start:stop]))))
		zcr.append(zc)
	
	zcr_obj = {"ZCR_TS":zcr,"TS":timestamps}
	#zcr_obj = zcr
	return zcr_obj
	#return numpy.asarray(zcr), numpy.asarray(timestamps)
def spectral_centroid(wavedata,Chunk_Size,fs):
	magnitude_spectrum = alysis.stft(x,Chunk_Size)
	timebins , freqbins = numpy.shape(magnitude_spectrum)
	timestamps = (numpy.arange(0,timebins - 1 )*(timebins / float(fs)))

	sc = []
	for t in range (timebins - 1):
		power_spectrum = numpy. abs (magnitude_spectrum[t])**2
		sc_t = numpy.sum(power_spectrum * numpy.arange(1,freqbins+1)) / numpy.sum(power_spectrum)
		sc.append(sc_t)

	sc = numpy.asarray(sc)
	sc = numpy.nan_to_num(sc)
	return sc, numpy.asarray(timestamps)
def unvoiced_starting_pts(x,f0,vSig,Chunk_Size):
    #register unvoiced signal starting points
	fs = 44100
	zcr_array = zero_crossing_rate_blocks(x, Chunk_Size,fs)
	for i in range (0,len(zcr_array ["ZCR_TS"])):
		if zcr_array["ZCR_TS"][i] >= numpy.mean(zcr_array ["ZCR_TS"]):
			vSig["unvoicedStart"].append (zcr_array["TS"][i])
			vSig["USamp"].append(i)
def voiced_starting_pts(x,f0,vSig,Chunk_Size):
    #register voiced signal starting points
    fs = 44100
    zcr_array = zero_crossing_rate_blocks(x, Chunk_Size,fs)
    for i in range (0,len(zcr_array ["ZCR_TS"])):
		if zcr_array["ZCR_TS"][i] <= numpy.mean(zcr_array ["ZCR_TS"]):
			vSig["voicedStart"].append(zcr_array["TS"][i])
			vSig["VSamp"].append(i)
def Voiced_regions(x,f0,vSig,Chunk_Size):
	X = Data_Blocks(x,Chunk_Size)
	Voiced_Regions = []
	for i in range(0,len(vSig["voicedStart"])):
		Voiced_Regions.append(X[vSig['VSamp'][i]])
	Voiced_Regions = numpy.abs(Voiced_Regions)
	return Voiced_Regions
def UnVoiced_regions(x,f0,vSig,Chunk_Size):
	X = Data_Blocks(x,Chunk_Size)
	UnVoiced_Regions = []
	for i in range(0,len(vSig["unvoicedStart"])):
		UnVoiced_Regions.append(X[vSig['USamp'][i]])
	UnVoiced_Regions = numpy.abs(UnVoiced_Regions)
	return UnVoiced_Regions
def startinginfo(x,f0,fs,Chunk_Size):
	vSig = {"unvoicedStart":[],"voicedStart":[],"USamp":[],"VSamp" :[]}
	unvoiced_starting_pts(x,f0,vSig,Chunk_Size)
	voiced_starting_pts(x,f0,vSig,Chunk_Size)
	return vSig
if __name__ == '__main__':
	filename ="/home/dere/Desktop/TestFolder/Test.wav"
	fs,x = wavfile.read(filename)
	Chunk_Size=1024
	
 	


	#rms_array = root_mean_square(x,Chunk_Size,fs)
	#sp_C_array = spectral_centroid(x,Chunk_Size,fs)
	

	