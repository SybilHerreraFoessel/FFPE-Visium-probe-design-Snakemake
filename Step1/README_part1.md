# FFPE Visium probe design with snakemake
The pipeline developed by Ireen van Dolderen (with different python scripts) has been modified by Sybil Herrera Foessel to be 
run as a Snakemake workflow system (all necessary files included in the Step1 folder). 

## Files needed

- Input_genes_to_pipeline.xlsx #input file 1. #paste genes of interest in 'gene' column 
- primer3_input_design2.py
- generate_probe_pairs_snakemake2.py
- target_specificity_trim.py
- select_probe_pairs.py
- Snakefile_part1
- probes_env.yaml
