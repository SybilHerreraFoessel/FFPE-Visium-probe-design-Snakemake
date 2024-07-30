import sys
import pandas as pd
from Bio import SeqIO

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Usage: python primer3_input_design2.py Input_genes_to_pipeline.xlsx Potra02_CDS.fa")

    input_excel = sys.argv[1]
    ref_genome = sys.argv[2]

    try:
        # Read input Excel file with gene IDs
        df = pd.read_excel(input_excel)
        genelist_full = df['gene']

        # Remove duplicates within the DataFrame
        genelist_full = genelist_full.drop_duplicates()

        # Get transcript information from reference genome into DataFrame
        ids = []
        sequences = []
        for record in SeqIO.parse(ref_genome, "fasta"):
            ids.append(record.id.split('.')[0])  # remove part after period from gene_id
            sequences.append(str(record.seq))

        d = {'gene_id': ids, 'Sequence': sequences}
        seq_df = pd.DataFrame(d)
        seq_df = seq_df[seq_df['gene_id'].isin(genelist_full)]  # keep only genes in the df which correspond to the list of genes of interest
        seq_df = seq_df.drop_duplicates(subset=['gene_id'])  # drop duplicate gene_ids, keep the first transcript (ending at .1)
        seq_df = seq_df.reset_index(drop=True)

        # Write primer3 input file
        output_file = "primer3_input_full.txt"
        with open(output_file, 'w') as f:
            for index, row in seq_df.iterrows():
                f.write('SEQUENCE_ID=' + row['gene_id'] + '\n')
                f.write('SEQUENCE_TEMPLATE=' + row['Sequence'] + '\n')
                f.write('PRIMER_PICK_LEFT_PRIMER=0' + '\n')  # indicate creation of hybridising probes instead of primers
                f.write('PRIMER_PICK_INTERNAL_OLIGO=1' + '\n')  # indicate creation of hybridising probes instead of primers
                f.write('PRIMER_PICK_RIGHT_PRIMER=0' + '\n')  # indicate creation of hybridising probes instead of primers
                f.write('PRIMER_INTERNAL_MIN_SIZE=25' + '\n')  # probe size
                f.write('PRIMER_INTERNAL_OPT_SIZE=25' + '\n')  # probe size
                f.write('PRIMER_INTERNAL_SIZE=25' + '\n')  # probe size
                f.write('PRIMER_MAX_NS_ACCEPTED=1' + '\n')  # max number of unknown nucleotides
                f.write('PRIMER_INTERNAL_MIN_GC=44' + '\n')  # minimum GC percentage
                f.write('PRIMER_INTERNAL_MAX_GC=72' + '\n')  # maximum GC percentage
                f.write('PRIMER_INTERNAL_MAX_POLY_X=5' + '\n')  # maximum length of mononucleotide repeats
                f.write('PRIMER_NUM_RETURN=35' + '\n')  # number of primers to return
                f.write('PRIMER_EXPLAIN_FLAG=1' + '\n')  # get statistics of primer
                f.write('=' + '\n')  # indicate end of parameters

    except Exception as e:
        print("An error occurred:", str(e))

