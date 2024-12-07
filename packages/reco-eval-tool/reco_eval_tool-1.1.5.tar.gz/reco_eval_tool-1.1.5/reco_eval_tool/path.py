import os
import time

# default output directory is current directory + 'evaluation_output_' + timestamp
OUTPUT_DIR = os.path.join(os.getcwd(), 'evaluation_output_' + time.strftime("%Y%m%d%H%M%S"))

def set_output_dir(output_dir):
	"""
	Set the output directory for the evaluation tool
	:param output_dir: output directory
	"""
	global OUTPUT_DIR
	OUTPUT_DIR = output_dir
	print(f">>>> output directory is set to {OUTPUT_DIR}")

def get_output_dir():
	"""
	Get the output directory for the evaluation tool
	:return: output directory
	"""
	print(f">>>> output directory is {OUTPUT_DIR}")
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
	return OUTPUT_DIR

