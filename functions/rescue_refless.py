from constants import RESCUE_REFLESS_LOG, REF_GENOME_ID, GENOMES_DIR, BLAST_DB_PATH, REFLESS_PROTEOME_PATH, BLAST_RESULTS_PATH, THRESHOLD, STRANDED_LIST_PATH, CLUSTERS_DF_PATH, RESCUED_LIST_PATH

import os
import pandas as pd

def rescue_refless():

    log = open(RESCUE_REFLESS_LOG, 'w', buffering=1)

    log.write('Generating BLAST database from reference genome\n')

    # Generate BLAST database from reference genome
    os.system('makeblastdb -in %s%s/%s_protein.faa -dbtype prot -out %s' % (GENOMES_DIR, REF_GENOME_ID, REF_GENOME_ID, BLAST_DB_PATH))

    log.write('Performing BLAST search against reference genome\n')

    # Perform BLAST search
    os.system('blastp -query %s -db %s -outfmt "6 qseqid sseqid pident qcovs" -max_target_seqs 1 > %s' % (REFLESS_PROTEOME_PATH, BLAST_DB_PATH, BLAST_RESULTS_PATH))

    log.write('Parsing BLAST results\n')

    # Read in BLAST results
    results_df = pd.read_csv(BLAST_RESULTS_PATH, sep='\t', header=None)
    results_df.columns = ['query_id', 'subject_id', 'perc_identity', 'coverage']

    # Proteins successfully rescued (percent identity and coverage >= set threshold)
    rescued_df = results_df.loc[(results_df.perc_identity >= THRESHOLD) & (results_df.coverage >= THRESHOLD)].copy()
    protein_names_rescued = set(rescued_df.query_id.tolist())

    # All protein names, and protein names failed to be rescued ("stranded")
    protein_names_all = set(results_df.query_id.tolist()) 
    protein_names_stranded = list(protein_names_all.difference(protein_names_rescued))

    log.write('Writing stranded proteins to %s\n' % STRANDED_LIST_PATH)

    # Write stranded proteins to file
    with open(STRANDED_LIST_PATH, 'w') as filename:
        filename.write('\n'.join(protein_names_stranded))

    log.write('Writing rescued proteins to %s\n' % STRANDED_LIST_PATH)

    # Determine which clusters rescued proteins "belong to" (i.e. which clusters their rescuers belong to)

    # Subject IDs of queried proteins that were rescued ("rescuers")
    protein_names_rescuers = rescued_df.subject_id.tolist()

    # Import cluster data, only consider proteins belonging to reference genome (all rescuers belong to reference genome)
    clusters_df = pd.read_csv(CLUSTERS_DF_PATH)
    clusters_ref_genome_df = clusters_df.loc[clusters_df.genome == REF_GENOME_ID + '_']

    # Dataframe only containing rescuers
    clusters_rescuers_df = clusters_ref_genome_df.loc[clusters_ref_genome_df.name.isin(protein_names_rescuers)]

    # Create dictionary of rescuer: cluster
    clusters_rescuers_dict = clusters_rescuers_df.set_index('name').cluster.to_dict()

    # Create column of clusters for rescued proteins
    rescued_clusters = [clusters_rescuers_dict[protein] for protein in protein_names_rescuers]
    rescued_df['cluster'] = rescued_clusters

    # Format dataframe for export, save
    rescued_df_save = rescued_df.loc[:, ['query_id', 'cluster']].copy()
    rescued_df_save = rescued_df_save.loc[~rescued_df_save.duplicated()]
    rescued_df_save.to_csv(RESCUED_LIST_PATH, index=False)

    log.write('Done')

