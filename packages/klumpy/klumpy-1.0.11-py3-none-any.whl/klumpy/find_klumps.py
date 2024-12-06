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


import sys
import os
import gzip
from  .Classes import Klump, KLUMPS, Kmer

def check_params(args):
    """check params to prevent downstream errors"""

    # first, check if we are starting from fast[a|q] records
    if (args.subject != None) and (args.query != None) and (args.query_map == None):
        # run kmerize
        from .kmerize import Kmerize
        Kmerize(args)
        # assign outname to kmerize output
        args.query_map = "query_map.gz"
    # the above analysis should finish first
    if args.query_map != None:
        assert os.path.isfile(args.query_map), f"Could not find {args.query_map}"
        # check min_kmers param
        assert type(args.min_kmers) is int, "--min_kmers values must be an integer"
        assert args.min_kmers >= 0,         "--min_kmers cannot be a negative integer"
        # check base pair param:
        assert type(args.range) is int, "--range values must be an integer"
        assert args.range > 0,          "--range values must be greater than 0"
        # check query ct and klump_ct
        assert type(args.query_count) is int, "--query_count must be an integer"
        assert type(args.klump_count) is int, "--klump_count must be an integer"
    else:
        msg = "find_klumps must be either provided the --query_map file (generated from kmerize or find_klumps) or " + \
              "--subject and --query files in fast[a|q] format"
        sys.exit(msg)
    

    return args.query_map, args.output, args.range, args.min_kmers, args.query_count, args.klump_count

def make_output_name(input_file : str, extension: str, subject_file: str):
    """create the output file names"""

    # create base name
    filename = os.path.basename(input_file)

    # using default name?
    if filename == "query_map.gz":
        if subject_file != None:
            filename = os.path.basename(subject_file)
        else:
            return "query_klumps.tsv"

    if '.gz' in filename and filename.count('.') > 1:
        filename = filename.split(".")[:-2]
    elif filename.count('.') >= 1:
        filename = filename.split(".")[:-1]

    filename = ".".join([text for text in filename])
    output   = f"{str(filename)}{extension}"

    return output

def get_distributions(input: str):
    """parse the file for kmer distribution"""

    # create dict to store the data
    dict_of_seqs = {}
    seq_lengths  = {}
    src_dict     = {}
    ksize        = None

    if input.endswith(".gz"):
        cfile = gzip.open(input, "rt")
    else:
        cfile = open(input, 'r')

    for line in cfile:
        if (line[0] == '#'):
            if line.startswith("# k-size:"):
                try:
                    ksize = int(line.strip().split(': ')[1])
                except:
                    m = "ERROR: Could not parse k-size line\n" + \
                        "Offending line --> " + line
                    sys.exit(m)
            # move on regardless if it's true or not
            elif (line.startswith("#Source")):
                line    = line.replace("#Source ", '')
                sources = line.strip('\n').split(',')
                for source in sources:
                    source = source.strip(' ').split(' ')
                    src, idx = source[0], source[1]
                    src_dict[idx] = src
            continue
        list_of_coords = list()
        line           = line.strip()
        if line.count(':') == 1:
            seq_name = line.split(':')[0].split('[')[0][:-1]
            seq_lengths[seq_name] = \
                        int(line.split(":")[0].split("[")[1].replace("]",""))
            data = line.split(':')[1].split(',')
        else:
            seq_header = line.split(':')[:-1]
            seq_header = ":".join([name for name in seq_header])
            seq_name = seq_header.split('[')[0][:-1]
            if "_PAIRED" in seq_name:
                seq_length_name = seq_name.replace(f"_PAIRED{seq_name[-1]}", "")
            else:
                seq_length_name = seq_name
            seq_lengths[seq_length_name] = \
                int(seq_header.split('[')[1].replace(']',''))
            data = line.split(':')[-1].split(',')
        # parse data [kmer, coord, direction, query_id]
        for kmer_info in data:
            kmer_info = kmer_info.strip().split(" ")
            # position , query id, direction
            qsrc = src_dict.get(kmer_info[2], kmer_info[2])
            list_of_coords.append(Kmer(kmer_info[0], qsrc, kmer_info[1]))
        dict_of_seqs[seq_name] = list_of_coords

    if ksize == None:
        msg = f"Could not find k-size. Is the \"# k-size:\" present? in {os.path.basename(input)}?"
        sys.exit(msg)
    
    return dict_of_seqs, seq_lengths, ksize

def find_klumps(seq_dict: dict, bp_range: int, min_kmers: int, query_ct: int, klump_ct: int):
    """find and summarize klumps"""

    coord_dict = {}

    for seq, kmers_list in seq_dict.items():
        res, last = [[]], None
        # get first direction
        direction = kmers_list[0].direction
        current_src = kmers_list[0].query
        for kmer in kmers_list:
            if last is None or abs(last - kmer.pos) <= bp_range:
                # check if kmers are the same direction & from the same source
                if kmer.direction == direction and current_src == kmer.query:
                    res[-1].append(kmer)
                else:
                    res.append([kmer])
            else:
                res.append([kmer])
            direction   = kmer.direction
            last        = kmer.pos
            current_src = kmer.query
        coord_dict[seq] = res

    # if queryID present, assign as klump ID
    full_seq_klumps = {}

    for seq, full_list in coord_dict.items():
        klump_cnt = 1
        seq_klump = KLUMPS(seq)
        for klumps in full_list:
            if len(klumps) < min_kmers:
                continue
            direction = klumps[0].direction
            first_pos = klumps[0].pos
            last_pos  = klumps[-1].pos
            # use coordinates and source of kmers for klump name
            queries = set()
            for kmer in klumps:
                queries.add(kmer.query)
            klmp = Klump(f"Klump{klump_cnt}", first_pos,
                         last_pos, queries, len(klumps), direction)
            seq_klump.add_klumps(klmp)
            klump_cnt += 1
        seq_klump.create_all_klumps()
        full_seq_klumps[seq] = seq_klump

    # check if query ct is requested
    if query_ct > 1:
        filtered_coord_dict = {seq: klmp for seq, klmp in full_seq_klumps.items(
        ) if len(klmp.queries()) >= query_ct}
        # replace
        full_seq_klumps = filtered_coord_dict
        del filtered_coord_dict

    # another check for klump_ct
    if klump_ct > 1:
        filtered_coord_dict = {seq: klmp for seq, klmp in full_seq_klumps.items(
        ) if klmp.num_of_klumps() >= klump_ct}
        full_seq_klumps = filtered_coord_dict
        del filtered_coord_dict

    return full_seq_klumps

def sort_klump_info(klump_info: dict):
    """sort klump dictionary prior to writing"""

    num_klumps = len(klump_info)
    if num_klumps == 1:
        return klump_info
    else:
        fwd_klmps  = {}
        rvsd_klmps = {}
        for klmp, klmp_info in klump_info.items():
            if klmp_info[4] == 'F':
                fwd_klmps[klmp] = klmp_info
            elif klmp_info[4] == 'R':
                rvsd_klmps[klmp] = klmp_info
        for klmp in reversed(list(rvsd_klmps.keys())):
            fwd_klmps[klmp] = rvsd_klmps[klmp]
        num = 1
        sorted_dict = {}
        for klmp, klmp_info in fwd_klmps.items():
            new_klmp = "Klump" + str(num)
            sorted_dict[new_klmp] = klmp_info
            num += 1
        return sorted_dict


def write_threshold_met(meets_threshold: dict, output: str, seq_lengths: dict, ksize: int):
    """write info for sequences meeting threshold"""

    # store arguments to tsv file
    command = "# klumpy " + \
         " ".join("\"" + arg + "\"" if " " in arg else arg for arg in sys.argv[1:]) + '\n'

    #store lines for printing
    printing_lines = []
    out_header = \
        f"Sequence\tSeq_Length\tKlump\tKlump_Start\tKlump_End\tQuery\tKmer_Count\tDirection\n"
    printing_lines.append(out_header[:-1]) #exclude '\n'

    with open(output, "w") as out:

        # header
        header_written = False
        
        #if pair info present
        extra_column = False

        # get klump info and store as dict
        all_klump_info = {q: info.all_klumps for q,
                          info in meets_threshold.items()}

        for Seq, klumps_info in all_klump_info.items():
            #check if paired info attach to remove
            if "PAIRED" in Seq.split("_")[-1]:
                extra_column = True
                pair_num = Seq[-1]
                #get original name
                org_name = Seq.replace(f"_PAIRED{pair_num}", "")
                if org_name[-2:] in ["/1", "/2"]:
                    Seq = org_name[:-2]
                else:
                    Seq = org_name
            else:
                org_name = Seq
            if not header_written:
                if extra_column:
                    out_header = out_header.replace("\n", "\tPair_Num\n")
                    printing_lines[0] = printing_lines[0].replace("Direction","Direction\tPair_Num")
                out.write(command)
                out.write(out_header)
                header_written = True
            #initially captured during parsing,
            #hence, using original name
            seq_length  = seq_lengths[org_name]
            sorted_info = sort_klump_info(klumps_info)
            for klump, klmp_info in sorted_info.items():
                start = klmp_info[0] + 1
                end   = klmp_info[1] + ksize # 1-based so no need to subtract 1
                queries = klmp_info[2]
                if len(queries) == 1:
                    query = list(queries)[0]
                else:
                    query = ", ".join(q for q in queries)
                size = klmp_info[3]
                direction = klmp_info[4]
                line = f"{Seq}\t{seq_length}\t{klump}\t{start}\t{end}\t{query}\t{size}\t{direction}\n"
                if extra_column:
                    line = line.replace("\n", f"\t{pair_num}\n")
                out.write(line)
                printing_lines.append(line[:-1])

    return printing_lines

def Find_Klumps(args):
    """Find the klumps!"""

    # get arguments
    input, output, bp_range, min_kmers,\
         query_ct, klump_ct = check_params(args)

    # get distributions
    dict_of_seqs, seq_lengths, ksize = get_distributions(input)

    seq_klumps_dict = find_klumps(
        dict_of_seqs, bp_range, min_kmers, query_ct, klump_ct)
    
    #write results
    if output != None:
        printing_lines = write_threshold_met(seq_klumps_dict, output, seq_lengths, ksize)
    else:
        output         = make_output_name(input, "_klumps.tsv", args.subject)
        printing_lines = write_threshold_met(seq_klumps_dict, output, seq_lengths, ksize)
    
    #print results
    print()
    for line in printing_lines:
        print(line)
        