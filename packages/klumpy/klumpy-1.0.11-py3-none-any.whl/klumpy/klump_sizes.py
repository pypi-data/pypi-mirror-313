#
# Copyright 2024, Giovanni Madrigal <gm33@illinois.edu>
#
# This file is part of Klumpy.
#
# Klumpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Klumpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Klumpy. If not, see <http://www.gnu.org/licenses/>.
#


import gzip
import os
import sys
from  .Classes import Seq_Record

def check_args(args):
    """verify that the arguments are legal and able to be used"""

    if args.fasta == None:
        msg = "No fasta input. Use --fasta"
        sys.exit(msg)
    assert os.path.isfile(args.fasta), f"Could not find {args.fasta}"
    assert args.ksize > 0,              "--ksize must be greater than 0"

    return args.fasta, args.ksize

########################
### Parsing functions ###
########################


def load_fasta_file(fasta_file: str, ksize: int):
    """read fasta records"""

    records = []

    #
    # Read a gzipped file without any intervention.
    #
    if fasta_file.endswith(".gz"):
        fh = gzip.open(fasta_file, 'rt')
    else:
        fh = open(fasta_file, 'r')

    seq = ''
    id  = None

    for line in fh:
        # skip empty or commented lines
        if len(line) == 0 or line.startswith('#'):
            continue
        line = line.strip()
        if line.startswith('>'):
            # for the 1st record
            if seq == '':
                id = line[1:].split(" ")[0]
                continue
            else:
                if len(seq) >= ksize:
                    records.append(Seq_Record(id, seq))
                seq = ''
                id  = line[1:].split(' ')[0]
        else:
            seq += line.upper()

    # for the last record
    if len(seq) >= ksize:
        records.append(Seq_Record(id, seq))

    fh.close()

    return records


########################
### Kmer functions ###
########################


def print_to_console(records: list, ksize: int):
    """for each fasta record, print the kmer"""

    for record in records:
        seq_id    = record.seq_name
        num_kmers = record.seq_length - ksize + 1
        print(f"{seq_id} length {record.seq_length}: Klump size of {num_kmers} k-mers")


def Klump_Sizes(args):
    """Main entry point to this small subprogram"""
    # get arguments

    fasta, ksize = check_args(args)

    # load sequences
    records      = load_fasta_file(fasta, ksize)

    print_to_console(records, ksize)
