import numpy as np
import analysis as alysis
import preprocess as prep
import synthesis as synth
import warnings
warnings.filterwarnings('ignore')
<<<<<<< HEAD

CHUNK_SIZE = 1024
QFACTOR = 1
def emotive_speech(x,fs,typeOfEmotion):
	
	NUM_BLOCKS = int(np.ceil(len(x)/CHUNK_SIZE))
	SAMPLE_PERIOD = 1/float(fs) * CHUNK_SIZE
	TIME_STAMPS = (np.arange(0,NUM_BLOCKS -1)* (CHUNK_SIZE/float(fs)))
	
=======
def emotive_speech(x,fs,typeOfEmotion):
	CHUNK_SIZE = 1024
	NUM_BLOCKS = int(np.ceil(len(x)/CHUNK_SIZE))
	SAMPLE_PERIOD = 1/float(fs) * CHUNK_SIZE
	TIME_STAMPS = (np.arange(0,NUM_BLOCKS -1)* (CHUNK_SIZE/float(fs)))
	QFACTOR = 1
>>>>>>> 63daf31b5496f36dc18b5b729d508be832b3dd19
	#---------------------Analysis---------------------------------------#
	data_in_blocks = alysis.data_blocks(x,CHUNK_SIZE)
	fundamental_frequency_in_blocks = alysis.pitch_detect(x,fs,CHUNK_SIZE)
	voiced_unvoiced_starting_info_object = alysis.starting_info(x,fundamental_frequency_in_blocks,fs,CHUNK_SIZE)
	voiced_samples = voiced_unvoiced_starting_info_object['VSamp']
	voiced_regions = alysis.voiced_regions(x,fundamental_frequency_in_blocks,voiced_unvoiced_starting_info_object,CHUNK_SIZE)
	consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)


	#---------------------preprocess-------------------------------------#
	inflection_voice_samples = prep.pre_process(voiced_samples)
	frequency_of_voiced_samples = fundamental_frequency_in_blocks[inflection_voice_samples]
	rms = prep.root_mean_square(x,CHUNK_SIZE,fs)[0]
	frequency_for_inflection = prep.potential_inflection_fundamental_frequency(frequency_of_voiced_samples)
	inflection_sample_numbers = prep.matrix_of_sample_numbers(rms,inflection_voice_samples)
<<<<<<< HEAD
	inflect_blocks = prep.consecutive_blocks_for_inflection(inflection_sample_numbers,consecutive_blocks)	
=======
	inflect_blocks = prep.consecutive_blocks_for_inflection(inflection_sample_numbers,consecutive_blocks)
>>>>>>> 63daf31b5496f36dc18b5b729d508be832b3dd19
	selected_inflect_block = prep.alteration_of_discrete_data(inflection_sample_numbers,consecutive_blocks,inflect_blocks)
	n = prep.consecutive_blocks_in_selected_blocks(selected_inflect_block,consecutive_blocks)
	reshaped_inflect_blocks = prep.reshaped_inflection_blocks(n,selected_inflect_block,consecutive_blocks)
	differece_arrays = prep.difference_arrays(NUM_BLOCKS,reshaped_inflect_blocks)
<<<<<<< HEAD
	print n
=======
	
>>>>>>> 63daf31b5496f36dc18b5b729d508be832b3dd19
	#----------------------synthesis-------------------------------------#
	
	if typeOfEmotion == "Happy":
		consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)
		selected_inflect_block = prep.alteration_of_discrete_data(inflection_sample_numbers,consecutive_blocks,inflect_blocks)	
		utterance_time_stamps = TIME_STAMPS[selected_inflect_block]

		gain = 3.0
		semitones = 0.5
		synth.happy_patch(fs,semitones,QFACTOR,gain,utterance_time_stamps)	
	
	if typeOfEmotion == "HappyTensed":	
<<<<<<< HEAD
		consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)
=======
		consecutive_blocks = int(0.5 / SAMPLE_PERIOD)
>>>>>>> 63daf31b5496f36dc18b5b729d508be832b3dd19
		inflection_sample_numbers = prep.matrix_of_sample_numbers(rms,inflection_voice_samples)
		inflect_blocks = prep.consecutive_blocks_for_inflection(inflection_sample_numbers,consecutive_blocks)
		selected_inflect_block = prep.alteration_of_discrete_data(inflection_sample_numbers,consecutive_blocks,inflect_blocks)
		utterance_time_stamps = TIME_STAMPS[selected_inflect_block]
		
		gain = 3.0
		semitones = 1.0
		synth.happy_tensed_patch(fs,semitones,QFACTOR,gain,utterance_time_stamps)
	
	if typeOfEmotion == "Sad":	
		gain = 0.25
		semitones = -0.5
		synth.sad_patch(fs,semitones,QFACTOR,gain)
	
	if typeOfEmotion == "Afraid":
		speed = 8.5
<<<<<<< HEAD
		depth = 60
		utterance_time_stamps = TIME_STAMPS[selected_inflect_block]
		synth.afraid_patch(fs,speed,depth,utterance_time_stamps)

=======
		depth = 50
		utterance_time_stamps = TIME_STAMPS[selected_inflect_block]
		synth.afraid_patch(fs,speed,depth,utterance_time_stamps)
>>>>>>> 63daf31b5496f36dc18b5b729d508be832b3dd19
if __name__ == '__main__':
	filename = "/home/dereje/Desktop/TestFolder/Test.wav"
	fs,x = prep.wave_file_read(filename)
	emotive_speech(x,fs,"Happy")
	emotive_speech(x,fs,"HappyTensed")
	emotive_speech(x,fs,"Sad")
	emotive_speech(x,fs,"Afraid")
