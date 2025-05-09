#!/usr/bin/env python3
"""
Author : parker <Add your email>
Date   : 2025-05-06
Purpose: test
"""

import argparse
import os
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='test',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(#'-s',
                        #'--sequence',
                        'file',
                        help='Input sequence file',
                        metavar='FILE',
                        nargs='+', #how to do without args
                        type=argparse.FileType('rt'),
                        default= [sys.stdin]
                        )

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar= 'str',
                        type=str, 
                        default='')


    return parser.parse_args()

# --------------------------------------------------
def main():
    """Transcribe DNA into RNA for mult file."""
    num_seq = 0
    num_files = 0
    args = get_args()
    directory = args.out_dir
    try:
        os.mkdir(directory)
        #print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    sys.stdout
    #dna = args.file.read().strip().upper()
    f = args.file
    
    for fh in f:
        name = os.path.basename(fh.name)
        out_fh = open(directory+'/'+name, 'wt') if args.out_dir else sys.stdout
        num_files += 1
        for line in fh:
            dna = line.strip().upper()
            if dna: #if not empty
                num_seq += 1
                out_fh.write(dna.replace('T', 'U')+'\n')
                #print(dna.replace('T', 'U'))
        out_fh.close()
    plural = 'file' if num_files == 1 else 'files'
    pluralseq = 'sequence' if num_seq == 1 else 'sequences'
    print(f'Done, wrote {num_seq} {pluralseq} in {num_files} {plural} to directory "{args.out_dir}".')

# --------------------------------------------------
if __name__ == '__main__':
    main()
