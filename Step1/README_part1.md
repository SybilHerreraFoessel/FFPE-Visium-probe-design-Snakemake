# FFPE Visium probe design with snakemake part 1
The pipeline developed by Ireen van Dolderen (with different python scripts) has been modified by Sybil Herrera Foessel to be 
run as a Snakemake workflow system (all necessary files included in the Step1 folder).   

## Files needed

- Input_genes_to_pipeline.xlsx #input file 1. #paste genes of interest in 'gene' column
- Snakefile_part1_blast_twice_log 
- primer3_input_design2.py
- generate_probe_pairs_snakemake3.py
- target_specificity_trim_CDS_genome.py
- select_probe_pairs_after_blast_twice.py
- probes_env.yaml


In the Snakefile adjust the blast parameters for each respective rule (CDS and genome)

        evalue=10, # default 10
        
        word_size=11, # default 11
        
        reward=1, # default 1
        
        penalty=-2, # default -2
        
        task="blastn-short" # default blastn

Final output for part1: selected_probes.txt and the process_log.log file

Copy selected_probes.txt for running part2 $cp selected_probes.txt part2/. 
