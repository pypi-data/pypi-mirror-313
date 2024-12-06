import os
import sys
import re

import pandas as pd

import mygene

from .util import *

def query_enhancer_atlas(path_enhancer_file):
	
	"""
	
	Queries an enhancer atlas txt file and returns a dictionary of coordinates. Can additionally pass a list of gene/transcript names/ids to filter.
	Return format: {gene_name: [[chromosome, start, stop], [chromosome, start, stop] ... ] ... }

	:param path_enhancer_file:	Path of the enhancer atlas text file
	
	Example:
	
	>>> return_dict = query_enhancer_atlas('/home/data/Shared/genome_reference_files/hg19/regions/hg19_H1_EnhancerGenePair_EnhancerAtlas2.0.txt')
	
	"""
	
	enhancer_df_ga = pd.read_csv(path_enhancer_file, sep='\t', names = ['data', 'wtf'])
	enhancer_ga_records = enhancer_df_ga.to_records()
	enhancer_gene_pairs = [enhancer['data'].replace(':','\t').replace('-','\t').replace('_','\t').replace('$','\t').split('\t') for enhancer in enhancer_ga_records]
	enhancer_ga_records = [{'chrom': enhancer_gene_pair[0], 'start': int(enhancer_gene_pair[1]), 'stop': int(enhancer_gene_pair[2]), 'genecard_id': enhancer_gene_pair[4]} for enhancer_gene_pair in enhancer_gene_pairs]
	
	enhancer_coord_dict = {}
	
	for enhancer in enhancer_ga_records:
	
		if enhancer['genecard_id'] not in enhancer_coord_dict:
			enhancer_coord_dict[enhancer['genecard_id']] = []
		
		enhancer_coord_dict[enhancer['genecard_id']].append([enhancer['chrom'], enhancer['start'], enhancer['stop']])
		
	return enhancer_coord_dict

def prepare_chromhmm(path_chrom_hmm):
	
	df = pd.read_csv(path_chrom_hmm, names=['chrom', 'start', 'stop', 'class', 'null1', 'null2', 'null3', 'null4', 'null5'], sep='\t')
	
	df = df[['chrom', 'start', 'stop', 'class']]
	
	df = df.dropna()
	
	df['start'] = df['start'].astype(int)
	df['stop'] = df['stop'].astype(int)
	
	chromhmm_list = df.to_dict('records')
	
	chromhmm_by_chrom = {}
	for i, entry in enumerate(chromhmm_list):
		
		chrom = entry['chrom']
		entry['index'] = i
		entry['midpoint'] = (entry['start'] + entry['stop'])/2
		
		if chrom not in chromhmm_by_chrom:
			chromhmm_by_chrom[chrom] = []
			
		chromhmm_by_chrom[chrom].append(entry)
		
	return chromhmm_by_chrom, chromhmm_list

def find_chromhmm_mark(chromhmm_list, i, direction, match_list=None, no_match_list=None):
	
	if no_match_list is not None and match_list is not None:
		print('please select only non-matching regions, or matching regions, cant do both')
		return False
		
	if no_match_list is None and match_list is None:
		print('please select at least one of non-matching regions or matching regions')
		return False
	
	while True:
		if direction == '+':
			if i >= len(chromhmm_list):
				return i - 1
			entry = chromhmm_list[i]
			if (no_match_list is not None and entry['class'] not in no_match_list) or (match_list is not None and entry['class'] in match_list):
				return i
			i += 1
		else:
			if i == 0:
				return i
			entry = chromhmm_list[i]
			if (no_match_list is not None and entry['class'] not in no_match_list) or (match_list is not None and entry['class'] in match_list):
				return i
			i -= 1

def find_most_likely_gene_coordinates(path_gtf, path_chromhmm, sequence_type, key, chromhmm_tss_identifier, return_type='list'):
	
	"""
	
	Queries a gtf file and returns a dictionary of coordinates. Can additionally pass a list of gene/transcript names/ids to filter.
	Return format: {key: [chromosome, gene_start, gene_stop, strand] ... }

	:param path_gtf:		Path to a gtf file

	:param sequence_type:	Which relevant genomic type is to be retrieved from the gtf file. 
							Possible values: transcript, exon, 5UTR, CDS, start_codon, stop_codon, 3UTR
	
	:param key: 			Which information to use as the key for the return dictionary.
							Possible values: gene_id, transcript_id, exon_number, exon_id, gene_name
							
	:param gene_name_filter_list:		Optional, function returns a truncated dictionary containing information for matching keys.
	
	
	Example:
	
	>>> query_gtf_coordinates('/home/data/Shared/genome_reference_files/hg19/hg19.refGene.gtf', 'transcript', 'gene_name', gene_name_filter_list = ['GAPDH'])
	
	"""
	
	#'/home/data/Shared/genome_reference_files/hg19/hg19.refGene.gtf'
	# sequence_type='transcript', key='gene_name'
	
	chromhmm_by_chrom, chromhmm_list = prepare_chromhmm(path_chromhmm)
	
	gtf_df = pd.read_csv(path_gtf, sep='\t', names=['chrom', 'gene_id_source', 'sequence_type', 'start', 'stop', 'null1', 'strand', 'null2', 'id_data'])
	gtf_df_transcripts = gtf_df.loc[gtf_df['sequence_type'] == sequence_type]
	gtf_df_transcripts_records = gtf_df_transcripts.to_records()
	
	gene_coordinate_dict = {}
	for record in gtf_df_transcripts_records:
		id_data = string_to_dict(record['id_data'], item_delimiter=';', pair_delimiter=None)
		if key in id_data:
			gene_name = id_data[key].replace('"', '')
			if gene_name not in gene_coordinate_dict:
				gene_coordinate_dict[gene_name] = []
			gene_coordinate_dict[gene_name].append({'chrom': record['chrom'], 'start': record['start'], 'stop': record['stop'], 'strand': record['strand']})
	
	real_gene_coordinate_dict = {}
	
	for gene_name in gene_coordinate_dict:
		if len(gene_coordinate_dict[gene_name]) > 0:
		
			distances_to_closest_tss = []
			in_chrom = True
			for possible_gene_coordinate in gene_coordinate_dict[gene_name]:
				
				chrom = possible_gene_coordinate['chrom']
				strand = possible_gene_coordinate['strand']
				
				if chrom not in chromhmm_by_chrom:
					in_chrom = False
					break
				
				if strand == '+':
					gene_tss = int(possible_gene_coordinate['start'])
				else:
					gene_tss = int(possible_gene_coordinate['stop'])
				
				# for alternate entry, see if TSS overlaps directly
				for chromhmm_entry in chromhmm_by_chrom[chrom]:
					i = chromhmm_entry['index']
					if gene_tss > chromhmm_entry['start'] and gene_tss < chromhmm_entry['stop']:
						break
						
				if chromhmm_list[i]['class'] == chromhmm_tss_identifier:
					# direct TSS overlap
					distances_to_closest_tss.append(i)
				else:
					
					i_nearest_tss_right = find_chromhmm_mark(chromhmm_list, i, '+', match_list=[chromhmm_tss_identifier])
					i_nearest_tss_left = find_chromhmm_mark(chromhmm_list, i, '-', match_list=[chromhmm_tss_identifier])
					
					closest_midpoint = min(chromhmm_list[i_nearest_tss_right]['midpoint'], chromhmm_list[i_nearest_tss_left]['midpoint'])
					
					distances_to_closest_tss.append(closest_midpoint)
				
			if in_chrom:
				
				most_likely_tss_i = distances_to_closest_tss.index(min(distances_to_closest_tss))
				real_gene_coordinate_dict[gene_name] = gene_coordinate_dict[gene_name][most_likely_tss_i]
				
		else:
			
			real_gene_coordinate_dict[gene_name] = gene_coordinate_dict[gene_name][0]
			
	if return_type == 'list':
		return_dict_list = {}
		for gene in real_gene_coordinate_dict:
			return_dict_list[gene] = [real_gene_coordinate_dict[gene]['chrom'], int(real_gene_coordinate_dict[gene]['start']), int(real_gene_coordinate_dict[gene]['stop']), real_gene_coordinate_dict[gene]['strand']]
		return return_dict_list
	else:
		return real_gene_coordinate_dict

def query_gtf_coordinates(path_gtf, sequence_type, key, gene_name_filter_list = None):
	
	"""
	
	Queries a gtf file and returns a dictionary of coordinates. Can additionally pass a list of gene/transcript names/ids to filter.
	Return format: {key: [chromosome, gene_start, gene_stop, strand] ... }

	:param path_gtf:		Path to a gtf file

	:param sequence_type:	Which relevant genomic type is to be retrieved from the gtf file. 
							Possible values: transcript, exon, 5UTR, CDS, start_codon, stop_codon, 3UTR
	
	:param key: 			Which information to use as the key for the return dictionary.
							Possible values: gene_id, transcript_id, exon_number, exon_id, gene_name
							
	:param gene_name_filter_list:		Optional, function returns a truncated dictionary containing information for matching keys.
	
	
	Example:
	
	>>> query_gtf_coordinates('/home/data/Shared/genome_reference_files/hg19/hg19.refGene.gtf', 'transcript', 'gene_name', gene_name_filter_list = ['GAPDH'])
	
	"""
	
	#'/home/data/Shared/genome_reference_files/hg19/hg19.refGene.gtf'
	# sequence_type='transcript', key='gene_name'
	
	gtf_df = pd.read_csv(path_gtf, sep='\t', names=['chromosome', 'gene_id_source', 'sequence_type', 'start', 'stop', 'null1', 'strand', 'null2', 'id_data'])
	
	gtf_df_transcripts = gtf_df.loc[gtf_df['sequence_type'] == sequence_type]
	gtf_df_transcripts_records = gtf_df_transcripts.to_records()
	
	gene_coordinate_dict = {string_to_dict(record['id_data'], item_delimiter=';', pair_delimiter=None)[key].replace('"', ''): [str(record['chromosome']), int(record['start']), int(record['stop']), str(record['strand'])] for record in gtf_df_transcripts_records if key in string_to_dict(record['id_data'], item_delimiter=';', pair_delimiter=None)}
	
	if gene_name_filter_list is not None:
	
		filtered_gene_coordinate_dict = {gene_name: gene_coordinate_dict[gene_name] for gene_name in gene_name_filter_list if gene_name in gene_coordinate_dict}
		print(len(gene_name_filter_list) - len(filtered_gene_coordinate_dict), 'genes not found in gtf')
		return filtered_gene_coordinate_dict
		
	else:
		
		return gene_coordinate_dict


def query_mygene_coordinates(gene_id_list, *ignore, scopes=None, genome=None):
	
	"""
	
	Queries the mygene.info database with a list of gene names/ids and returns a dictionary with their coordinates.

	:param gene_id_list:	A list of query terms, should be gene ids/names in string format
	
	:param scopes: 		A list of of types of gene ids/names that should be matched to, in descending order of priority.
				Should contain any of the following: ['ensembl', 'entrezgene', 'refseq', 'symbol', 'alias', 'name', 'other_names']
				Pass multiple in the event that your list of gene ids/names aren't all the same type.
				For example, if list contains some outdated gene symbols, add 'alias' as an additional scope.
				In the event of a duplicate, the highest priority scope will match the query term.
							
	:param genome:		'hg19' or 'hg38'
	
	
	Example:
	
	>>> query_coordinates(['YATS2'], scopes=['symbol','alias'], genome='hg19')
	
	"""
	
	# some incorrect arugments
	if ignore:  # If ignore is not empty
		raise TypeError("Incorrect arguments provided. Example usage: query_coordinates([['YEATS2']], scopes=['symbol','alias'], genome=hg19)")
	
	# check scopes
	if type(scopes) != list:
		raise TypeError("Invalid 'scopes' argument. Scopes should be a list of potential name/id types in string form that you would like to match to.\nAny of the following: ['ensembl', 'entrezgene', 'refseq', 'symbol', 'alias', 'name', 'other_names']. Pass in order of descending importance in case of duplicate return values.")
		
	valid_scopes = ['ensembl', 'entrezgene', 'refseq', 'symbol', 'alias', 'name', 'other_names']
	
	if any(scope not in valid_scopes for scope in scopes):
		raise NameError("Invalid entry in 'scopes' argument.\nShould contain any of the following: ['ensembl', 'entrezgene', 'refseq', 'symbol', 'alias', 'name', 'other_names']. Pass in order of descending importance in case of duplicate return values.")
	
	# check genome
	if genome != 'hg19' and genome != 'hg38':
		raise NameError("Invalid 'genome' argument. Should be either 'hg19' or 'hg38' as a string")

	mg = mygene.MyGeneInfo()
	
	if genome == 'hg19':
		position_field = 'genomic_pos_hg19'
	elif genome == 'hg38':
		position_field = 'genomic_pos'
		
	mg_response = mg.querymany(gene_id_list, scopes=scopes, species='human', fields=position_field)
	
	mg_response_dict = {}
	for gene in mg_response:
		if position_field in gene:
			if gene['query'] in mg_response_dict:
				# this is the duplicate entry case
				# remap this if the current gene symbol matches the current gene query
				
				if gene['query'] not in mg_response_dict:
					mg_response_dict[gene['query']] = gene[position_field]
				else:
					# check scope to see if existing entry should be rewritten
					for scope in reversed(scopes):
						if scope in gene:
							if gene[scope] == gene['query']:
								mg_response_dict[gene['query']] = gene[position_field]
			else:
				mg_response_dict[gene['query']] = gene[position_field]
		elif gene['query'] not in mg_response_dict:
			mg_response_dict[gene['query']] = 'not found'
	
	return mg_response_dict