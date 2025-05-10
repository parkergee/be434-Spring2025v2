
#!/usr/bin/env python3
"""
Author : parker
Purpose: Creating synthetic DNA/RNA sequences
"""

import argparse
import random

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create synthetic sequences',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-o',
                       '--outfile',
                       help='Output filename',
                       metavar='str',
                       type=str,
                       default='out.fa')

    parser.add_argument('-t',
                       '--seqtype',
                       help='DNA or RNA',
                       metavar='str',
                       type=str,
                       default='dna',
                       choices=['dna', 'rna'])

    parser.add_argument('-n',
                       '--numseqs',
                       help='Number of sequences to create',
                       metavar='int',
                       type=int,
                       default=10)

    parser.add_argument('-m',
                       '--minlen',
                       help='Minimum length',
                       metavar='int',
                       type=int,
                       default=50)

    parser.add_argument('-x',
                       '--maxlen',
                       help='Maximum length',
                       metavar='int',
                       type=int,
                       default=75)

    parser.add_argument('-p',
                       '--pctgc',
                       help='Percent GC',
                       metavar='float',
                       type=float,
                       default=0.5)

    parser.add_argument('-s',
                       '--seed',
                       help='Random seed',
                       metavar='int',
                       type=int,
                       default=None)

    args = parser.parse_args()

    if not 0 <= args.pctgc <= 1:
        parser.error(f'--pctgc "{args.pctgc}" must be between 0 and 1')

    args.seqtype = args.seqtype.lower()
    return args
#validate good sequence
def validate_sequence(seq, seq_type):
    """Validate that sequence contains only valid bases"""
    valid_bases = {'dna': set('ACGT'), 'rna': set('ACGU')}
    return all(base in valid_bases[seq_type.lower()] for base in seq.upper())

def create_pool(pctgc, max_len, seq_type):
    """Create the pool of bases"""
    
    if seq_type.lower() not in ['dna', 'rna']:
        raise ValueError(f'Invalid sequence type: {seq_type}')
        
    t_or_u = 'T' if seq_type.lower() == 'dna' else 'U'
    num_gc = int(pctgc * max_len / 2)  # Split GC between G and C
    num_at = int((1 - pctgc) * max_len / 2)  # Split AT/AU between A and T/U
    
    # Create the pool with the correct proportions
    pool = ('A' * num_at + 'C' * num_gc + 'G' * num_gc + t_or_u * num_at)
    
    # Add any remaining bases to maintain proportions
    remaining = max_len - len(pool)
    if remaining > 0:
        gc_remaining = int(pctgc * remaining / 2)
        at_remaining = remaining - 2 * gc_remaining
        pool += ('A' * at_remaining + 'C' * gc_remaining + 
                'G' * gc_remaining + t_or_u * at_remaining)
    
    return pool * 2  # Double the pool size to ensure enough bases for sampling

def main():
    """Make synthetic sequences"""

    args = get_args()
    random.seed(args.seed)
    pool = create_pool(args.pctgc, args.maxlen, args.seqtype)

    with open(args.outfile, 'wt') as out_fh:
        for i in range(args.numseqs):
            seq_len = random.randint(args.minlen, args.maxlen)
            seq = ''.join(random.sample(pool, seq_len))
            out_fh.write(f'>{i+1}\n{seq}\n')

    print(f'Done, wrote {args.numseqs} {args.seqtype.upper()} sequences to "{args.outfile}".')

if __name__ == '__main__':
    main()
