import os


def set_enviroment():
    """Create subdirectories needed for the other steps of the pipeline.

    Directory tree after work of the pipeline will look like this (except for .py files):
    .
    ├── tmp - folder with temporary results, will be deleted upon completion 
    ├── cd_hit - folder with cd-hit results
    ├── data - folder where all the downloaded data will be saved
    │   ├── assembly_summary.txt - table with all organism assemblies from refseq
    │   ├── GCF_000005845.2_ASM584v2 - folder with files for that assembly
    │   │   ├── GCF_000005845.2_ASM584v2_feature_table.txt - from NCBI
    │   │   ├── GCF_000005845.2_ASM584v2_genomic.fna - from NCBI
    │   │   ├── GCF_000005845.2_ASM584v2_protein.faa - from NCBI
    │   │   └── GCF_000005845.2_ASM584v2_protein.gpff - from NCBI
    │   ├── GCF_000006665.1_ASM666v1
    │   ...
    ├── logs
    │   ├── alignment.log - log of align_to_database()
    │   ├── downloading.log - log of download_genomes()
    │   └── pipeline.log - general log
    ├── plots - folder with graphs
    └── results
        ├── proteome.faa - fasta file with all the protein coding genes from all the genomes with extra information
        ├── genes_info.tsv - data frame with following format (tab-separated):
        │       gene    info
        │       gene_1[genome:genome_1] info_1
        │       ...
        │       gene_n[genome:genome_n] info_n
        │   Information about genes is extracted from fasta header. Genome id is appended to each gene
        ├── cluster_info.json - Counter in .json format for each cluster. Counts information about genes in the cluster
        │   so you could understand, what the cluster contains.
        ├── total_list.csv - table with clusters in rows and genomes in columns. Number on the intersection means, how
        │   many genes from this cluster the genome contains.
        ├── clusters.csv - data frame with following columns:
        │   1. 'cluster' — cluster of a sequence
        │   2. 'representative' — boolean variable, which indicates, if the given sequence is representative
        │   in the cluster
        │   3. 'gene' — name of the sequence from fasta header with appended genome id
        │   4. 'length' — length of the gene's sequence
        │   5. 'identity' — identity of a sequence to representative sequence of its cluster
        │   6. 'name' — name of the sequence from fasta header without appended genome id
        │   7. 'genome' — genome id from fasta header
        │   8. 'info' — information about gene from its fasta header
        └── summary.txt - summary about results

    """
    os.makedirs('tmp', exist_ok=True)
    os.makedirs('cd_hit', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    os.makedirs('results', exist_ok=True)
