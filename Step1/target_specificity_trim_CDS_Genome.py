"""
Keep the highest percentage identify per gene for the probe hybridisation.
Get rid of transcript variants as a column and replace them with gene IDs 
It has been modified to skip rows that are innecessary.

"""
import pandas as pd
import sys

def trim_specificity(input_file, output_file):
    """
    Function to trim specificity of probe pairs from a given input file and save to an output file.
    """
    # Read the data from the input file
    df = pd.read_csv(input_file, sep="\t", names=["probe_id", "transcript_id", "percentage_ident"])

    # Convert transcript_id column to string and split to extract gene_id
    df['gene_id'] = df['transcript_id'].astype(str).str.split('.').str[0]

    # Sort the DataFrame by probe_id, gene_id, and percentage_ident
    df = df.sort_values(["probe_id", "gene_id", "percentage_ident"])

    # Drop duplicates based on probe_id and gene_id, keeping the first occurrence
    df = df.drop_duplicates(subset=['probe_id', 'gene_id'], keep='first').reset_index(drop=True)

    # Drop the transcript_id column
    df = df.drop(['transcript_id'], axis=1)

    # Reorder columns
    df = df.loc[:, ['probe_id', 'gene_id', 'percentage_ident']]

    # Export the trimmed DataFrame to a new text file
    df.to_csv(output_file, sep=" ", index=False, header=True)

def main(cds_input_file, genome_input_file, cds_output_file, genome_output_file):
    # Process CDS input file
    trim_specificity(cds_input_file, cds_output_file)
    
    # Process genome input file
    trim_specificity(genome_input_file, genome_output_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python target_specificity_trim_CDS_Genome.py <cds_input_file> <genome_input_file> <cds_output_file> <genome_output_file>")
        sys.exit(1)

    cds_input_file = sys.argv[1]
    genome_input_file = sys.argv[2]
    cds_output_file = sys.argv[3]
    genome_output_file = sys.argv[4]

    main(cds_input_file, genome_input_file, cds_output_file, genome_output_file)

