import numpy as np
import preprocess as prep
import warnings
warnings.filterwarnings('ignore')
import batchprocess as bp
CHUNK_SIZE = 1024


def emotive_speech(x,fs,typeOfEmotion):
	TIME_STAMPS = bp.process_variables(x,fs,CHUNK_SIZE)[0]
	CONSECUTIVE_BLOCKS = bp.process_variables(x,fs,CHUNK_SIZE)[1]

	fundamental_frequency_in_blocks = bp.batch_analysis(x,fs,CHUNK_SIZE)[0]
	voiced_samples = bp.batch_analysis(x,fs,CHUNK_SIZE)[1]
	rms = bp.batch_analysis(x,fs,CHUNK_SIZE)[2]

	selected_inflect_block_new = bp.batch_preprocess(fundamental_frequency_in_blocks,voiced_samples,rms)
	
	output = bp.batch_synthesis(fs,CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block_new,typeOfEmotion)
	
if __name__ == '__main__':
	filename = "/home/dereje/Desktop/TestFolder/Test.wav"
	fs,x = prep.wave_file_read(filename)
	emotive_speech(x,fs,"Happy")
	emotive_speech(x,fs,"HappyTensed")
	emotive_speech(x,fs,"Sad")
	emotive_speech(x,fs,"Afraid")
