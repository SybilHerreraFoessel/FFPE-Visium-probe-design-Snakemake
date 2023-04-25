# FFPE-ST-probe-design-

## Files needed

- top10_marker_genes_T89.xlsx #Excel file with top X differentially expressed gene in clusters, generated using Seurat
- markergenes_plus_conversion.xlsx #Excel file with marker genes based on literature research
- primer3_intput_design_T89.py
- generate_probe_pairs.py
- target_specificity_trim.py
- select_probe_pairs.py

## Output files

- primer3_input_full.txt
- primer3_output.txt
- probe_pairs_hyb_T89.fasta
- possible_probe_pairs.txt
- probes_pairs_comb_target_specificity_CDS.txt
- trimmed_paired_probes_target_specificity_CDS.txt
- selected_probes.txt

---

## Preparation

1. Differential gene expression analysis in R
2. Marker gene identification from the literature
3. download CDS (spliced transcriptome) fasta file for reference genome using `$wget [ftp://plantgenie.org:980/Data/PlantGenIE/Populus_tremula_X_Populus_tremuloides/v1.0.1/fasta/Potrx01-CDS.fa.gz](ftp://plantgenie.org:980/Data/PlantGenIE/Populus_tremula_X_Populus_tremuloides/v1.0.1/fasta/Potrx01-CDS.fa.gz)`
4. unzip CDS fasta file using `$gunzip Potrx01-CDS.fa`
5. generate primer3 input file using `$python3 primer3_intput_design_T89.py`
    1. note: depending on the layout and format of your marker gene input file, one should modify this file 

## Primer3

1. install primer3 command line version using `$conda install -c bioconda primer3`
2. run primer3: `$primer3_core < primer3_input_full.txt > primer3_output.txt`

**Criteria taken care of in this step:** 

- probe size = 25 nucleotides
- GC range for LHS probe = 44% - 72%
- max unknown nucleotides = 1
- maximum length of mononucleotide repeats = 5
- n probes generated per sequence = 35 (to be filtered down in later steps)

## Generate probe pairs

1. run `$python3 generate_probe_pairs.py > possible_probe_pairs.txt.`

**output:** 

- preliminary list of primer pairs including:
    1. sequence ID 
    2. sequence template 
    3. probe pairs sorted based on start site, and their information: 
        1. LHS & RHS probe ID
        2. probe pair start and end site 
        3. LHS & RHS probe sequence, including handles 
        4. LHS & RHS probe GC content 
- a fasta file containing the ************************hybridising************************ all probe pairs sequences sequences pair, RHS and LHS combined (”probe_pairs_hyb_T89.fasta”)
- a fasta file for each gene containing the ************************hybridising************************ sequences for all probes, RHS and LHS separate
- a txt file for each gene containing the **********full********** probe sequences for each gene, in IDT OligoAnalyzer batch input format
- NOTE: comment out the writing functions which you do not need to avoid cluttering

**criteria taken care of:**

- LHS probe must end at T
- RHS probe must start right after the LHS probe
- RHS probe must be within GC range 44%-72%
- RHS probe must fit on the sequence template
- LHS and RHS hybridising sequences must be ligated to their corresponding probe handles

## Off target hybridisation (BLAST)

1. install command line BLAST following the [NCBI instructions](https://www.ncbi.nlm.nih.gov/books/NBK52640/)
2. build a blast database `$makeblastdb -in Potrx01-CDS.fasta -dbtype nucl -parse_seqids -out db/Potrx-CDS-db`
3. copy probe_pairs_hyb_T89.fasta to your blast folder
4. blast the probe_pairs_hyb_T89.fasta against the database `$blastn -db db/Potrx-CDS-db -query probe_pairs_hyb_comb_T89.fasta > probes_pairs_comb_target_specificity_CDS.txt -outfmt "6 qseqid sseqid pident”`
    - note: include `-task blastn-short` when blasting sequences < 30 nucleotides (i.e. when blasting RHS and LHS invidiually)
    - note: the output contains probe ID, sequence ID and percentage identity
    - note: with standard blast threshold (E value = 0.05), the lowest percentage identity included in the hits is 88%
5. clean up blast output file using target_specificity_trim.py
    1. keep only match for highest transcript variant, remove duplicate matches to the same gene different transcript variant 
    2. output “trimmed_paired_probes_target_specificity_CDS.txt” 

## Probe overlap correction

1. run `$python3 select_probe_pairs.py > selected_probes.txt`

**output** 

- final probe pairs

**criteria taken care of**

- get rid of probes which have off target hybridisation
- keep probes only if the binding sites do not overlap
- if probe pairs > 3, then do not accumulate more probes
- (optional: remove sequences for which no probe pairs could be generated)

## To be included in the future

1. assessing hairpin structure 
2. assessing cross-probe hybridisation
