#!/usr/bin/env python3
"""
Author : parker <Add your email>
Date   : 2025-05-06
Purpose: test
"""

import argparse
import random
import biopython
import numpy
import os
import sys

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description=' Creating synthetic DNA/RNA sequences',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


    parser.add_argument('-t',
                        '--seqtype',
                        help='The sequence type, either dna or rna.',
                        metavar='str',
                        type=str,
                        default='dna')

    parser.add_argument('-n',
                        '--numseqs',
                        help='The number of sequences to generate.',
                        metavar='int',
                        type=int,
                        default=10)
    parser.add_argument('-m',
                        '--minlen',
                        help='The minimum length of the sequences.',
                        metavar='int',
                        type=int,
                        default=50)
    parser.add_argument('-x',
                        '--maxlen',
                        help='The maximum length of the sequences.',
                        metavar='int',
                        type=int,
                        default=75)
  
    parser.add_argument('-p',
                        '--pctgc',
                        help='The percentage of GC content.',
                        metavar='float',
                        type=float,
                        default=0.5)

    parser.add_argument('-s',
                        '--seed',
                        help='The random seed.',
                        metavar='int',
                        type=int,
                        default=None) 

    parser.add_argument('-o',
                        '--outfile',
                        help='Output File',
                        metavar= 'str',
                        type=argparse.FileType('wt'), 
                        default='out.fa')
    
    args = parser.parse_args()
    if not 0 <= args.pctgc <= 1:
                        parser.error(f'--pctgc "{args.pctgc}" must be between 0 and 1')

    return parser.parse_args()



# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    random.seed(args.seed)
    pool = create_pool(args.pctgc, args.maxlen, args.seqtype)
    max_len = args.maxlen
    min_len = args.minlen
    seq_len = random.randint(min_len, max_len)
    seq_type = args.seqtype
    
##--------------------------------------------------
def create_pool(pctgc, max_len, seq_type):
        """Create a pool of nucleotides based on GC content and sequence type.""" t_or_u = 'T' if seqtype == 'dna' else 'U'
         num_gc = int((pctgc / 2)*max_len)
    for fh in f:
        name = os.path.basename(fh.name)
        out_fh = open(directory+'/'+name, 'wt') if args.out_dir else sys.stdout
        num_files += 1
        for line in fh:
            dna = line.strip().upper()
            if dna: #if not empty
                num_seq += 1
                random.sample(pool,seq_len)
                out_fh.write('\n'+seq_len)
                #print(dna.replace('T', 'U'))
        out_fh.close()
                       




# --------------------------------------------------
if __name__ == '__main__':
    main()
