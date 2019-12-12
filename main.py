from functions.set_enviroment import set_enviroment
from functions.download_genomes import download_genomes
from functions.create_proteome import create_proteome
from functions.create_total_list_of_genes import create_total_list_of_genes
from functions.create_refless_proteome import create_refless_proteome
from functions.rescue_refless import rescue_refless
from functions.make_summary import make_summary

from constants import LOG_PATH, DOWNLOADING_LOG, PROTEOME_LOG, TOTAL_LIST_LOG, REFLESS_PROTEOME_LOG, RESCUE_REFLESS_LOG

import os

set_enviroment()
log = open(LOG_PATH, 'w', buffering=1)

try:
    '''
    log.write('Downloading genomes. More details in {}\n'.format(DOWNLOADING_LOG))
    download_genomes()

    log.write('Trying to create proteome. More information in {}\n'.format(PROTEOME_LOG))
    create_proteome()

    log.write('Trying to create total list of genes. More information in {}\n'.format(TOTAL_LIST_LOG))
    create_total_list_of_genes()

    log.write('Trying to create proteome of refless genes. More information in {}\n'.format(REFLESS_PROTEOME_LOG))
    create_refless_proteome()
    
    log.write('Trying to perform rescue process for refless genes. More information in {}\n'.format(RESCUE_REFLESS_LOG))
    rescue_refless()
    
    log.write('Making summary\n')
    make_summary()
    log.write('All done!')
    '''

    # Remove temp file and /tmp files
    os.system('rm ./temp')
    os.system('rm -r ./tmp/')

finally:
    log.close()
