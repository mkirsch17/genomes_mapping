from constants import RESCUE_REFLESS_LOG, REF_GENOME_ID, GENOMES_DIR, BLAST_DB_PATH, REFLESS_PROTEOME_PATH, BLAST_RESULTS_PATH, THRESHOLD, STRANDED_LIST_PATH

import os
import pandas as pd

def rescue_refless():

    log = open(RESCUE_REFLESS_LOG, 'w', buffering=1)

    log.write('Generating BLAST database from reference genome\n')

    # Generate BLAST database from reference genome
    os.system('makeblastdb -in %s%s/%s_protein.faa -dbtype prot -db_name %s' % (GENOMES_DIR, REF_GENOME_ID, REF_GENOME_ID, BLAST_DB_PATH))

    log.write('Performing BLAST search against reference genome\n')

    # Perform BLAST search
    os.system('blastp -query %s -db %s "6 qseqid sseqid pident qcovs" -max_target_seqs 1 > %s' % (REFLESS_PROTEOME_PATH, BLAST_DB_PATH, BLAST_RESULTS_PATH))

    log.write('Parsing BLAST results\n')

    # Read in BLAST results
    results_df = pd.read_csv(BLAST_RESULTS_PATH, sep='\t', header=None)
    results_df.columns = ['query_id', 'subject_id', 'perc_identity', 'coverage']

    # Proteins successfully rescued (percent identity and coverage >= set threshold)
    rescued_df = results_df.loc[(results_df.perc_identity >= THRESHOLD) & (results_df.coverage >= THRESHOLD)]
    protein_names_rescued = set(rescued_df.query_id.tolist())

    # All protein names, and protein names failed to be rescued ("stranded")
    protein_names_all = set(results_df.query_id.tolist()) 
    protein_names_stranded = list(protein_names_all.difference(protein_names_rescued))

    log.write('Writing stranded proteins to %s\n' % STRANDED_LIST_PATH)

    # Write stranded proteins to file
    with open(STRANDED_LIST_PATH, 'w') as filename:
        filename.write('\n'.join(protein_names_stranded))
    
    log.write('Done')
