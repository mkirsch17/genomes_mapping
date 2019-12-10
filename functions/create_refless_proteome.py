from functions.query_refless import query_refless
from constants import REFLESS_PROTEOME_LOG, CLUSTERS_DF_PATH, REF_GENOME_ID

import pandas as pd

def create_refless_proteome():

    log = open(REFLESS_PROTEOME_LOG, 'w', buffering=1)

    log.write('Importing cluster data\n')

    # Import dataframe of clusters
    clusters_df = pd.read_csv(CLUSTERS_DF_PATH)

    # Names of all clusters
    cluster_names_all = set(clusters_df.cluster.tolist())

    # Clusters that contain a protein belonging to reference genome
    clusters_with_ref_df = clusters_df.loc[clusters_df.genome == REF_GENOME_ID + '_']
    cluster_names_with_ref  = set(clusters_with_ref_df.cluster.tolist())

    # Clusters that don't contain a protein belonging to reference genome ("refless" clusters)
    cluster_names_refless = list(cluster_names_all.difference(cluster_names_with_ref))
    clusters_refless_df = clusters_df.loc[clusters_df.cluster.isin(cluster_names_refless)]

    # Proteins belonging to refless clusters ("refless" proteins)
    protein_names_refless = list(set(clusters_refless_df.gene.tolist()))

    # This function queries the proteome for all refless proteins and generates the refless proteome
    query_refless(protein_names_refless)

    log.write('Done')
