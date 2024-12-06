import os
import sys
import re

import pandas as pd

def string_to_dict(string, item_delimiter=',', pair_delimiter=None):
	if pair_delimiter is not None:
		string_dict = {item.split(pair_delimiter)[0]:item.split(pair_delimiter)[1] for item in string.split(item_delimiter) if len(item.split(pair_delimiter)) > 1}
	else:
		string_dict = {item.split()[0]:item.split()[1] for item in string.split(item_delimiter) if len(item.split()) > 1}
		
	return string_dict

def savefile_with_readme(args, stack, path_file, data_file_string):
	
	with open(path_file, 'w') as file:
		file.write(data_file_string)
	
	dirname = os.path.dirname(path_file)
	path_readme = os.path.join(dirname, 'README.txt')
	
	path_script = stack[0][1]
	
	text_stack = ['line: ' + str(trace[2]) + ', ' + str(trace[4][0]) for i, trace in enumerate(stack) if i > 0]
	text_stack.reverse()
	
	text_readme = '\n'.join(['Datafiles generated with: ' + path_script, 'Input arguments: ' + str(args), 'Stack:\n']) + ''.join(text_stack)
	
	with open(path_readme, 'w') as file:
		file.write(text_readme)

def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	'''
	alist.sort(key=natural_keys) sorts in human order
	http://nedbatchelder.com/blog/200712/human_sorting.html
	(See Toothy's implementation in the comments)
	'''
	return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def bam_file(filename):
	ext = [".bam", ".sam"]
	return filename.endswith(tuple(ext))

def bed_file(filename):
	ext = [".bed"]
	return filename.endswith(tuple(ext))
	
def output_memmap_file(filename):
	ext = [".output.memmap"]
	return filename.endswith(tuple(ext))

def bigwig_file(filename):
	ext = [".bigWig", ".bigwig", ".bw"]
	return filename.endswith(tuple(ext))
	
def scale_num(new_max, new_min, old_max, old_min, val):
	return (new_max - new_min) * (val - old_min) / (old_max - old_min) + new_min
			
def binary_boundary_search(region_boundaries, low, high, insert_midpoint):

	if high > low:

		mid = (high + low) // 2

		if insert_midpoint >= region_boundaries[mid][0] and insert_midpoint <= region_boundaries[mid][1]:
			return mid
		elif insert_midpoint > region_boundaries[mid][1]:
			return binary_boundary_search(region_boundaries, mid + 1, high, insert_midpoint)
		else:
			return binary_boundary_search(region_boundaries, low, mid - 1, insert_midpoint)

	else:

		return -1

def create_dict_entry(input_dict, keys, entry, overwrite=True):
	
	# need an example here lol
	
	key_to_check = keys.pop(0)
	
	if len(keys) == 0:
		if key_to_check not in input_dict or overwrite:
			input_dict[key_to_check] = entry
	else:
		if key_to_check not in input_dict:
			input_dict[key_to_check] = {}
		input_dict[key_to_check] = create_dict_entry(input_dict[key_to_check], keys, entry, overwrite=overwrite)
	
	return input_dict
