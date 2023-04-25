"""
script for selecting final probe pairs based on: 
- off target hybridisation (BLAST OUTPUT)
- non overlapping target region
- max probe pairs per gene = 3

input files: 
- python code for generating initial probe pairs 
- trimmed BLAST output generated using target_specificity_trim.py 

output: final probe pairs 
"""

import pandas as pd 

## import initial probe pairs 
import generate_probe_pairs
sequences = generate_probe_pairs.process()

## import BLAST output for off-target hybridisation
hits = pd.read_csv('trimmed_paired_probes_target_specificity_CDS.txt', sep = ' ')
#print(hits['percentage_ident'].min()) #gives 88% 

## delete probes which have >1 BLAST hits 
hits2 = hits[hits['probe_id'].duplicated(keep = False) == True] #make dataframe only containing probes with >1 hit
#hits2 = hits2.sort_values(by=['probe_id'])
nonspec_probes = hits2['probe_id'].values.tolist() #create list of probe_ids which have >1 hits (non-specific) 
for sequence in sequences: 
    for i, probe in enumerate(sequence.PROBES): 
            for nonspec_probe in nonspec_probes:
                if nonspec_probe == probe.LHS_ID: 
                    del sequence.PROBES[i]
                    break 

## delete probes which overlap 
for sequence in sequences:
    iterator = 0
    while iterator < len(sequence.PROBES)-1:
        if sequence.PROBES[iterator].END > sequence.PROBES[iterator+1].START:
            del sequence.PROBES[iterator+1]
        else:
             iterator = iterator + 1

## keep first 3 probe pairs 
for index, sequence in enumerate(sequences): 
    while len(sequence.PROBES) > 3:
        del sequence.PROBES[-1]

## delete sequences without probes (if desirable) (not working at the moment)
# for i, sequence in enumerate(sequences): 
#     if len(sequence.PROBES) == 0:
#         del sequences[i]
#         break

generate_probe_pairs.printer(sequences)
