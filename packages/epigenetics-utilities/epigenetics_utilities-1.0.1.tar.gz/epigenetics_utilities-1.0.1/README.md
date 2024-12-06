# epigenetics_utilities
Various utilities for epigenetics or genomics research

## Installation & General Usage

```bash
pip install epigenetics-utilities
```

## Usage

Functions can be used through the command line or imported as functions in Python.

Examples:

```bash
cluster_regions --path_bed ./bedfile.bed --value_thresholds="-1,0,1" --distance_threshold 1000 --min_num_values 3 --path_out_dir
```

```python
import epigenetics_utilities as eu
df_clusters = eu.cluster_regions('bedfile.bed', '-1,0,1', 1000)
```

Functions:

1. cluster_regions
2. enrichment
3. odds_ratio_intersection

### cluster_regions

This function joins regions together in a bed file based off a distance threshold. It is ideally used for creating things like Differentially Methylated Regions (DMRs).

#### Input BED File

| column | name                  | description                 | type  |
|--------|-----------------------|-----------------------------|-------|
| 1      | chrom                 | name of the chromosome      | str   |
| 2      | start position        | start position of cpg       | int   |
| 3      | end position          | end position of cpg         | int   |
| 4      | value                 | some value for filtering	   | float |

Input bed file must be sorted

#### Input Arguments

The other command line arguments to the code are as follows:

| name                  | description                                            | type  |
|-----------------------|--------------------------------------------------------|-------|
| path_bed              | path of input bed file                                 | str   |
| value_thresholds      | comma-separated thresholds for filtering (i.e. -1,0,1) | str   |
| distance_threshold    | distance threshold in basepairs                        | int   |
| min_num_values        | minimum number of values in a region                   | int   |
| path_out_dir          | path of directory to write output beds to              | str   | 

#### Output BED

| column | name                  | description                 | type  |
|--------|-----------------------|-----------------------------|-------|
| 1      | chrom                 | name of the chromosome      | str   |
| 2      | start position        | start position of cpg       | int   |
| 3      | end position          | end position of cpg         | int   |
| 4      | value                 | average value               | float |
| 5      | num                   | number of values in region  | float |

### enrichment

### odds_ratio_intersection