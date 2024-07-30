import pandas as pd
import sys
import generate_probe_pairs_snakemake2 as generate_probe_pairs  # Ensure the module is correct

def main(primer3_output_file, cds_blast_output_file, genome_blast_output_file, output_file_name):
    # Open a log file to record debug information
    with open('process_log.txt', 'w') as log_file:

        # Import probe pairs from generate_probe_pairs_snakemake2.py
        log_file.write("Reading primer3 output file...\n")
        sequences = generate_probe_pairs.process(primer3_output_file)  # Pass the argument here
        log_file.write(f"Number of sequences processed: {len(sequences)}\n")

        # Read BLAST output for CDS
        log_file.write("Reading CDS BLAST output file...\n")
        hits_cds = pd.read_csv(cds_blast_output_file, sep='\t', header=None, names=['probe_id', 'sseqid', 'pident'])
        log_file.write(f"Number of CDS BLAST hits: {len(hits_cds)}\n")

        # Read BLAST output for genome
        log_file.write("Reading genome BLAST output file...\n")
        hits_genome = pd.read_csv(genome_blast_output_file, sep='\t', header=None, names=['probe_id', 'sseqid', 'pident'])
        log_file.write(f"Number of genome BLAST hits: {len(hits_genome)}\n")

        # Combine CDS and genome hits
        combined_hits = pd.concat([hits_cds, hits_genome])
        log_file.write(f"Total number of combined BLAST hits: {len(combined_hits)}\n")

        # Identify non-specific probes
        non_specific_hits = combined_hits[combined_hits['probe_id'].duplicated(keep=False)]

        # Log non-specific probes for CDS
        cds_non_specific = hits_cds[hits_cds['probe_id'].isin(non_specific_hits['probe_id'])]
        log_file.write("Non-specific probes (CDS):\n")
        for _, row in cds_non_specific.iterrows():
            log_file.write(f"Probe ID: {row['probe_id']}, Gene ID: {row['sseqid']}, Percentage Identity: {row['pident']}\n")

        # Log non-specific probes for genome
        genome_non_specific = hits_genome[hits_genome['probe_id'].isin(non_specific_hits['probe_id'])]
        log_file.write("Non-specific probes (Genome):\n")
        for _, row in genome_non_specific.iterrows():
            log_file.write(f"Probe ID: {row['probe_id']}, Gene ID: {row['sseqid']}, Percentage Identity: {row['pident']}\n")

        # Filter sequences based on non-specific probes
        for sequence in sequences:
            sequence.PROBES = [probe for probe in sequence.PROBES if probe.LHS_ID not in non_specific_hits['probe_id'].values.tolist()]
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

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python select_probe_pairs_after_blast_twice.py <primer3_output_file> <cds_blast_output_file> <genome_blast_output_file> <output_file_name>")
        sys.exit(1)

    primer3_output_file = sys.argv[1]
    cds_blast_output_file = sys.argv[2]
    genome_blast_output_file = sys.argv[3]
    output_file_name = sys.argv[4]

    main(primer3_output_file, cds_blast_output_file, genome_blast_output_file, output_file_name)


