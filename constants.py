FTP_LINK = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/'
ORGANISM = 'Escherichia_coli'  # TODO: make a parameter to generalize the pipeline
REF_GENOME_ID = 'GCF_000005845.2_ASM584v2'

CD_HIT_PATH = 'cd-hit'  # path to a tool iteself. If it is not in $PATH variable, please, set it

GENOMES_DIR = './data/'
TEMP_PATH = './temp'
PROTEOME_PATH = './results/proteome.faa'
GENES_INFO_PATH = './results/genes_info.tsv'
CLUSTERS_INFO = './results/cluster_info.json'
TOTAL_LIST_PATH = './results/total_list.csv'
CLUSTERS_DF_PATH = './results/clusters.csv'
REFLESS_PROTEOME_PATH = './results/proteome_refless.faa'
SUMMARY = './results/summary.txt'

LOG_PATH = './logs/pipeline.log'
DOWNLOADING_LOG = './logs/downloading.log'
PROTEOME_LOG = './logs/proteome.log'
TOTAL_LIST_LOG = './logs/total_list.log'
REFLESS_PROTEOME_LOG = './logs/proteome_refless.log'

THRESHOLD = 90
