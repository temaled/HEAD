from scipy.io import wavfile
from scipy import signal
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import Voiced_Unvoiced as voi
import peakdetect as pd
def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]
def stft(x,Chunk_Size,overlap=1):
	import scipy
	hop = Chunk_Size / overlap
	w = scipy.hanning(Chunk_Size+1)[:-1]
	cnt = 0
	return np.array([np.fft.rfft(w*x[i:i+Chunk_Size]) for i in range (0,len(x)-Chunk_Size,hop)])
def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """
    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( int(len(sound_array)/f) + window_size)
    for i in np.arange(0, len(sound_array)-(window_size+h), int(h*f)):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h:i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        # add to result
        i2 = int(i/f) 
        result[i2 : i2 + window_size] += (hanning_window*a2_rephased).astype(np.float32)
    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)
    return result.astype('int16')
def pitchshift(snd_array, n, window_size=1024, h=256):
    """n is in semitones"""
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    new_snd =  speedx(stretched[window_size:], factor)
    return np.array(new_snd)
def Happy_Inflection(DownPitchArray,UpPitchArray,NormalPitchArray):
    """1Semitones=100Cents"""
    IU = 1.084227
    #IU = 140/100
    #ID = float(-200)/100
    ID = 0.890899
    DPA = pitchshift(DownPitchArray,ID,1024,256)
    UPA = pitchshift(UpPitchArray,IU,1024,256)
    NPA = NormalPitchArray.flatten()

    InflectArray = []
    InflectArray.extend(DPA)
    InflectArray.extend(UPA)
    InflectArray.extend(NPA)
    return InflectArray 
if __name__ == '__main__':
	
    fs,x = wavfile.read('/home/dereje/Desktop/SoundFolder/Test.wav')
    Chunk_Size = 1024
