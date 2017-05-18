import numpy as np
import analysis as alysis
import preprocess as prep
import synthesis as synth
import warnings
warnings.filterwarnings('ignore')

CHUNK_SIZE = 1024
QFACTOR = 1
PARAMETER_CONTROL = 1
def emotive_speech(x,fs,typeOfEmotion):
	
	NUM_BLOCKS = int(np.ceil(len(x)/CHUNK_SIZE))
	SAMPLE_PERIOD = 1/float(fs) * CHUNK_SIZE
	TIME_STAMPS = (np.arange(0,NUM_BLOCKS -1)* (CHUNK_SIZE/float(fs)))
	
	#---------------------Analysis---------------------------------------#
	data_in_blocks = alysis.data_blocks(x,CHUNK_SIZE)
	fundamental_frequency_in_blocks = alysis.pitch_detect(x,fs,CHUNK_SIZE)
	voiced_unvoiced_starting_info_object = alysis.starting_info(x,fundamental_frequency_in_blocks,fs,CHUNK_SIZE)
	voiced_samples = voiced_unvoiced_starting_info_object['VSamp']
	voiced_regions = alysis.voiced_regions(x,fundamental_frequency_in_blocks,voiced_unvoiced_starting_info_object,CHUNK_SIZE)
	consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)


	#---------------------preprocess-------------------------------------#
	voice_sample_begin = prep.utterance_region_begin_samples(voiced_samples)
  	voice_chunk_sample = prep.utterance_chunk(voiced_samples,voice_sample_begin[1])
	inflection_voice_samples = prep.pre_process(voice_chunk_sample)
	frequency_of_voiced_samples = fundamental_frequency_in_blocks[voiced_samples]
	rms = prep.root_mean_square(x,CHUNK_SIZE,fs)
	frequency_for_inflection = prep.potential_inflection_fundamental_frequency(frequency_of_voiced_samples)
	inflection_sample_numbers = prep.matrix_of_sample_numbers(rms[voice_sample_begin[0]],inflection_voice_samples)
	#inflection_sample_numbers = np.asarray(inflection_sample_numbers)
	
	#inflect_blocks = prep.consecutive_blocks_for_inflection(inflection_sample_numbers,consecutive_blocks)	
	

	selected_inflect_block = inflection_sample_numbers
	selected_inflect_block_new = []
	for i in range (len(selected_inflect_block)-1):
		if len(selected_inflect_block[i]) >= 4:
			selected_inflect_block_new.append(selected_inflect_block[i])
	
	
	
	
	#selected_inflect_block = prep.alteration_of_discrete_data(inflection_sample_numbers,consecutive_blocks,inflect_blocks)
	# n = prep.consecutive_blocks_in_selected_blocks(selected_inflect_block,consecutive_blocks)
	# reshaped_inflect_blocks = prep.reshaped_inflection_blocks(n,selected_inflect_block,consecutive_blocks)
	# differece_arrays = prep.difference_arrays(NUM_BLOCKS,reshaped_inflect_blocks)
	
	#----------------------synthesis-------------------------------------#
	
	if typeOfEmotion == "Happy":
		consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)
		
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = []
		for i in range(len(selected_inflect_block)):
			utterance_time_stamps.append(TIME_STAMPS[selected_inflect_block[i][:consecutive_blocks]])
		
		utterance_time_stamps = np.asarray(utterance_time_stamps)
		
		gain = 3.0
		semitones = 1.5 * PARAMETER_CONTROL
		synth.happy_patch(fs,semitones,QFACTOR,gain,utterance_time_stamps)	
	
	if typeOfEmotion == "HappyTensed":	
		consecutive_blocks = 1 + int(0.5 / SAMPLE_PERIOD)
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = []
		for i in range(len(selected_inflect_block)):
			utterance_time_stamps.append(TIME_STAMPS[selected_inflect_block[i][:consecutive_blocks]])

		utterance_time_stamps = np.asarray(utterance_time_stamps)
		gain = 3.0
		semitones = 2.0 * PARAMETER_CONTROL
		synth.happy_tensed_patch(fs,semitones,QFACTOR,gain,utterance_time_stamps)
	
	if typeOfEmotion == "Sad":	
		gain = 0.25
		semitones = -1.5 * PARAMETER_CONTROL
		synth.sad_patch(fs,semitones,QFACTOR,gain)
	
	if typeOfEmotion == "Afraid":
		speed = 8.5
		depth = 1 + (60 * PARAMETER_CONTROL)
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = []
		for i in range(len(selected_inflect_block)):
			utterance_time_stamps.append(TIME_STAMPS[selected_inflect_block[i][:consecutive_blocks]])

		synth.afraid_patch(fs,speed,depth,utterance_time_stamps)

if __name__ == '__main__':
	filename = "/home/dereje/Desktop/TestFolder/Test.wav"
	fs,x = prep.wave_file_read(filename)
	emotive_speech(x,fs,"Happy")
	emotive_speech(x,fs,"HappyTensed")
	emotive_speech(x,fs,"Sad")
	emotive_speech(x,fs,"Afraid")
