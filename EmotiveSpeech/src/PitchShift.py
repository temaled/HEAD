from sox.transform import Transformer
import matplotlib.pyplot as plt
from scipy.io import wavfile
import Voiced_Unvoiced as voi 

def Happy_pitchshift(n_semitones):
	PitchShift = Transformer()
	PitchShift.pitch(n_semitones,False)
	filenameIn = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestHappyPitch.wav"
	PitchShift.build(filenameIn,filenameout)
	fs,pitch_shifted_array = wavfile.read(filenameout)
	return pitch_shifted_array,filenameout
def Sad_pitchshift(n_semitones):
	PitchShift = Transformer()
	PitchShift.pitch(n_semitones,False)
	filenameIn = "/home/dereje/Desktop/TestFolder/Test.wav"
	filenameout = "/home/dereje/Desktop/TestFolder/TestSadPitch.wav"
	PitchShift.build(filenameIn,filenameout)
	fs,pitch_shifted_array = wavfile.read(filenameout)
	return pitch_shifted_array
