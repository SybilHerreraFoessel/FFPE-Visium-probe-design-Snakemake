"""
Keep the highest percentage identify per gene for the probe hybridisation.
Get rid of transcript variants as a column and replace them with gene IDs 
It has been modified to skip rows that are innecessary.

"""
import pandas as pd

# Read the data from the input file
df = pd.read_csv("probes_pairs_comb_target_specificity_CDS.txt",
                 sep="\t",
                 names=["probe_id", "transcript_id", "percentage_ident"])

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
df.to_csv("trimmed_paired_probes_target_specificity_CDS.txt", sep=" ", index=False, header=True)

