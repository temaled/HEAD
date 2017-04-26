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
if __name__ == '__main__':
	filename = "/home/dereje/Desktop/SoundFolder/Test.wav" 
	fs,x = wavfile.read(filename)
	Chunk_Size = 1024
	Spectral_Analysis = stft(x,Chunk_Size)
	rmsx = root_mean_square(x,Chunk_Size,fs)
	