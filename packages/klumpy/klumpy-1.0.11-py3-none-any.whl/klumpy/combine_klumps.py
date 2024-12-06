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

def check_args(args):
    """verify that the input args are legal and safe to process"""

    assert len(args.klumps_tsv_list) > 1, "One or less files was given. Exiting"
    if args.output == None:
        args.output = "Combined_Klumps.tsv"

    return args.klumps_tsv_list, args.output

def longest_header(list_of_tsvs: list):
    """check if some tsvs have paired info"""

    column_cnts = 0 #will keep the longest header
    kept_header = ""

    for tsv in list_of_tsvs:
        tsv_fh = gzip.open(tsv, "rt") if tsv.endswith(".gz") else open(tsv, 'r')
        header = tsv_fh.readline()
        while header[0] == '#':
            header = tsv_fh.readline()
        header_col_cnts = header.count('\t')
        if header_col_cnts > column_cnts:
            kept_header = header
            column_cnts = header_col_cnts
        tsv_fh.close()

    return kept_header, column_cnts
        

def combine_tsvs(list_of_tsvs: list, output: str, kept_header: str, column_cnts: int):
    """write out combined files"""

    with open(output, 'w') as combined:
        combined.write(kept_header)
        for tsv in list_of_tsvs:
            input_tsv = gzip.open(tsv, "rt") if tsv.endswith(".gz") else open(tsv, 'r')
            for line in input_tsv:
                if line.startswith("Sequence\t") or len(line) == 0 or line[0] == '#':
                    continue
                else:
                    line_col_cnt = len(line.split('\t'))
                    #if paired end info is needed
                    if line_col_cnt < column_cnts:
                        line = line.replace('\n',"\tNA\n")
                    combined.write(line)
            input_tsv.close()
            
def Combine_Klumps(args):
    """Start Combining"""

    list_of_tsvs, output     = check_args(args)

    kept_header, column_cnts = longest_header(list_of_tsvs)

    combine_tsvs(list_of_tsvs, output, kept_header, column_cnts)
