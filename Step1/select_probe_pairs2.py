"""
script for selecting final probe pairs based on: 
- off target hybridisation (BLAST OUTPUT)
- non overlapping target region
- max probe pairs per gene = 3

input files: 
- python code for generating initial probe pairs 
- trimmed BLAST output generated using target_specificity_trim.py 

output: final probe pairs 
corrected to correct path for trimmed file
"""
import pandas as pd

# Import initial probe pairs
import generate_probe_pairs
sequences = generate_probe_pairs.process()

# Import BLAST output for off-target hybridisation
hits = pd.read_csv('trimmed_paired_probes_target_specificity_CDS.txt', sep=' ')

# Delete probes which have >1 BLAST hits
hits2 = hits[hits['probe_id'].duplicated(keep=False)]
nonspec_probes = hits2['probe_id'].tolist()

for sequence in sequences:
    sequence.PROBES = [probe for probe in sequence.PROBES if probe.LHS_ID not in nonspec_probes]

# Delete probes which overlap
for sequence in sequences:
    iterator = 0
    while iterator < len(sequence.PROBES) - 1:
        if sequence.PROBES[iterator].END > sequence.PROBES[iterator + 1].START:
            del sequence.PROBES[iterator + 1]
        else:
            iterator += 1

# Keep first 3 probe pairs
for sequence in sequences:
    while len(sequence.PROBES) > 3:
        del sequence.PROBES[-1]

# Print or write selected probes
with open('selected_probes.txt', 'w') as f:
    for sequence in sequences:
        for probe in sequence.PROBES:
            f.write(f"{probe.LHS_ID}\t{probe.RHS_ID}\n")

