# This function is currently not integrated into the pipeline, and is meant to be used as a one-off script to assist in identifying outlier genomes. This is not a robust approach to such a problem, and the results should be interpreted cautiously. Methods below:

# This function takes the total_list.csv matrix, which indicates, for each cluster, whether the genome has a protein belonging to such a cluster. For each genome, it's presence in each cluster is compared to that of all other genomes. If they match, i.e. Genome and Genome B both contain a protein in Cluster 1, a score of 1 is assigned. This is done for each cluster (containing a certain number of proteins) and pairwise comparisons are made for all genomes. The result is a matrix where each cell contains the number of clusters the two genomes "agree" on, i.e. whether the both contain or both do not contain a protein for a given cluster.

# To interpret this result, two options are suggested:
# 1) Use MORPHEUS (online tool by The Broad Institute) to visualize the output as a heatmap.
# 2) Sum the rows/columns to obtain a global similarity score for each genome.



# Import modules
import pandas as pd
import numpy as np
import collections

# Paths to files
TOTAL_LIST_PATH = './results/total_list.csv'
CLUSTERS_DF_PATH = './results/clusters.csv'

# Only consider clusters containing this many proteins (default: 50)
cluster_size = 50



# Function definition
def identify_outliers(TOTAL_LIST_PATH, CLUSTERS_DF_PATH, cluster_size):

    # Import total list matrix
    df_matrix = pd.read_csv(TOTAL_LIST_PATH)

    # Import clusters
    df_clusters = pd.read_csv(CLUSTERS_DF_PATH)

    # Names of clusters containing certain number of proteins
    cluster_names = df_clusters.cluster.tolist()
    cluster_counts = collections.Counter(cluster_names)
    clusters_sizable = [cluster for cluster in cluster_counts.keys() if cluster_counts[cluster] >= cluster_size]

    # Only consider sizable clusters, set index to cluster names
    df_matrix = df_matrix.loc[df_matrix.gene.isin(clusters_sizable)]
    df_matrix.set_index('gene', inplace=True)

    # Lists of clusters and genomes
    cluster_names = df_matrix.index.tolist()
    genome_names = df_matrix.columns.tolist()

    # We only care whether the genome has a protein in a cluster or not, so change all values >1 to 1
    max_value = df_matrix.max().max()
    df_matrix.replace(range(2, max_value+1), 1, inplace=True)

    # Initialize matrix to contain similarity scores
    scores_matrix = np.zeros((len(genome_names), len(genome_names)))

    # Counter to indicate matrix row 
    genome_count = 0

    # Make pairwise comparison for each genome
    # Could make this 2x faster, since it does pairwise calculations and the operation is commutative
    for genome in genome_names:

        print(genome_count)

        # Counter to indicate matrix column
        comp_genome_count = 0

        for comp_genome in genome_names:
            
            # If self-comparison, set score to maximum possible
            if genome == comp_genome:
                scores_matrix[genome_count, comp_genome_count] = len(cluster_names)

            # Make genome comparison, add score to matrix
            else:
                similarity_score = sum(df_matrix[genome] == df_matrix[comp_genome])
                scores_matrix[genome_count, comp_genome_count] = similarity_score

            # Add to counter
            comp_genome_count += 1

        # Add to counter
        genome_count += 1


    # Convert matrix into dataframe, add column and index names
    df_scores = pd.DataFrame(scores_matrix)
    df_scores.columns = genome_names
    df_scores.index = genome_names
    df_scores.to_csv('./genome_similarities.csv')



# Call function
identify_outliers(TOTAL_LIST_PATH, CLUSTERS_DF_PATH, cluster_size)

