#!/usr/bin/env python3
"""
Author : parker <Add your email>
Date   : 2025-05-02
Purpose: count gc
"""

import argparse
import sys
import os
from operator import itemgetter


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='count gc',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(#'-s',
                        #'--sequence',
                        'sequence',
                        help='Input sequence file',
                        metavar='FILE',
                        nargs='*', #how to do without args
                        type=argparse.FileType('rt'),
                        default= [sys.stdin]
                        )

    args = parser.parse_args()


    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    gc = 0
    at = 0
    unknown = 0
    results = []
    seq_id = ''
    total = 0
    seq = args.sequence
    for fh in seq:
        for line in fh:
            if line.startswith('>'):
                if(total) > 0:
                    percentage = (gc)/(total)*100
                    result = percentage
                    #print(seq_id,result)
                    results.append((seq_id, result))
                    gc = at = unknown = total = 0
                seq_id = line.strip()[1:]
            else:
                nuc_str = list(line.strip().upper())
                for n in nuc_str:
                    total += 1
                    if n == 'G' or n == 'C' :
                        gc += 1
                    elif n == 'A' or n == 'T':
                        at += 1
                    else:
                        unknown += 1
        result = (gc)/(total)*100
        results.append((seq_id, result))
        #print(results)
        final = ('',-1)
        for result in results:
            if result[1] > final[1]:
                final = result
            #print(result[1], final[1])
        print("{} {:.6f}".format(*final))

# --------------------------------------------------
if __name__ == '__main__':
    main()
