import os, sys, re, argparse, random

import pandas as pd
import numpy as np
import pyranges as pr

from tqdm import tqdm

from joblib import Parallel, delayed, dump, load, parallel_backend

from collections import defaultdict

from .util import *

def get_df(path, category_field_num):

	if os.path.isdir(path):
	
		filenames = os.listdir(path)
		filenames = list(filter(bed_file, filenames))
		filenames.sort(key=natural_keys)
		
		filepaths = [os.path.join(path, filename) for filename in filenames]
		
		dfs = []
		
		for i, filepath in enumerate(filepaths):
			
			# Column names required for pyranges
			df = pd.read_csv(filepath, sep='\t', header=None, usecols=[0,1,2], names=['Chromosome', 'Start', 'End'])
			df[3] = filenames[i].replace('.bed', '')
			
			# ensure consistent naming convention
			df['Chromosome'] = [f'chr{i}' if 'chr' not in i else i for i in list(df['Chromosome'])]
			
			dfs.append(df)
			
		df_merged = pd.concat(dfs)
		
		return df_merged, 3
		
	else:
		
		if category_field_num is not None:
		
			df = pd.read_csv(path, sep='\t', header=None)
			
			# Column names required for pyranges
			df.rename(columns={0: 'Chromosome', 1:'Start', 2:'End'}, inplace=True)
			
			# ensure consistent naming convention
			df['Chromosome'] = [f'chr{i}' if 'chr' not in i else i for i in list(df['Chromosome'])]
			
			return df, int(category_field_num)
			
		else:
			
			print(f'Please provide a field number for identifying categories in {path}')
			sys.exit()

def create_slices(input_list, num_slices):
	"""
	Create slices of the input list into a specified number of slices.
	
	Args:
	input_list (list): The list to be sliced.
	num_slices (int): The number of slices to create.
	
	Returns:
	list: A list containing the slices.
	"""
	# Calculate the size of each slice
	slice_size = len(input_list) // num_slices
	remainder = len(input_list) % num_slices
	
	slices = []
	start = 0
	
	for i in range(num_slices):
		# Calculate the end index for the current slice
		end = start + slice_size + (1 if i < remainder else 0)
		# Append the current slice to the slices list
		slices.append(input_list[start:end])
		# Update the start index for the next slice
		start = end
	
	return slices

def calculate_distributions(df):
	"""
	Calculate the distributions of region lengths and distances between regions, separately for each chromosome.
	"""
	chrom_distributions = defaultdict(lambda: {'lengths': [], 'distances': []})
	
	for chrom in df['Chromosome'].unique():
		chrom_df = df[df['Chromosome'] == chrom].copy()
		chrom_df['distance'] = chrom_df['Start'].shift(-1) - chrom_df['End']
		
		chrom_distributions[chrom]['lengths'] = chrom_df['length'].values
		chrom_distributions[chrom]['distances'] = chrom_df['distance'].values
		
	return chrom_distributions

def generate_random_overlap_slice(slice, distributions_to_shuffle, df_static, chrom_sizes, mask_dict):
	"""
	Generate a random track with the given lengths and distances, avoiding mask regions.
	"""
	overlaps = []
	for i_slice in slice:
		
		random_region_records = []
		
		for chrom, size in chrom_sizes.items():
			
			lengths = distributions_to_shuffle[chrom]['lengths']
			distances = distributions_to_shuffle[chrom]['distances']
			
			random.shuffle(lengths)
			random.shuffle(distances)
			
			current_position = 0
			chrom_mask = sorted(mask_dict.get(chrom, []), key=lambda x: x[0])
			mask_index = 0
			mask_length = len(chrom_mask)
			
			for length, distance in zip(lengths, distances):
				start = current_position + distance
				end = start + length
				
				while mask_index < mask_length and chrom_mask[mask_index][1] < start:
					mask_index += 1
				
				while (mask_index < mask_length and 
					   (chrom_mask[mask_index][0] <= start <= chrom_mask[mask_index][1] or 
						chrom_mask[mask_index][0] <= end <= chrom_mask[mask_index][1])):
					start = chrom_mask[mask_index][1] + 1
					end = start + length
					mask_index += 1
				
				if end <= size:
					random_region_records.append({'Chromosome': chrom, 'Start': int(start), 'End': int(end)})
					current_position = end
				else:
					break
		
		df_shuffle = pd.DataFrame.from_records(random_region_records)
		
		gr1 = pr.PyRanges(df_shuffle)
		gr2 = pr.PyRanges(df_static)
		
		# Perform intersection
		df_intersected = gr1.join(gr2, how='left', report_overlap=True).df
		df_intersected = df_intersected[df_intersected['Overlap'] > 0]
		
		num_overlap = len(df_intersected['Overlap'])
		sum_overlap = np.sum(df_intersected['Overlap'])
		
		overlaps.append({'num_overlaps': num_overlap, 'length_overlaps': sum_overlap})
		
	return overlaps
	
def generate_random_overlaps(df_shuffle, df_static, num_permutations, mask_dict, chrom_sizes, num_processes):
		
	# get distribution of distances and lengths
	distributions_to_shuffle = calculate_distributions(df_shuffle)
	
	# this should be parallelized here
	input_list = list(range(num_permutations))  # Example list of length 1000
	slices = create_slices(input_list, num_processes)
	
	with parallel_backend("loky", inner_max_num_threads=2):
		random_overlap_list = Parallel(n_jobs=num_processes, verbose=10, pre_dispatch="all")(delayed(generate_random_overlap_slice)(slice, distributions_to_shuffle, df_static, chrom_sizes, mask_dict) for slice in slices)
	
	random_overlap_records = [item for sublist in random_overlap_list for item in sublist]
	
	df_random_overlaps = pd.DataFrame.from_records(random_overlap_records)

	return df_random_overlaps

def calculate_p(random_list, enrichment):
	
	num_bins = max(random_list) - min(random_list)
	hist, bin_edges = np.histogram(random_list, bins=num_bins, density=True)
	
	x_d = np.linspace(min(random_list), max(random_list), num_bins)
	
	p_value = sum([hist[i] for i, x in enumerate(x_d) if x > enrichment])
		
	return p_value

def enrichment(path_1, path_2, category_field_num_1, category_field_num_2, path_mask, path_sizes, num_permutations, num_processes):
	
	df_mask = pd.read_csv(path_mask, sep='\t', header=None)
	mask_dict = {}
	for record in df_mask.to_dict('records'):
		if record[0] not in mask_dict:
			mask_dict[record[0]] = []
		mask_dict[record[0]].append((record[1], record[2]))
	
	# initialize distances and chromosomes dicts
	df_chrom_sizes = pd.read_csv(path_sizes, sep='\t', header=None)
	chrom_sizes = {}
	for record in df_chrom_sizes.to_dict('records'):
		chrom_sizes[record[0]] = record[1]
	
	df_1, category_field_num_1 = get_df(path_1, category_field_num_1)
	df_2, category_field_num_2 = get_df(path_2, category_field_num_2)
	
	df_1['length'] = df_1['End'] - df_1['Start']
	df_2['length'] = df_2['End'] - df_2['Start']
	
	categories_1 = sorted(list(set(df_1[category_field_num_1].tolist())), key=natural_keys)
	categories_2 = sorted(list(set(df_2[category_field_num_2].tolist())), key=natural_keys)
	
	enrichment_records = []
	
	for category_1 in categories_1:
		
		for category_2 in categories_2:
			
			df_1_filt = df_1.loc[df_1[category_field_num_1] == category_1]
			df_2_filt = df_2.loc[df_2[category_field_num_2] == category_2]
			
			sum_length_1 = np.sum(df_1_filt['length'])
			sum_length_2 = np.sum(df_2_filt['length'])
			
			gr1 = pr.PyRanges(df_1_filt)
			gr2 = pr.PyRanges(df_2_filt)
			
			df_intersected = gr1.join(gr2, how='left', report_overlap=True).df
			df_intersected = df_intersected[df_intersected['Overlap'] > 0]
			
			num_overlaps = len(df_intersected['Overlap'])
			length_overlaps = np.sum(df_intersected['Overlap'])
			
			####################
			# RANDOM INTERSECTIONS
			####################
			shuffle = 2
			if shuffle == 1:
				df_shuffle = df_1_filt
				df_static = df_2_filt
			else:
				df_shuffle = df_2_filt
				df_static = df_1_filt
				
			print(f'Generating {num_permutations} permutations, not in masked region for {category_1} and {category_2} comparison')
			df_random_overlaps = generate_random_overlaps(df_shuffle, df_static, num_permutations, mask_dict, chrom_sizes, num_processes)
			
			mean_length_random_overlaps = np.mean(df_random_overlaps['length_overlaps'])
			mean_num_permutationsom_overlaps = np.mean(df_random_overlaps['num_overlaps'])
			
			length_enrichment = np.log2(length_overlaps / mean_length_random_overlaps)
			num_enrichment = np.log2(num_overlaps / mean_num_permutationsom_overlaps)
			
			length_p = calculate_p(df_random_overlaps['length_overlaps'], length_enrichment)
			num_p = calculate_p(df_random_overlaps['num_overlaps'], num_enrichment)
				
			enrichment_records.append({'category_1': category_1, 'category_2': category_2, 'num_overlaps_log2_enrichment': num_enrichment, 'length_overlaps_log2_enrichment': length_enrichment, 'length_p': length_p, 'num_p': num_p})
	
	df_enrichment = pd.DataFrame.from_records(enrichment_records)
	
	return df_enrichment

# DESCRIPTION
# --------
# Script will calculate enrichment of path_1 vs. path_2
# --------

# Clock CpGs and ChromHMM
# enrichment -path_1 /home/data/Shared/shared_datasets/wgbs/nlaszik/horvath_clock_skin_blood/separated -path_2 /home/data/Shared/shared_datasets/chip_seq/data/roadmap_epigenomics_chromhmm/data/E016_25_imputed12marks_dense.bed -category_field_num_2 3 -path_mask /home/data/Shared/genome_reference_files/hg19/hg19_gap.bed -path_sizes /home/data/Shared/genome_reference_files/hg19/hg19.sizes -path_out_csv /home/data/Shared/shared_datasets/wgbs/nlaszik/horvath_clock_skin_blood/test.enrichment.csv -num_processes 64 -num_permutations 1000

def parse_arguments():
	"""
	Parses command-line arguments.
	"""
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-path_1", required = True)
	parser.add_argument("-path_2", required = True)
	parser.add_argument("-path_mask", required = True)
	parser.add_argument("-path_sizes", required = True)
	parser.add_argument("-num_permutations", required = True)
	parser.add_argument("-num_processes", required = True)
	parser.add_argument("-path_out_csv", required = True)
	parser.add_argument("-category_field_num_1", required = False)
	parser.add_argument("-category_field_num_2", required = False)
	
	# get arguments
	return parser.parse_args()

def main():
	
	"""
	Main function for command-line usage.
	"""
	args = parse_arguments()
	
	path_1 = args.path_1
	path_2 = args.path_2
	path_mask = args.path_mask
	path_sizes = args.path_sizes
	num_permutations = int(args.num_permutations)
	num_processes = int(args.num_processes)
	category_field_num_1 = args.category_field_num_1
	category_field_num_2 = args.category_field_num_2
	path_out_csv = args.path_out_csv
	
	df = enrichment(path_1, path_2, category_field_num_1, category_field_num_2, path_mask, path_sizes, num_permutations, num_processes)
	
	df.to_csv(path_out_csv)

if __name__ == "__main__":
	main()





