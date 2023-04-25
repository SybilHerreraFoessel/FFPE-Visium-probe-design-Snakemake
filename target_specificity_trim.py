"""
Keep the highest percentage identify per gene for the probe hybridisation.
Get rid of transcript variants as a column and replace them with gene IDs 
"""

import pandas as pd 

df = pd.read_csv("probes_pairs_comb_target_specificity_CDS.txt", 
                 sep = "\t",
                 names = ["probe_id", "transcript_id", "percentage_ident"])
df['gene_id'] = df['transcript_id'].str.split('.').str[0] #remove part after period from gene_id
df = df.sort_values(["probe_id", "gene_id", "percentage_ident"]) #sort first on probe_id, then gene_id and then percentage identity
df = df.drop_duplicates(
  subset = ['probe_id', 'gene_id'],
  keep = 'first').reset_index(drop = True)
df = df.drop(['transcript_id'], axis=1)
df = df.loc[:,['probe_id', 'gene_id', 'percentage_ident']] #change order of columns

#export to txt file 
df.to_csv("trimmed_paired_probes_target_specificity_CDS.txt", sep=" ", index=False, header=True)

