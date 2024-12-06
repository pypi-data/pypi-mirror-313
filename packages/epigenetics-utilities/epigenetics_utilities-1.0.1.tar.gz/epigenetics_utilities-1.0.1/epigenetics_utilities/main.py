# main.py
#from .gene import query_enhancer_atlas, find_most_likely_gene_coordinates, query_gtf_coordinates, query_mygene_coordinates
from .odds_ratio_intersection import odds_ratio_intersection
from .enrichment import enrichment
from .cluster_regions import cluster_regions

################
# FUNCTIONS
################

def cluster_regions(df, value_threshold_pair, distance_threshold, min_num_values, suffix=None):

	return cluster_regions(df, value_threshold_pair, distance_threshold, min_num_values, suffix)

def enrichment(path_1, path_2, category_field_num_1, category_field_num_2, path_mask, path_sizes, num_permutations, num_processes):

	return enrichment(path_1, path_2, category_field_num_1, category_field_num_2, path_mask, path_sizes, num_permutations, num_processes)

def odds_ratio_intersection(path_1, path_2, category_field_num_1, category_field_num_2):

	return odds_ratio_intersection(path_1, path_2, category_field_num_1, category_field_num_2)
