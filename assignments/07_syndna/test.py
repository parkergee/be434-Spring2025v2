#!/usr/bin/env python3
"""tests for syndna.py"""

import os
import random
import re
import string
from subprocess import getstatusoutput
from Bio import SeqIO
from numpy import mean
from itertools import chain
from syndna import gc_fraction

prg = './syndna.py'

# --------------------------------------------------
def GC(sequence):
    return 100 * gc_fraction(sequence, ambiguous="ignore")

# --------------------------------------------------
def random_string():
    """generate a random string"""

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# --------------------------------------------------
def test_exists():
    """usage"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput('{} {}'.format(prg, flag))
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_seqtype():
    """die on bad seqtype"""

    bad = random_string()
    rv, out = getstatusoutput(f'{prg} -t {bad}')
    assert rv != 0
    assert re.match('usage:', out, re.I)

# --------------------------------------------------
def test_bad_pctgc():
    """die on bad pctgc"""

    bad = random.randint(1, 10)
    rv, out = getstatusoutput(f'{prg} -p {bad}')
    assert rv != 0
    assert re.match('usage:', out, re.I)
    assert re.search(f'--pctgc "{float(bad)}" must be between 0 and 1', out)


# --------------------------------------------------
def test_defaults():
    """runs on good input"""

    out_file = 'out.fa'
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(prg)
        assert rv == 0
        assert out == f'Done, wrote 10 DNA sequences to "{out_file}".'
        assert os.path.isfile(out_file)

        # correct number of seqs
        seqs = list(SeqIO.parse(out_file, 'fasta'))
        assert len(seqs) == 10

        # the lengths are in the correct range
        seq_lens = list(map(lambda seq: len(seq.seq), seqs))
        assert max(seq_lens) <= 75
        assert min(seq_lens) >= 50

        # bases are correct
        bases = ''.join(
            sorted(
                set(chain(map(lambda seq: ''.join(sorted(set(seq.seq))),
                              seqs)))))
        assert bases == 'ACGT'

        # the pct GC is about right
        gc = list(map(lambda seq: gc_fraction(seq.seq) / 100, seqs))
        assert .47 <= mean(gc) <= .53

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)

# --------------------------------------------------
def test_options():
    """runs on good input"""

    out_file = random_string() + '.fasta'
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        min_len = random.randint(50, 99)
        max_len = random.randint(100, 150)
        num_seqs = random.randint(100, 150)
        pct_gc = random.random()
        cmd = (f'{prg} -m {min_len} -x {max_len} -o {out_file} '
               f'-n {num_seqs} -t rna -p {pct_gc:.02f} -s 1')
        rv, out = getstatusoutput(cmd)

        assert rv == 0
        assert out == f'Done, wrote {num_seqs} RNA sequences to "{out_file}".'
        assert os.path.isfile(out_file)

        # correct number of seqs
        seqs = list(SeqIO.parse(out_file, 'fasta'))
        assert len(seqs) == num_seqs

        # the lengths are in the correct range
        seq_lens = list(map(lambda seq: len(seq.seq), seqs))
        assert max(seq_lens) <= max_len
        assert min(seq_lens) >= min_len

        # bases are correct
        bases = set(''.join(
            map(lambda seq: ''.join(sorted(set(seq.seq))), seqs)))
        assert bases == set('ACGU')

        # the pct GC is about right
        gc = list(map(lambda seq: gc_fraction(seq.seq) / 100, seqs))
        assert pct_gc - .3 <= mean(gc) <= pct_gc + .3

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)