from constants import REFLESS_PROTEOME_LOG, PROTEOME_PATH, REFLESS_PROTEOME_PATH

import os
import math
import re

# This function queries the proteome for all refless proteins and generates the refless proteome
def query_refless(protein_names_refless):

    log = open(REFLESS_PROTEOME_LOG, 'w', buffering=1)

    log.write('Preparing to query refless proteins\n')

    # Find all genomes that contain refless proteins, only need to query these
    genomes_refless = list(set([protein.split('genome:')[-1][:-1] for protein in protein_names_refless]))

    # Maximum number of protein IDs (patterns) per grep (manually determined)
    max_proteins_per_grep = 2000

    # Generate an individual fasta file of refless proteins for each genome
    for genome in genomes_refless:

        log.write('Querying refless proteins from %s\n' % genome)

        # Refless proteins belonging to current genome
        genome_proteins_refless = [protein for protein in protein_names_refless if genome in protein]

        # Determine how many greps must be performed
        num_greps = math.ceil(len(genome_proteins_refless) / max_proteins_per_grep)

        # Generate fasta file of all proteins belong to current genome
        os.system("grep -F -A 1 '%s' %s > ./tmp/%s.fa" % (genome, PROTEOME_PATH, genome))

        # For each batch of refless proteins, perform grep against current genome fasta 
        for loop in list(range(0, num_greps)):

            # Start and end indices
            start = loop * max_proteins_per_grep
            end = (loop + 1) * max_proteins_per_grep

            # If the end index goes beyond the list length, just go until the end
            if end > len(genome_proteins_refless):
                current_proteins = genome_proteins_refless[start:]

            # Otherwise, use the end index
            else:
                current_proteins = genome_proteins_refless[start:end]

            # Each protein should be preceded with '-e' flag
            grep_pattern = '-e ' + ' -e '.join(current_proteins)

            # Do some magic to avoid pattern being interpreted as regex
            rep = {'[': '[[]', ']': '[]]'}
            rep = dict((re.escape(k), v) for k, v in rep.items())
            pattern = re.compile('|'.join(rep.keys()))
            grep_pattern = pattern.sub(lambda m: rep[re.escape(m.group(0))], grep_pattern)
            grep_pattern = grep_pattern.replace('[[]', '[\[]').replace('[]]', '[\]]')

            # Query current genome for its refless proteins, save to fasta file (with suffix indicating which "batch" it contains)
            os.system("grep -A 1 %s ./tmp/%s.fa > ./tmp/%s_refless_%s.fa" % (grep_pattern, genome, genome, loop))

        # Remove genome's fasta file
        os.system('rm ./tmp/%s.fa' % genome)

    log.write('Generating refless proteome\n')

    # Concatenate all genomes' refless proteins into refless proteome
    os.system('cat ./tmp/*_refless*.fa > ./tmp/refless_proteome_tmp.fa')

    # Remove individual genomes' refless proteins files
    os.system('rm ./tmp/*__refless*.fa')

    # grep -A 1 generates lines of dashes: remove them and generate new file
    os.system("grep -v '^--' ./tmp/refless_proteome_tmp.fa > ./tmp/refless_proteome_clean.fa")

    # Remove temp proteome, move cleaned one to proper location
    os.system('rm ./tmp/refless_proteome_tmp.fa')
    os.system('mv ./tmp/refless_proteome_clean.fa %s' % REFLESS_PROTEOME_PATH)


