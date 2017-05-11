import scipy
from scipy.io import wavfile 
from scipy.fftpack import rfft,irfft,fftfreq
import numpy  
import pysptk
import warnings
warnings.filterwarnings('ignore')
import Preprocess as PreP
def data_blocks(x,Chunk_Size):
	num_blocks = int(numpy.ceil(len(x)/Chunk_Size))		
	X = numpy.resize(x,(num_blocks,Chunk_Size))
	X = numpy.array(X)
	# Blocks of Data by Windowing Through Chunk Size
	return X
def pitch_detect(sndarray,fs, chunk_size):
    new_sndarray = numpy.asarray(numpy.float64(sndarray))
    f0 = pysptk.swipe(numpy.asarray(new_sndarray), fs, chunk_size, 65,500,0.001,1) 
    # Fundamental Frequency 
    return f0
def zero_crossing_rate_blocks(wavedata,Chunk_Size,fs):
	num_blocks = int(numpy.ceil(len(wavedata)/Chunk_Size))
	time_stamps = (numpy.arange(0,num_blocks -1)* (Chunk_Size/float(fs)))
	zero_crossing_rate = []
	for i in range (0,num_blocks -1):
		start = i * Chunk_Size
		stop = numpy.min([(start + Chunk_Size - 1),len(wavedata)])
		zero_crossing = 0.5 * numpy.mean(numpy.abs(numpy.diff(numpy.sign(wavedata[start:stop]))))
		zero_crossing_rate.append(zero_crossing)
	
	zero_crossing_rate_obj = {"zero_crossing_rate_TS":zero_crossing_rate,"TS":time_stamps}
	return zero_crossing_rate_obj
	
def spectral_centroid(wavedata,Chunk_Size,fs):
	magnitude_spectrum = PreP.stft(x,Chunk_Size)
	timebins , freqbins = numpy.shape(magnitude_spectrum)
	time_stamps = (numpy.arange(0,timebins - 1 )*(timebins / float(fs)))

	spectral_centroid = []
	for t in range (timebins - 1):
		power_spectrum = numpy. abs (magnitude_spectrum[t])**2
		sc_t = numpy.sum(power_spectrum * numpy.arange(1,freqbins+1)) / numpy.sum(power_spectrum)
		spectral_centroid.append(sc_t)
	spectral_centroid = numpy.asarray(spectral_centroid)
	spectral_centroid = numpy.nan_to_num(spectral_centroid)
	return spectral_centroid, numpy.asarray(time_stamps)
def unvoiced_starting_pts(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size):
    #register unvoiced signal starting points
	fs = 44100
	zero_crossing_rate_array = zero_crossing_rate_blocks(x, Chunk_Size,fs)
	for i in range (0,len(zero_crossing_rate_array ["zero_crossing_rate_TS"])):
		if zero_crossing_rate_array["zero_crossing_rate_TS"][i] >= numpy.mean(zero_crossing_rate_array ["zero_crossing_rate_TS"]):
			voiced_unvoiced_starting_info_object["unvoicedStart"].append (zero_crossing_rate_array["TS"][i])
			voiced_unvoiced_starting_info_object["USamp"].append(i)
def voiced_starting_pts(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size):
    #register voiced signal starting points
    fs = 44100
    zero_crossing_rate_array = zero_crossing_rate_blocks(x, Chunk_Size,fs)
    for i in range (0,len(zero_crossing_rate_array ["zero_crossing_rate_TS"])):
		if zero_crossing_rate_array["zero_crossing_rate_TS"][i] <= numpy.mean(zero_crossing_rate_array ["zero_crossing_rate_TS"]):
			voiced_unvoiced_starting_info_object["voicedStart"].append(zero_crossing_rate_array["TS"][i])
			voiced_unvoiced_starting_info_object["VSamp"].append(i)
def voiced_regions(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size):
	X = data_blocks(x,Chunk_Size)
	voiced_regions = []
	for i in range(0,len(voiced_unvoiced_starting_info_object["voicedStart"])):
		voiced_regions.append(X[voiced_unvoiced_starting_info_object['VSamp'][i]])
	voiced_regions = numpy.abs(voiced_regions)
	# Voiced Regions 
	return voiced_regions
def unvoiced_regions(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size):
	X = data_blocks(x,Chunk_Size)
	unvoiced_regions = []
	for i in range(0,len(voiced_unvoiced_starting_info_object["unvoicedStart"])):
		unvoiced_regions.append(X[voiced_unvoiced_starting_info_object['USamp'][i]])
	unvoiced_regions = numpy.abs(unvoiced_regions)
	return unvoiced_regions
def starting_info(x,f0,fs,Chunk_Size):
	voiced_unvoiced_starting_info_object = {"unvoicedStart":[],"voicedStart":[],"USamp":[],"VSamp" :[]}
	unvoiced_starting_pts(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size)
	voiced_starting_pts(x,f0,voiced_unvoiced_starting_info_object,Chunk_Size)
	# Starting Info of Voiced/Unvoiced Regions
	return voiced_unvoiced_starting_info_object


	
	