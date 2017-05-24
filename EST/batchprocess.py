import numpy as np
import analysis as alysis
import preprocess as prep
import synthesis as synth

def process_variables(x,fs,CHUNK_SIZE):
	NUM_BLOCKS = int(np.ceil(len(x)/CHUNK_SIZE))
	SAMPLE_PERIOD = 1/float(fs) * CHUNK_SIZE
	
	TIME_STAMPS = (np.arange(0,NUM_BLOCKS -1)* (CHUNK_SIZE/float(fs)))
	CONSECUTIVE_BLOCKS = 1 + int(0.5 / SAMPLE_PERIOD)
	return TIME_STAMPS,CONSECUTIVE_BLOCKS
def batch_analysis(x,fs,CHUNK_SIZE):
	fundamental_frequency_in_blocks = alysis.pitch_detect(x,fs,CHUNK_SIZE)
	rms = alysis.root_mean_square(x,CHUNK_SIZE,fs)
	voiced_unvoiced_starting_info_object = alysis.starting_info(x,fundamental_frequency_in_blocks,fs,CHUNK_SIZE)
	voiced_samples = voiced_unvoiced_starting_info_object['VSamp']
	return fundamental_frequency_in_blocks,voiced_samples,rms
def batch_preprocess(fundamental_frequency_in_blocks,voiced_samples,rms):
	voice_sample_begin = prep.utterance_region_begin_samples(voiced_samples)
  	voice_chunk_sample = prep.utterance_chunk(voiced_samples,voice_sample_begin[1])
	inflection_voice_samples = prep.pre_process(voice_chunk_sample)
	frequency_of_voiced_samples = fundamental_frequency_in_blocks[voiced_samples]
	#frequency_for_inflection = prep.potential_inflection_fundamental_frequency(frequency_of_voiced_samples)
	inflection_sample_numbers = prep.matrix_of_sample_numbers(rms[voice_sample_begin[0]],inflection_voice_samples)
	selected_inflect_block_new = prep.selected_inflect_block_new(inflection_sample_numbers)
	return selected_inflect_block_new
def batch_synthesis(fs,CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block_new,typeOfEmotion):
	
	if typeOfEmotion == "Happy":
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = synth.appended_utterance_time_stamps(CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block)
		output = synth.happy_patch(fs,utterance_time_stamps)	
	
	if typeOfEmotion == "HappyTensed":	
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = synth.appended_utterance_time_stamps(CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block)
		output = synth.happy_tensed_patch(fs,utterance_time_stamps)

	if typeOfEmotion == "Sad":	
		output = synth.sad_patch(fs)
	
	if typeOfEmotion == "Afraid":
		selected_inflect_block = selected_inflect_block_new
		utterance_time_stamps = synth.appended_utterance_time_stamps(CONSECUTIVE_BLOCKS,TIME_STAMPS,selected_inflect_block)
		output = synth.afraid_patch(fs,utterance_time_stamps)
	return output