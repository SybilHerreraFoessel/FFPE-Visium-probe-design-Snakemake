"""
script for selecting final probe pairs based on: 
- off target hybridisation (BLAST OUTPUT)
- non overlapping target region
- max probe pairs per gene = 3

input files: 
- python code for generating initial probe pairs 
- trimmed BLAST output generated using target_specificity_trim.py 
- primer3_output.txt

output: final probe pairs 
corrected to correct path for trimmed file
"""
import pandas as pd
import generate_probe_pairs_snakemake2 as generate_probe_pairs  # Import your modified generate_probe_pairs_snakemake2.py script

# Import probe pairs from generate_probe_pairs_snakemake2.py
sequences = generate_probe_pairs.process('primer3_output.txt')

# Read BLAST output for off-target hybridization
hits = pd.read_csv('trimmed_paired_probes_target_specificity_CDS.txt', sep=' ')

# Filter out probes with more than one BLAST hit (non-specific probes)
hits2 = hits[hits['probe_id'].duplicated(keep=False)]
nonspec_probes = hits2['probe_id'].values.tolist()

for sequence in sequences:
    sequence.PROBES = [probe for probe in sequence.PROBES if probe.LHS_ID not in nonspec_probes]

# Filter out probes that overlap
for sequence in sequences:
    iterator = 0
    while iterator < len(sequence.PROBES) - 1:
        if sequence.PROBES[iterator].END > sequence.PROBES[iterator + 1].START:
            del sequence.PROBES[iterator + 1]
        else:
            iterator += 1

# Keep only the first 3 probe pairs per sequence
for sequence in sequences:
    sequence.PROBES = sequence.PROBES[:3]

# Print or process the final selected probe pairs
generate_probe_pairs.printer(sequences)

