import pandas as pd
import generate_probe_pairs_snakemake2 as generate_probe_pairs  # Import the corrected module
import sys

def main(primer3_output_file, blast_output_file, output_file_name):
    # Open a log file to record debug information
    log_file = open('process_log.txt', 'w')

    # Import probe pairs from generate_probe_pairs_snakemake2.py
    log_file.write("Reading primer3 output file...\n")
    sequences = generate_probe_pairs.process(primer3_output_file)  # Pass the argument here
    log_file.write(f"Number of sequences processed: {len(sequences)}\n")

    # Read BLAST output for off-target hybridization
    log_file.write("Reading BLAST output file...\n")
    hits = pd.read_csv(blast_output_file, sep='\t', header=None, names=['probe_id', 'sseqid', 'pident'])
    log_file.write(f"Number of BLAST hits: {len(hits)}\n")

    # Filter out probes with more than one BLAST hit (non-specific probes)
    hits2 = hits[hits['probe_id'].duplicated(keep=False)]
    nonspec_probes = hits2['probe_id'].values.tolist()
    log_file.write(f"Number of non-specific probes: {len(nonspec_probes)}\n")

    for sequence in sequences:
        sequence.PROBES = [probe for probe in sequence.PROBES if probe.LHS_ID not in nonspec_probes]
        log_file.write(f"Number of probes after specificity filter for sequence {sequence.ID}: {len(sequence.PROBES)}\n")

    # Filter out probes that overlap
    for sequence in sequences:
        iterator = 0
        while iterator < len(sequence.PROBES) - 1:
            if sequence.PROBES[iterator].END > sequence.PROBES[iterator + 1].START:
                del sequence.PROBES[iterator + 1]
            else:
                iterator += 1
        log_file.write(f"Number of probes after overlap filter for sequence {sequence.ID}: {len(sequence.PROBES)}\n")

    # Keep only the first 3 probe pairs per sequence
    for sequence in sequences:
        sequence.PROBES = sequence.PROBES[:3]
        log_file.write(f"Number of probes after limiting to 3 for sequence {sequence.ID}: {len(sequence.PROBES)}\n")

    # Print the final selected probe pairs in the specified format
    with open(output_file_name, 'w') as output_file:
        for sequence in sequences:
            output_file.write(f"Sequence id: {sequence.ID}\n")
            output_file.write(f"Sequence template:\n{sequence.TEMPLATE}\n")
            output_file.write("\nProbes:\n")
            for probe in sequence.PROBES:
                output_file.write(f"\n     probe pair LHS ID: {probe.LHS_ID}\n")
                output_file.write(f"     probe pair RHS ID: {probe.RHS_ID}\n")
                output_file.write(f"     probe pair START: {probe.START}\n")
                output_file.write(f"     probe pair END: {probe.END}\n")
                output_file.write(f"     probe LHS: {probe.LHS}\n")
                output_file.write(f"     probe LHS GC: {float(probe.LHS_GC):.3f}\n")
                output_file.write(f"     probe RHS: {probe.RHS}\n")
                output_file.write(f"     probe RHS GC: {float(probe.RHS_GC):.3f}\n")
                output_file.write("     -----------------\n")

    # Close the log file
    log_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python select_probe_pairs2.py <primer3_output_file> <blast_output_file> <output_file_name>")
        sys.exit(1)

    primer3_output_file = sys.argv[1]
    blast_output_file = sys.argv[2]
    output_file_name = sys.argv[3]

    main(primer3_output_file, blast_output_file, output_file_name)

