#!/bin/bash
#SBATCH -N 1 -n 1 -c 15
#SBATCH --mem 64000
#SBATCH -t 12:00:00
#SBATCH -J blastn_job
#SBATCH --mail-user sybil.herrera.foessel@scilifelab.se
#SBATCH --mail-type=ALL
#SBATCH -e job-%J.err
#SBATCH -o job-%J.out

# Activate the Conda environment
echo "Activating Conda environment"
source /home/sybil.hf/miniconda3/bin/activate /home/sybil.hf/miniconda3/envs/probes_env

# Define output directory
output_dir="filtered_results"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Run BLAST search with the correct path to the database index file
blastn -query /home/sybil.hf/probes_populus/30_Apr_24_probes/3_May_24_probes/merge_probes/cleaned_sequences.fasta -db ../cluster_data -out "$output_dir/results.txt" -outfmt 6

# Filter results to include only matches with >= 99% identity
awk '$3 >= 99' "$output_dir/results.txt" > "$output_dir/filtered_results.txt"

# Notify user of completion
echo "Filtering completed. Filtered results are saved in '$output_dir/filtered_results.txt'."

