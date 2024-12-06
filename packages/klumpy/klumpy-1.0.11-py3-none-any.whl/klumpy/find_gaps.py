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
import sys
import os
from   collections import defaultdict
from  .Classes     import Seq_Record

def check_args(args):
    """verify that there is a file to parse"""

    if args.fasta == None:
        msg = "--fasta file required for find_gaps"
        sys.exit(msg)
    assert os.path.isfile(args.fasta), f"Could not find {args.fasta}"

    return args.fasta


def load_fasta_file(fasta_file: str):
    """read fasta records"""

    records = []

    # Read a gzipped file without any intervention.
    if fasta_file.endswith(".gz"):
        fh = gzip.open(fasta_file, 'rt')
    else:
        fh = open(fasta_file, "r")

    seq = ""
    id  = None

    for line in fh:
        # skip empty or commented lines
        if len(line) == 0 or line.startswith('#'):
            continue
        line = line.strip()
        if line[0] == '>':
            # for the 1st record
            if seq == "":
                id = line[1:].split(" ")[0]
                continue
            else:
                records.append(Seq_Record(id, seq))
                seq = ""
                id = line[1:].split(" ")[0]
        else:
            seq += line.upper()

    # for the last record
    if len(seq) > 0:
        records.append(Seq_Record(id, seq))

    fh.close()

    return records


def get_gaps(records: list, fasta_file: str):
    """get gaps from inputted sequences"""

    seq_gaps = defaultdict(list)

    # initialize some trackers
    start   = float("inf")
    end     = -float("inf")
    gap_cnt = 0

    for seq_record in records:
        # will make 1-index for users
        for pos, nuc in enumerate(seq_record.seq, start = 1):
            if nuc.upper() != "N":
                if start != float("inf"):
                    gap = (start, end)
                    seq_gaps[seq_record.seq_name].append(gap)
                    gap_cnt += 1
                    start    = float("inf")
                    end      = -float("inf")
                else:
                    continue
            elif nuc.upper() == "N":
                start = min(pos, start) # will stay as first num
                end   = max(pos, end)
                #if it is the last position
                # should never happen but still check
                if pos == seq_record.seq_length:
                    gap = (start, end)
                    seq_gaps[seq_record.seq_name].append(gap)
                    gap_cnt += 1

    if gap_cnt == 0:
        sys.exit(f"Did not find any gaps in {os.path.basename(fasta_file)}")
    else:
        print(f"Found {gap_cnt} gaps")

    return seq_gaps

def write_output(seq_gaps: dict, fasta_file: str):
    """write to tsv"""

    if '.gz' in fasta_file:
        filename = os.path.basename(fasta_file).split(".")[:-2]
    else:
        filename = os.path.basename(fasta_file).split(".")[:-1]

    filename = ".".join([text for text in filename])
    outfile  = f"{filename}_gaps.tsv"

    with open(outfile, "w") as out:
        out.write(f"Chrom\tStart\tEnd\n")
        for seq_id, gaps in seq_gaps.items():
            for gap in gaps:
                out.write(f"{seq_id}\t{gap[0]}\t{gap[1]}\n")
    
def Find_Gaps(args):
    """Find the gaps in the provided fasta file"""

    # get arguments
    fasta_file = check_args(args)

    #get sequences
    records   = load_fasta_file(fasta_file)

    #get gaps
    seq_gaps  = get_gaps(records, fasta_file)

    #write output
    write_output(seq_gaps, fasta_file)

