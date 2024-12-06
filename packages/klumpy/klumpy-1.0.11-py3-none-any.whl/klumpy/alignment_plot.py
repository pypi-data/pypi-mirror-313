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

import math
import cairo
import sys
import gzip
import os
import random
from   collections import defaultdict
from   typing      import List
from  .Classes     import SAM, SAM_FLAG, GAP, Feature_Color, Klump, GeneRecord, algn_blocks, Label_Position
from  .grouping    import Group_Seqs, within_window

########## safety/validating functions #############

def check_tick_params(tick_count: int, tick_span: float, leftbound: int, rightbound: int):
    """a function to verify that the tick counts are legal or need some modification"""

    # do some assertions
    if tick_count != None:
        assert type(tick_count) == int, "--tick_count requires an integer"
        assert tick_count >= 0,         "--tick_count cannot be negative"
        if tick_span != None:
            assert type(tick_span) == float, "--tick_span requires a number [float or int]"
            assert tick_span > 0,            "--tick_span must be greater than 0"
            tick_span = int(tick_span)
            last_tick = leftbound + (tick_count * tick_span)
            if last_tick > rightbound:
                msg = f"--rightbound set to {rightbound}." + \
                      f"Setting --tick_count to {tick_count} and --tick_span to {tick_span} places last tick at {last_tick}"
                sys.exit(msg)
        else:
            # estimate tick_span
            tick_span = (rightbound - leftbound) // (tick_count + 1) # do not include rightbound pos
    elif tick_span != None:
        assert type(tick_span) == float, "--tick_span requires a number [float or int]"
        assert tick_span > 0,            "--tick_span must be greater than 0"
        tick_span = int(tick_span)
        assert leftbound + tick_span < rightbound, f"--tick_span {tick_span} + --leftbound {leftbound} is greater than --rightbound {rightbound}"
        tick_count = ((rightbound - leftbound) // (tick_span)) # - 1  # TODO this minus 1 may need to be re-implemented in the future
    else:
        tick_count, tick_span = None, None

    # if passed all checks, return validated values
    return tick_count, tick_span

def percent_check(value: float, msg: str):
    """function to convert a number to an allowable percentage"""

    if value >= 1.0:
        if (value/100.0) > 1.0:
            msg = msg + " percentage calculated was >100%. Use a value like 2 or 0.02"
            sys.exit(msg)
        else:
            return value/100.0
    else:
        return value

def group_assert(val: float, var: str):
    """assert that the grouping variables are integers"""
    
    fmsg = var + " must be a number"
    imsg = var + " cannot be a negative integer"

    try:
        val = int(val)
        assert type(val) == int, fmsg
        assert 0 <= val,         imsg
    except:
        sys.exit(fmsg)

    return val

def check_args(args):
    """determine if params are acceptable"""

    assert type(args.list_colors) is bool, "--list_colors does not take any positional values"
    if args.list_colors:
        get_color(True, False, 0)

    warning_color = "\033[93m"
    end_color     = "\033[0m"

    # check if alignment file exists and samtools is in path
    if args.alignment_map == None:
        msg = "--alignment_map SAM/BAM file is required for alignment_plot"
        sys.exit(msg)
    if os.path.isfile(args.alignment_map):
        in_path = os.popen("which samtools").read()
        if in_path.startswith("which: no samtools"):
            msg = "Samtools was not found in your path"
            sys.exit(msg)
        index_file1 = args.alignment_map + ".bai"
        index_file2 = args.alignment_map.replace(".bam", ".bai")
        if (os.path.isfile(index_file1) == False) and (os.path.isfile(index_file2) == False):
            msg = f"Could not locate an index file (*.bai) for {args.alignment_map}\n" + \
                  "Input must follow samtools requirements for indexing\n" + \
                  "File must be BGZF compressed & indexed"
            sys.exit(msg) 
    else:
        msg = f"Could not find {args.alignment_map}"
        sys.exit(msg)

    # check if a reference or candidates file was provided
    if args.reference == None:
        assert args.candidates != None,          "No --candidates or --reference argument provided"
        assert os.path.isfile(args.candidates), f"Could not locate {args.candidates}"
        assert type(args.region_num) == int,     "--region_num must be an integer"
        # assign values
        ref, l, r       = parse_candidates(args.candidates, args.region_num)
        args.reference  = ref
        args.leftbound  = l
        args.rightbound = r
    
    # no else b/c it is not none by now
    
    # check inputs for non-scan pipeline
    # make sure bounds are reasonable
    # adjusts for extending past reference seq
    # this will also cause an error if leftbound is greater than ref len
    assert args.leftbound >= 0, "Leftbound cannot be a negative number" 
    args.rightbound = \
        adjust_rightbound(args.reference, args.rightbound, args.alignment_map)
    assert args.rightbound > args.leftbound, "Rightbound must be greater than leftbound"
    assert args.view_span >= 0,              "The view offset used when calling samtools must be greater or equal to 0"
    assert args.height    > 0,               "Figure height must be greater than 0"
    assert args.width     > 0,               "Figure width must be greater than 0"
    assert args.min_len   > 0,               "--min_len must be greater than 0"

    # convert params to ints
    args.leftbound                  = int(args.leftbound)
    args.min_len                    = int(args.min_len)
    args.deletion_len               = int(args.deletion_len)
    args.tick_count, args.tick_span = \
        check_tick_params(args.tick_count, args.tick_span, args.leftbound, args.rightbound)

    # ensure one type of alignment is to be retained
    if args.no_primary:
        if args.secondary == False and args.supplementary == False:
            msg = "Error. Filtering out primary, secondary, and supplementary alignments\n" + \
                  "Please ensure 1 type of alignment is to be retained"
            sys.exit(msg)

    # other params to verify
    assert type(args.deletion_len) is int, "--deletion_len must be an integer"
    if args.plotting_list != None:
        assert os.path.isfile(args.plotting_list), f"Could not find {args.plotting_list}"

    #check gtf/gff3 file 
    if args.annotation != None:
        if os.path.isfile(args.annotation):
            if (args.annotation.endswith(".gtf.gz"))   or (args.annotation.endswith(".gtf")):
                pass
            elif (args.annotation.endswith(".gff.gz")) or (args.annotation.endswith(".gff")) or \
                (args.annotation.endswith(".gff3.gz")) or (args.annotation.endswith(".gff3")):
                pass
            else:
                msg = f"No .gtf, .gtf.gz, .gff, .gff.gz, .gff3, or .gff3.gz file extension detected in {args.annotation}" + \
                    "\nAssuming proper input"
                print(f"{warning_color}{msg}{end_color}")
        else:
            sys.exit(f"Could not find {args.annotation}")

    if args.vertical_line_exons:
        if args.annotation == None:
            msg = "WARNING: Drawing vertical lines at exons requires annotation file in gtf/gff3 format for exon locations"
            print(f"{warning_color}{msg}{end_color}")
            args.vertical_line_exons = False

    #check gaps file   
    if args.gap_file != None:
        assert os.path.isfile(args.gap_file), f"Could not find {args.gap_file}"
        fh = gzip.open(args.gap_file, "rt") if args.gap_file.endswith(".gz") else open(args.gap_file, 'r')
        for line in fh:
            if len(line.strip().split("\t")) != 3:
                sys.exit(f"Check if {args.gap_file} is a three column file")
            else:
                break
        #check if drawing vertical dashes at gaps
        assert type(args.vertical_line_gaps) is bool, "--vertical_line_gaps does not take any positional values"
        if args.vertical_line_gaps:
            if args.gap_file == None:
                msg = "WARNING: Drawing vertical lines at gaps requires gap file for gap locations"
                print(f"{warning_color}{msg}{end_color}")    
                args.vertical_line_gaps = False
    else:
        args.vertical_line_gaps = False

    if args.klumps_tsv != None:
        assert os.path.isfile(args.klumps_tsv), f"Could not find {args.klumps_tsv}"
        assert type(args.min_klump_size) is int, "--min_klump_size must be an integer"
        assert args.min_klump_size >= 0,         "--min_klump_size must be greater or equal to 0"
        #check if drawing vertical dashes at klumps
        assert type(args.vertical_line_klumps) is bool, "--vertical_line_klumps does not take any positional values"
        if args.vertical_line_klumps:
            if args.klumps_tsv == None:
                msg = "WARNING: Drawing vertical lines at klumps requires klumps tsv file for klump locations"
                print(f"{warning_color}{msg}{end_color}")
        if args.klump_colors != None:
            assert os.path.isfile(args.klump_colors), f"Could not find {args.klump_colors}"
            assert type(args.color_by_gene) == bool,   "--color_by_gene does not take any arguments"
    else:
        args.vertical_line_klumps = False   

    # check for currently available colors and set as default
    args.color = get_color(False, False, 0, args.color)

    # check other boolean params
    assert type(args.supplementary) is bool, "--supplementary does not taken any positional values"
    assert type(args.secondary)     is bool, "--secondary does not take any positional values"
    assert type(args.number)        is bool, "--number does not take any positional values"
    assert type(args.write_table)   is bool, "--write_table does not take any positional values"
    assert type(args.paired)        is bool, "--paired does not take any positional values"
    assert type(args.group_seqs)    is bool, "--group_seqs does not take any positional values"
    assert type(args.no_subsample)  is bool, "--no_subsample does not take any positional values"

    #check for percentages
    msg              = "Minimum mapping"
    args.min_percent = percent_check(args.min_percent, msg)
    msg              = "Maximum mapping"
    args.max_percent = percent_check(args.max_percent, msg)
    assert args.min_percent <= args.max_percent, "--min_percent cannot be higher than --max_percent"
   
    # currently only supports non-paired end
    if args.group_seqs:
        msg                 = "Minimum percent for trusting a sequence when grouping"
        args.t_per          = percent_check(args.t_per, msg)
        msg                 = "Minimum percent for confidently grouping two sequences"
        args.per_overlap    = percent_check(args.per_overlap, msg)
        args.align_offset   = group_assert(args.align_offset, "Alignment Offset")
        args.clip_tolerance = group_assert(args.clip_tolerance, "Clip tolerance")
        args.del_tolerance  = group_assert(args.del_tolerance, "Deletion tolerance")
        args.t_len          = group_assert(args.t_len, "Trustworthy length")
        args.min_grp        = group_assert(args.min_grp, "Minimum group")
        assert type(args.assume_sep_del)  is bool, "--assume_sep_del does not take any positional values"
        assert type(args.write_groups)    is bool, "--write_groups does not take any positional values"
        assert type(args.write_seqs)      is bool, "--write_seqs does not take any positional values"
        assert type(args.write_edge_seqs) is bool, "--write_edge_seqs does not take any positional values"
        assert args.limit                    >= 0, "--limit must be >= 0"

        msg = f"WARNING: Grouping Sequences currently only uses primary alignments. " 
        if args.supplementary == args.secondary == True:
            msg = msg + "Excluding supplementary and secondary alignments"
            print(f"{warning_color}{msg}{end_color}")
            args.supplementary = False
            args.secondary = False
        elif args.supplementary:
            msg = msg + "Excluding supplementary alignments"
            print(f"{warning_color}{msg}{end_color}")
            args.supplementary = False
        elif args.secondary:
            msg = msg + "Excluding secondary alignments"
            print(f"{warning_color}{msg}{end_color}")
            args.secondary = False
        if args.paired:
            msg = "WARNING: Currently only support grouping sequences using non-paired-end sequences. No grouping will be performed."
            print(f"{warning_color}{msg}{end_color}")
            args.group_seqs = False
        # turn off write seqs if write_groups is set
        if args.write_seqs and args.write_groups:
            msg = "Writing group sequences will supersede writing sequences"
            print(f"{warning_color}{msg}{end_color}")
            args.write_seqs = False

    return args.alignment_map, args.klumps_tsv, args.reference, args.leftbound, args.rightbound, \
            args.view_span, args.min_len, args.min_klump_size, args.min_percent, args.max_percent , \
            args.annotation, args.vertical_line_exons, args.height, args.width, args.write_table, \
            args.supplementary, args.gap_file, args.plotting_list, args.number, args.secondary, args.paired, \
            args.color, args.klump_colors, args.color_by_gene, args.vertical_line_gaps, \
            args.vertical_line_klumps, args.no_primary, args.format, args.group_seqs, args.deletion_len, \
            args.align_offset, args.clip_tolerance, args.t_len, args.t_per, args.per_overlap, args.del_tolerance, \
            args.assume_sep_del, args.write_groups, args.min_grp, args.write_seqs, args.write_edge_seqs, \
            args.limit, args.no_subsample, args.tick_count, args.tick_span


######### parsing functions ############

def parse_candidates(candidates_tsv: str, region_num: int):
    """parse a candidates file for a region & return the positions of the window"""

    fh = gzip.open(candidates_tsv, "rt") if candidates_tsv.endswith(".gz") else open(candidates_tsv, 'r')

    reference  = None
    region_num = str(region_num) # a single conversion

    for line in fh:
        if line[0] == '#' or line.startswith("Region_Num\t"):
            continue
        fields = line.strip().split('\t')
        if fields[0] == region_num: # found the region
            reference  = fields[1]
            leftbound  = int(fields[2]) + 1
            rightbound = int(fields[3]) # will keep this as is and assume it is inclusive
            break

    fh.close()

    if reference == None:
        msg = f"Could not locate region number: {region_num}"
        sys.exit(msg)
    else:
        return reference, leftbound, rightbound 

def parse_klumps_out(klump_file: str, min_len: int, klump_size: int, paired_end: bool):
    """get klump info per sequence"""

    warning_color = "\033[93m"
    end_color     = "\033[0m"

    #determine if parsing to returning None's
    if klump_file == None:
        return None, None
    
    fh = gzip.open(klump_file, "rt") if klump_file.endswith(".gz") else open(klump_file, 'r')

    seq_klumps  = {}
    seq_lengths = {}
    src_dict    = {}

    for line in fh:
        if line.startswith("Sequence\t"):
            continue
        if (line[0] == '#'):
            if (line.startswith("#Source") == False): continue
            line    = line.replace("#Source ", '')
            sources = line.strip('\n').split(',')
            for source in sources:
                source = source.strip(' ').split(' ')
                src, idx = source[0], source[1]
                src_dict[idx] = src
            continue
        fields = line.strip().split("\t")
        #plotting only min_len seqs and klumps
        if int(fields[1]) < min_len or int(fields[6]) < klump_size:
            continue
        #only get klumps with alignment or ref klumps
        seq = fields[0]
        # keep track of seq length
        seq_lengths[seq] = int(fields[1])
        # klump name, start pos, end pos,
        # query source, klump size, direction
        qsrc = src_dict.get(fields[5], fields[5])
        klmp = Klump(fields[2], fields[3], fields[4],
                     qsrc, fields[6], fields[7])
        if paired_end:
            #check if pair info column was added
            if len(fields) == 9:
                #if klump tsv has a mixture of data
                if fields[8] in ["1", "2"]:
                    klmp.add_pair_num(int(fields[8]))
            else:
                msg = "WARNING: Paired End set as True but no paired-end info for klumps found"
                print(f"{warning_color}{msg}{end_color}")
        if seq not in seq_klumps:
            seq_klumps[seq] = [klmp]
        else:
            seq_klumps[seq].append(klmp)

    fh.close()

    # sort & some filtering, then return
    if len(seq_klumps) > 0:
        # only return records if present
        kept_lengths = {seq: seq_lengths[seq] for seq in seq_klumps.keys()}
        seq_klumps = dict(sorted(seq_klumps.items(), key = lambda klump: klump[1][0].start_pos))

    return seq_klumps, kept_lengths

def parse_sam(align_map: dict, ref: str, leftbound: int, rightbound: int, min_len: int,  seq_lengths: dict, 
              percent: float, max_per: float, figure_height: int, figure_width: int, supplementary: bool, 
              plotting_list: str, secondary: bool, no_primary: bool, limit: int, no_subsample: bool,
              paired_end: bool, deletion_len: int, grouping: bool, view_len: int, write_seqs: bool):
    """parse sam/bam file to retrieve the alignment records given a locus and criteria"""

    alignments = defaultdict(list)
    
    #check if klump file was added (i.e., seq lengths available)
    if seq_lengths == None:
        seq_lengths = {}

    #check for sequences of interest
    if plotting_list != None:
        plotting_list = parse_plotting_list(plotting_list)

    # import once
    if grouping or write_seqs:
        from .Classes import Seq_Record

    # samtools does not return alignments where the clip is within the region
    # so I will look ~500 Mb from the region of interest in both directions
    # in theory, MOST cases should be able to cover this region
    left_search  = leftbound - view_len
    right_search = rightbound + view_len

    if left_search < 0:
        left_search = 0

    cmd = f"samtools view {align_map} " + '"' + f"{ref}:{left_search}-{right_search}" + '"'
    fh  = os.popen(cmd, 'r')

    for line in fh:
        if line.startswith('@'):
            continue
        fields = line.strip('\n').split('\t')
        #check if even considering the sequence
        if plotting_list != None:
            if r'{}'.format(fields[0]) not in plotting_list:
                continue
        # index fields for passing filters
        seq_name          = fields[0]
        seq_flag          = int(fields[1])
        seq_cigar         = fields[5]
        leftmost_position = int(fields[3]) + 1 # SAM/BAM is 0-based
        paired            = False #assume not paired-end
        #get seq length if not in seq_lengths
        if seq_name not in seq_lengths:
            seq_lengths[seq_name] = estimate_seq_length(seq_cigar)
        # skip short seqs
        sequence_length = seq_lengths[seq_name]
        if sequence_length < min_len:
            continue
        #check if skipping primary/supplementary/secondary alignments
        sam_flag = SAM_FLAG(seq_flag)
        if no_primary:
            if sam_flag.primary: # if it is primary
                continue
        if secondary == False:
            if sam_flag.secondary:
                continue
        if supplementary == False:
            if sam_flag.supplementary:
                continue
        # data is presumably paired-end
        if paired_end:
            #remove non-proper alignments
            if (seq_flag & 3) != 3:
                continue
            # check pair num
            if (seq_flag & 1) == 1:
                if (seq_flag & 64) == 64:
                    pair_num = 1
                    paired   = True
                elif (seq_flag & 128) == 128:
                    paired   = True
                    pair_num = 2
                else:
                    pair_num = 0
            else:
                pair_num = 0
        algn_len, clipping_start, adjust_start, clipping_end, \
             adjust_end, align_blocks = \
            parse_cigar(seq_cigar, deletion_len)
        #check for % aligned considering regardless of clip type
        if adjust_start == None:
            clipped_start = 0
        else:
            clipped_start = adjust_start
        if adjust_end == None:
            clipped_end = sequence_length
        else:
            clipped_end = sequence_length - adjust_end
        percent_aligned = (clipped_end - clipped_start)/sequence_length
        #filter by align %
        if percent_aligned < percent or percent_aligned > max_per:
            continue
        in_window = within_window(leftmost_position, align_blocks, leftbound, rightbound, clipped_start)
        if in_window:
                segment    = (algn_len != sequence_length)
                #create sam object
                sam_record = SAM(seq_name, leftmost_position, seq_flag,
                                     ref, segment, align_blocks, clipping_start,
                                     adjust_start, clipping_end, adjust_end, 
                                     percent_aligned, sequence_length, sam_flag.primary)
                # add pair num info if paired
                if paired:
                    sam_record.pair_num = pair_num
                #add color
                sam_record.seq_color = algn_color(seq_flag)
                # add seq if writing
                if sam_record.IsPrimary:
                    if grouping or write_seqs:
                        if (seq_flag & 16) == 16:
                            sam_record.seq = Seq_Record.reverse_complement(fields[9])
                        else:
                            sam_record.seq = fields[9]
                #store
                alignments[seq_name].append(sam_record)

    fh.close()

    num_alignments = len(alignments)

    if num_alignments == 0:
        sys.exit(f"No matching records found within alignment file. Please check {align_map}.")

    #rescale?
        
    if num_alignments > limit:
        warning_color = "\033[93m"
        end_color     = "\033[0m"

        if no_subsample == False: 
            msg = f"WARNING: {num_alignments} sequence alignments found. Randomly subsampling to --limit size of {limit}.\n" + \
                    "To turn off random subsampling, add --no_subsample to command"
            alignments = dict(random.sample(alignments.items(), limit))
        else:
            msg           = f"WARNING: {num_alignments} sequence alignments found. Rescaling image dimensions..."
            figure_height = limit
            figure_width  = limit

        print(f"{warning_color}{msg}{end_color}")

    # add a map_num for each alignment
    for seq, algnments in alignments.items():
        for num, algn in enumerate(algnments):
            algn.map_num = f"{seq}-alignment-{num}"

    # returning only the seq lengths for seqs in alignments
    seq_lengths     = {seq: seq_lengths[seq] for seq in list(alignments.keys())}

    # add ref
    seq_lengths[ref] = int(rightbound - leftbound)
    
    # print info
    num_rec = len(alignments)
    ending  = "record"
    if num_rec > 1:
        ending += 's'

    print(f"A total of {num_rec} alignment {ending} will be drawn")
    
    return alignments, figure_height, figure_width, seq_lengths

def parse_annotation_file(annotation_file: str, leftbound: int, rightbound: int, chrom: str):
    """get the exons within the region based on the annotation coordinates"""

    print(f"Parsing {os.path.basename(annotation_file)}")

    fh = gzip.open(annotation_file, "rt") if annotation_file.endswith(".gz") else open(annotation_file, 'r')

    # CDS & exon records will be treated as exon records
    genes_found     = list()
    num_genes       = 0
    exons           = {}
    gene_record     = GeneRecord() # start off empty
    process_records = ["gene", "mRNA", "cds", "exon"] # construct once

    for line in fh:
        if line[0] == '#':
            continue
        fields = line.strip('\n').split('\t')
        if fields[0] == chrom:
            record_type = fields[2].lower()
            if record_type in process_records:
                if gene_record.update(record_type):
                    exons, genes_found = \
                        gene_record.incorporate(leftbound, rightbound, exons, genes_found)
                    num_genes = len(genes_found)
                gene_record.parse_attributes(fields[8])
                if record_type in ["cds", "exon"]:
                    left      = int(fields[3])
                    right     = int(fields[4])
                    direction = fields[6]
                    # may consider moving this step to the class
                    num        = num_genes % 6
                    gene_color = get_color(False, True, num)
                    # duplicates are not added
                    gene_record.add_exon(left, right, direction, gene_color, line)
            
    # get last bit
    if not gene_record.empty():
        exons, genes_found = gene_record.incorporate(leftbound, rightbound, exons, genes_found)
    
    # report to the user
    if num_genes > 0:
        genes = ' '.join(genes_found)
        print("Found the following genes:", genes)

    return exons
                
def parse_gap_file(gap_file: str, ref: str, leftbound: int, rightbound: int):
    """get gaps to plot onto ref"""

    #column 0: seq_id
    #column 1: start position
    #column 2: end position

    gaps = []

    fh = gzip.open(gap_file, "rt") if gap_file.endswith(".gz") else open(gap_file, 'r')

    for line in fh:
        fields = line.strip().split('\t')
        if fields[0] == ref:
            #0-based positions
            if leftbound <= int(fields[1]) <= rightbound or \
                leftbound <= int(fields[2]) <= rightbound:
                start_pos = int(fields[1])
                end_pos   = int(fields[2])
                #just in case gap crosses boundaries                    
                if start_pos <= leftbound:
                    start_pos = leftbound
                if end_pos >= rightbound:
                    end_pos   = rightbound
                gaps.append(GAP(start_pos, end_pos))

    fh.close()

    return gaps

def parse_cigar(cigar: str, deletion_len: int):
    """estimate seq len using cigar"""

    def create_op():
        """quick generation per block"""
        operators = {'M':0,
                    'I': 0,
                    'S':0,
                    '=':0,
                    'X':0}
        return operators

    # deletions will shift sequences
    align_blocks  = algn_blocks()
    block         = []
    current_cnt   = ''
    Op            = [] #operators found for entire cigar
    block_num     = 0
    estimated_len = 0
    del_cnt       = 0 # for total covered length
    del_pos       = {} # positions of deletions, needed to shift klumps
    hclip_start   = 0
    hclip_end     = 0
    pos           = 0
    operators     = create_op()

    for char in cigar:
        if char.isdigit():
            current_cnt += char
        elif char in operators:
            pos             += int(current_cnt)
            operators[char] += int(current_cnt)
            Op.append(char)
            if char != 'I': # insertions do not consume ref
                block.append(int(current_cnt))
            current_cnt = ''
        else:
            current_cnt       = int(current_cnt)
            if current_cnt >= deletion_len and char == 'D':
                estimated_len += sum(list(operators.values()))
                del_pos[pos]   = current_cnt # document deletion pos
                operators      = create_op()
                align_blocks.add_entry(block_num, block, current_cnt, del_cnt)
                block_num     += 1
                block          = []
                del_cnt        = 0
                pos           += int(current_cnt)
            elif char == 'D':
                del_pos[pos]   = current_cnt
                del_cnt       += current_cnt
                pos           += current_cnt
            elif char == 'H':
                if len(Op) == 0:
                    hclip_start = current_cnt
                else:
                    hclip_end   = current_cnt
            Op.append(char)
            current_cnt = ""
    
    # last block
    estimated_len += sum(list(operators.values()))
    align_blocks.add_entry(block_num, block, 0, del_cnt)
    del current_cnt

    # add deletion blocks
    align_blocks.add_del_pos(del_pos)

    #check for soft (S) or hard (H) clips
    clipping_start = None
    if Op[0] == 'S':
        clipping_start = 'S'
    elif Op[0] == 'H':
        clipping_start = 'H'
    if clipping_start != None:
        if clipping_start == 'S':
            adjust_start = align_blocks.adjust_start()
        else:
            adjust_start = hclip_start
    else:
        adjust_start = None
    
    clipping_end = None
    if Op[-1] == 'S':
        clipping_end = 'S'
    elif Op[-1] == 'H':
        clipping_end = 'H'
    if clipping_end != None:
        clipped_site = ""
        for char in cigar[::-1]:
            if char in ['S','H']:
                continue
            elif char.isdigit():
                clipped_site += str(char)
            else:
                adjust_end = int(clipped_site[::-1])
                break
    else:
        adjust_end = None
    
    # finalize alignment blocks
    if clipping_start == None:
        c_start = 0
    else:
        c_start = adjust_start

    if clipping_end == None:
        c_end = 0
    else:
        c_end = adjust_end

    # aligned length does not include clipping ends
    if clipping_end == 'S':
        align_blocks.adjust_end(adjust_end)

    # now calculate the total covered length (alignment portion + clips + deletions)
    align_blocks.covered_region(c_start, c_end)

    return estimated_len, clipping_start, adjust_start, clipping_end, \
        adjust_end, align_blocks

def parse_plotting_list(plotting_list: str):
    """extract sequences to be plotted"""

    fh = gzip.open(plotting_list, "rt") if plotting_list.endswith(".gz") else open(plotting_list, 'r')

    # use raw strings just in case of some weird characters
    seq_list = [r'{}'.format(line.strip('\n')) for line in fh]

    fh.close()

    return seq_list

def parse_klump_color_list(klump_colors: str):
    """return a dictionary where the key is the source and the value is the color"""

    fh = gzip.open(klump_colors, "rt") if klump_colors.endswith(".gz") else open(klump_colors, 'r')

    klump_colors = {}

    for line in fh:
        fields                  = line.strip('\n').split('\t')
        klump_colors[fields[0]] = get_color(False, False, 0, fields[1])

    fh.close()

    return klump_colors

########## analytical functions #############

def identify_overlaps(alignments: dict):
    """find which alignments overlap each other"""

    overlaps = defaultdict(dict)

    for seq_name, alignmnts in list(alignments.items()):
        mappings = {}
        for algn in alignmnts:
            algn_length = algn.aligned_length
            if len(mappings) == 0:
                mappings[algn.map_num]           = (algn.position, algn.position + algn_length)
                overlaps[seq_name][algn.map_num] = False
            else:
                for mapped, positions in list(mappings.items()):
                    # first scenario (position inside mapped region)
                    #        |------------|
                    #      |-----------|
                    if positions[0] <= algn.position <= positions[1]:
                        overlaps[seq_name][mapped]       = True
                        overlaps[seq_name][algn.map_num] = True
                        mappings[algn.map_num]           = (algn.position, algn.position + algn_length)
                    # second scenario (will catch only ones coming from the left)
                    #    |--------|
                    #      |-----------|
                    elif algn.position <= positions[0] <= algn.position + algn_length <= positions[1]:
                        overlaps[seq_name][mapped]       = True
                        overlaps[seq_name][algn.map_num] = True
                        mappings[algn.map_num]           = (algn.position, algn.position + algn_length)
                    # no overlap for the query
                    else:
                        overlaps[seq_name][algn.map_num] = False
                        mappings[algn.map_num]           = (algn.position, algn.position + algn_length)

    return overlaps

def estimate_seq_length(cigar: str):
    """Estimate seq length using cigar"""

    operators     = ['M', 'I', 'S', '=', 'X', 'H']
    current_cnt   = ''
    estimated_len = 0

    for char in cigar:
        if char.isdigit():
            current_cnt += char
        elif char in operators:
            estimated_len += int(current_cnt)
            current_cnt = ''
        else:
            current_cnt = ''

    return estimated_len

def scale_image_width(alignments: dict, leftmost: int, rightbound: int):
    """determine width to contain all seqs"""

    rightmost = 0
    for aligns in alignments.values():
        for align in aligns:
            rightpos = align.position + align.aligned_length
            if align.clipping_end:
                rightpos += align.adjust_end
            if rightpos > rightmost:
                rightmost = rightpos

    if rightbound < rightmost:
        image_area = rightmost - leftmost
    else:
        image_area = rightbound - leftmost

    return image_area

def adjust_x(image_width: int, seq_name: str, alignments: dict, leftmost_pos: float, 
             leftbound: int, position: float, image_area: float, figure_width: int, 
             clipping_start: str, adjust_start: int):
    """"estimate where to plot seqs by first align length"""

    #check if we need to adjust x pos based on clipping
    if clipping_start != None:
        position = position - adjust_start

    # the left most alignment will start 1% off the leftside of the img
    if seq_name in alignments:
        if leftmost_pos == position:
            return figure_width * 0.01
        else:
            # scale to leftmost
            allocated_pos     = image_width / image_area
            adjusted_position = position - leftmost_pos
            adjusted_x        = (figure_width * 0.01) + (allocated_pos*adjusted_position)
            return adjusted_x
    else:
        allocated_pos = image_width / image_area
        adjusted_x    = (figure_width * 0.01) + (allocated_pos*(leftbound - leftmost_pos))
        return adjusted_x

def create_seq_sizes(figure_height: int, num_seqs: int):
    """adjust seq sizes based on number of alignments and figure length"""

    offset       = figure_height * 0.01
    top          = figure_height * 0.99
    ref_area     = figure_height * 0.02 #proportion
    section_area = top - (figure_height * 0.1)
    sections     = section_area/num_seqs
    bottom       = figure_height * 0.905

    return offset, ref_area, sections, bottom

def set_up_plt(figure_height: float, alignments: dict, ref: str, leftbound: int, enumerating: bool):
    """set up plt height and y positions"""
    
    y_positions     = {} # y axis
    positions       = [] # for leftmost position (i.e., x axis)
    leftmost_aligns = {} # leftmost for each seq

    for seq, algns in alignments.items():
        for algn in algns: 
            if algn.clipping_start in ['S','H']:
                position = algn.position - algn.adjust_start
            else:
                position = algn.position
            positions.append(position)
            if seq not in leftmost_aligns:
                leftmost_aligns[seq] = position
            elif leftmost_aligns[seq] > position:
                leftmost_aligns[seq] = position
    
    #find leftmost seq
    leftmost_pos = min(positions)

    #if leftbound is left of leftmost seq
    if leftmost_pos > leftbound:
        leftmost_pos = leftbound

    #leftmost seq will be plotted at the top
    sorted_algns  = dict(sorted(leftmost_aligns.items(), key=lambda seq: seq[1]))
    reversed_seqs = list(sorted_algns.keys())[::-1]

    #if enumerating
    if enumerating:
        enumeration_dict = {seq: i for i, seq in enumerate(list(sorted_algns.keys()))}
    else:
        enumeration_dict = None

    #adjust image space by saving % for reference
    num_seqs = len(reversed_seqs)
    offset, ref_area, sections, bottom \
        = create_seq_sizes(figure_height, num_seqs)
    
    #check to avoid plotting sequences too wide for current plotting method
    if sections >= ref_area:
        print(f"The number of alignments ({num_seqs}) may not look well for the figure.")
        print("Adjusting...")
        adjusted_length = (figure_height - (2*offset))
        original_len    = figure_height + 0
        original_ref    = ref_area + 0
        adjusted_length = original_len - (2*offset)
        figure_height   = original_ref
        
        for _ in range(num_seqs):
            figure_height += sections
        offset, ref_area, sections, bottom \
            = create_seq_sizes(figure_height, num_seqs)
        
        if original_ref >= 3 * ref_area:
            original_ref      = original_ref * 0.5
            bottom_adjustment = 0.25
            len_adjustment    = 0.9
        else:
            bottom_adjustment = 0.15
            len_adjustment    = 0.925

        ref_area        = original_ref
        sections        = ref_area - (ref_area * (0.01 * num_seqs))
        bottom          = figure_height - (figure_height * bottom_adjustment)
        adjusted_length = figure_height * len_adjustment
 
    else:
        adjusted_length = (figure_height - (2*offset))

    #order going from bottom to top
    for i, seq in enumerate(reversed_seqs):
        y_positions[seq] = bottom - (sections * i)
    #add ref at bottom
    y_positions[ref] = adjusted_length - (adjusted_length * 0.05)

    return sections, y_positions, leftmost_pos, ref_area, figure_height, enumeration_dict

def write_output(y_positions: dict, leftbound: int, rightbound: int, ref: str, 
                 alignments: dict, seq_lengths: dict, enumerating: bool, 
                 enumeration_dict: dict, grouping: bool):
    """write alignments to a tsv file"""

    record_nt = len(y_positions) - 1 #remove ref count

    #create header
    header = f"Sequence\tSequence_Length\tChrom\tFlag\tPosition\tPercent_Aligned\tClipped_Start\tClipped_End"
    if enumerating:
        header += "\tSeq_Num"
    if grouping:
        header += "\tGroup_Num"

    # reverse order of seqs to go from top to bottom
    seqs = list(y_positions.keys())[::-1]
    seqs.remove(ref)

    # now go through EACH alignment, and write out to output
    with open(f"Results_{record_nt}_records_{ref}_{leftbound}-{rightbound}.tsv", 'w') as out:
        out.write(header + '\n')
        for seq_id in seqs:
            seq_len = seq_lengths[seq_id]
            seq_alignments = alignments[seq_id]
            for algn in seq_alignments:
                percentage = round(algn.percent_aligned * 100, 2)
                outLine    = f"{seq_id}\t{seq_len}\t{algn.chromosome}\t{algn.flag}\t{algn.position}\t{percentage}\t{algn.clipping_start}\t{algn.clipping_end}"
                if enumerating:
                    outLine += f"\t{enumeration_dict[seq_id]}"
                if grouping:
                    outLine += f"\t{algn.group_num}"
                out.write(outLine + '\n')

def get_color(list_colors: bool, grouping: bool, group_num: int, color = "blue"):
    """return a color from the listed colors"""

            # [red, green, blue]
    colors = {"alizarin": [0.86, 0.18, 0.26], "azure": [0, 0.5, 1],
              "baikal": [0.082, 0.312, 0.515], "beaver": [0.62, 0.51, 0.44], "bittersweet": [0.99, 0.435, 0.368], "black": [0,0,0], "blue": [0,0,1],                  
              "cinnabar": [0.89, 0.26, 0.20], "crimson": [0.86, 0.08, 0.24], "cyan": [0,1,1],
              "darkcyan": [0.0, 0.55, 0.55], "darkorange": [1.0, 0.55, 0.0], "dodgerblue": [0.11, 0.56, 1.0],            
              "ecru": [0.76, 0.70, 0.50], "eucalyptus" : [0.15, 0.54, 0.35],
              "firebrick": [0.70, 0.13, 0.13], "forestgreen" : [0.13, 0.55, 0.13],
              "gold": [0.90, 0.75, 0.54], "green":[0,1,0],         
              "indigo": [0.29, 0, 0.51], "ivory": [1, 1, 0.94],
              "khaki": [0.94, 0.90, 0.55], "kobi": [0.91, 0.62, 0.77],
              "lava": [0.81, 0.06, 0.13], "lavender": [0.71, 0.49, 0.86], "liberty": [0.33, 0.35, 0.65], "lightseagreen": [0.12, 0.70, 0.67],
              "mango": [0.99, 0.75, 0.01], "maroon": [0.50, 0, 0], "milk": [0.914, 0.914, 0.914], "mint": [0.24, 0.71, 0.54],
              "orange": [1, 0.627, 0.063], "orchid": [0.85, 0.44, 0.84],      
              "peach": [1, 0.90, 0.71], "periwinkle": [0.80, 0.80, 1], "persimmon": [0.93, 0.35, 0], "pink": [1, 0.75, 0.80], "purple":[0.694, 0.612, 0.851],
              "red":[1,0,0], "redwood": [0.64, 0.35, 0.32], "ruby": [0.88, 0.07, 0.37], "rust": [0.72, 0.25, 0.05],
              "saffron": [0.96, 0.77, 0.19], "salmon": [0.98, 0.50, 0.45], "sapphire": [0.06, 0.32, 0.73], "scarlet": [1, 0.14, 0], "silver": [0.75, 0.75, 0.75], "snow": [1, 0.98, 0.98], "steelblue": [0.27, 0.51, 0.71], "strawberry": [0.98, 0.31, 0.33], "sunset": [0.98, 0.84, 0.65],
              "tan": [0.82, 0.71, 0.55], "teal": [0, 0.50, 0.50], "tomato": [1, 0.39, 0.28], "turquoise": [0.19, 0.84, 0.78],
              "vanilla": [0.95, 0.90, 0.67], "vermilion": [0.89, 0.26, 0.20], "viridian": [0.25, 0.51, 0.43],
              "wheat": [0.96, 0.87, 0.70], "white": [1.0, 1.0, 1.0], "wine": [0.45, 0.18, 0.22],                       
              "yellow": [1, 0.878, 0.125], "yellowgreen" : [0.60, 0.80, 0.20],   
              "zen": [0.83, 0.81, 0.68], "zomp": [0.22, 0.65, 0.56]}

    if list_colors:
        for color in colors.keys():
            print(color, end = ' ')
        print()
        sys.exit(0)
    
    color = color.lower()
    
    if not grouping:
        if color not in colors:
            options = ",".join([opt for opt in colors.keys()])
            sys.exit(f"{color} currently not available. Current options are: {options}")
        else:
            colr = colors[color]
            return Feature_Color(colr[0], colr[1], colr[2], 1, color)
    else:
        colors_list = list(colors.keys())
        color       = colors_list[group_num]
        colr        = colors[color]
        return Feature_Color(colr[0], colr[1], colr[2], 1.0, color)

def algn_color(flag: str):
    """determine the color of the sequence"""

    samflag = int(flag)

    # PE: R1 - green & R2 - blue
    if (samflag & 1) == 1:
        if (samflag & 64) == 64:
            seq_color = Feature_Color(28/255,172/255,120/255)
        elif (samflag & 128) == 128:
            seq_color = Feature_Color(0, 141/255, 249/255)
    # non paired end are grey for forward, orangy-yellow for reverse
    elif (samflag & 0) == 0:
        if (flag & 16) != 16:
            seq_color = Feature_Color(0.7, 0.7, 0.7)
        else:
            seq_color = Feature_Color(2.47, 1.27, 0)  
      
    return seq_color

def adjust_rightbound(ref: str, rightbound: int, alignment_map: str):
    """if rightbound is beyond length of reference, adjust rightbound"""

    # just another check to verify that the ref is indeed in the aligment map
    ref_found  = False
    cmd        = f"samtools view -H {alignment_map}"
    fh         = os.popen(cmd, 'r')
    ref_field  = f"SN:{ref}"
    rightbound = int(rightbound) # convert from float to int

    for line in fh:
        if line.startswith("@SQ"):
            fields = line.strip('\n').split('\t')
            if fields[1] == ref_field:
                ref_found = True
                ref_len   = int(fields[2].split(':')[1])
                if rightbound > ref_len:
                    print(f"Rightbound exceeds {ref}'s length. Setting rightbound to the end of {ref}")
                    rightbound = ref_len
                break
    
    fh.close()

    # if not found, go ahead and break
    if ref_found == False:
        msg = f"Did not find {ref} in {os.path.basename(alignment_map)}"
        sys.exit(msg)

    return rightbound


def adjust_klumps(clip_start: int, klump_start: int, klump_end: int, 
                  align_blocks: dict, block_del: dict, del_pos: dict, deletion_len: int):
    """adjust klump positions if gaps are present, return a list if split across blocks"""


    # move to where the clip is
    if clip_start != None:
        block_start = clip_start
    else:
        block_start = 0

    # objects to check logic of loop
    klump_start_set = False
    klump_end_set   = False
    klumps_list     = []
    added_len       = 0

    # get in case of a split & reversing
    # adding 0 to avoid using copy module
    k_start = klump_start + 0.0
    k_end   = klump_end + 0.0

    # add mini deletions to positions
    for pos, dlen in del_pos.items():
        if pos <= k_start and dlen < deletion_len:
            klump_start += dlen
        if pos <= k_end and dlen < deletion_len:
            klump_end += dlen

    # stop once we shifted over to the new positions
    for block, block_len in align_blocks.items():
        block_len = align_blocks[block]
        block_end = block_start + block_len
        if block_start <= klump_start <= block_end:
            klump_start_set = True
        if block_start <= klump_end <= block_end:
            klump_end_set   = True
        if klump_start_set:
            if klump_end_set:
                if block_start <= klump_start <= klump_end <= block_end:
                    klumps_list.append([klump_start, klump_end])
                    return klumps_list
            elif block_start <= klump_start <= block_end:
                klumps_list.append([klump_start, block_end])
                added_len += (block_end - klump_start)
            elif klump_start < block_start:
                klumps_list.append([block_start, block_end])
                added_len += (block_end - block_start)
        if klump_end_set:
            klumps_list.append([block_start, klump_end - added_len])
        deletion_len = block_del[block]
        block_start  = block_end + deletion_len
        if not klump_start_set:
            klump_start += deletion_len
        if not klump_end_set:
            klump_end += deletion_len

    return klumps_list

def find_overlap_labels(labels_list: list):
    """find overlapping labels based on their dimensions"""

    # each sub list will be an overlapping group
    overlaps_group = [[]]
    first          = True
    prev_start     = None
    prev_end       = None

    for label_arr in labels_list:
        start = label_arr[0]
        end   = label_arr[1]
        if first:
            first = False
            overlaps_group[0].append(label_arr)
        else:
            if (prev_start <= start <= prev_end) or \
                (prev_start <= end <= prev_end):
                # add to current subgroup
                overlaps_group[-1].append(label_arr)
            else:
                # new subgroup
                overlaps_group.append([label_arr])
        prev_start = start
        prev_end   = end

    return overlaps_group

def find_coordinates(x1: float, y1: float, width: float, height: float, direction: str):
    """given the position where the label will be drawn, return the coordinates of each corner"""

    # first, we need to get the first two points
    # angels are either 45 or -45 when converting to radians
    # but their absolute values is still 45
    # therefore
    # a = cos(ANGLE) * width
    # b = sin(ANGLE) * width
    #       .
    #      /|
    #     / |
    #  c /  | b
    #   /   |
    #  /    |
    # /_____|
    #    a  
    
    
    # since image dimensions are inverted (greater values -> further down)
    # direction matter, so we invert the angle
    if direction == 'F':
        rad = math.radians(45)
    elif direction == 'R':
        rad = math.radians(-45)

    cos_angle = math.cos(rad)
    sin_angle = math.sin(rad)
    center_x  = x1 + (width * 0.5 * cos_angle)   
    center_y  = y1 - (width * 0.5 * sin_angle)

    # get corners
    # x1 = center_x + (height / 2) * cos_angle - (width / 2) * sin_angle
    # y1 = center_y + (height / 2) * sin_angle + (width / 2) * cos_angle

    x2 = center_x - (height / 2) * cos_angle - (width / 2) * sin_angle
    y2 = center_y - (height / 2) * sin_angle + (width / 2) * cos_angle

    x3 = center_x - (height / 2) * cos_angle + (width / 2) * sin_angle
    y3 = center_y - (height / 2) * sin_angle - (width / 2) * cos_angle

    x4 = center_x + (height / 2) * cos_angle + (width / 2) * sin_angle
    y4 = center_y + (height / 2) * sin_angle - (width / 2) * cos_angle

    if direction == 'F':
        label_position = Label_Position(x1, y1, x2, y2, x3, y3, x4, y4)
    elif direction == 'R':
        label_position = Label_Position(x1, y1, x3, y3, x2, y2, x4, y4)

    return label_position

def overlapping_labels(label1_pos: Label_Position, label2_pos: Label_Position):
    """determine if two labels are overlapping"""

    # here, will implement the Separating Axis Theoreom (SAT)
    # to determine whether their is an overlap between the labels

    # helper functions to project points onto the axes
    # MDP = Make Dot Product
    def MDP(corner1: tuple, corner2: tuple):
        return (corner1[0] * corner2[0]) + (corner1[1] * corner2[1])
    
    # coords will contain all cordinates of the rectange in a single tuple
    def project_rect(axis: tuple, label_pos: Label_Position):
        t      = label_pos.make_tuple() # get tuple
        min_pt = min(MDP(t[0], axis), MDP(t[1], axis), MDP(t[2], axis), MDP(t[3], axis))
        max_pt = max(MDP(t[0], axis), MDP(t[1], axis), MDP(t[2], axis), MDP(t[3], axis))
        return (min_pt, max_pt)
    
    # create the axes
    label1_tup = label1_pos.make_tuple()
    label2_tup = label2_pos.make_tuple()

    axes = [(label1_tup[1][0] - label1_tup[0][0], label1_tup[1][1] - label1_tup[0][1]),
            (label1_tup[2][0] - label1_tup[1][0], label1_tup[2][1] - label1_tup[1][1]),
            (label2_tup[1][0] - label2_tup[0][0], label2_tup[1][1] - label2_tup[0][1]),
            (label2_tup[2][0] - label2_tup[1][0], label2_tup[2][1] - label2_tup[1][1])]
    
    # project the axes
    for a in axes:
        proj1 = project_rect(a, label1_pos)
        proj2 = project_rect(a, label2_pos)
        if (proj1[1] < proj2[0]) or (proj2[1] < proj1[0]):
            return False
    
    return True

def adjust_klump_labels(klump_labels: dict, exon_positions: list, direction: str):
    """shift the klump labels to avoid overlap with exon lables"""

    adjusted_positions = {} # {label : (label_position, width, height)}

    for klump_name, label_dim in klump_labels.items():
        x_start      = label_dim[0]
        label_width  = label_dim[1]
        y_start      = label_dim[2]
        label_height = label_dim[3]
        label        = label_dim[4]
        label_pos    = find_coordinates(x_start, y_start, label_width, label_height, direction)
        # make sure it has not move onto other adjusted labels
        for label2_tuple in adjusted_positions.values():
            label2_pos = label2_tuple[0]
            while (overlapping_labels(label_pos, label2_pos)):
                label_pos.shift_right(1) # shift 1 pixel to the right
        # if the label was shifted, we need to move it above any overlapping
        # exon labels
        for exon_loc in exon_positions:
            # x -> start, end
            # y -> bottom, top
            exon_start  = exon_loc[0]
            exon_end    = exon_loc[1]
            exon_bottom = exon_loc[2]
            exon_top    = exon_loc[3]
            exon_pos    = Label_Position(exon_start, exon_bottom, exon_end, exon_bottom,
                                      exon_end, exon_top, exon_start, exon_top)
            if overlapping_labels(label_pos, exon_pos):
                if direction == 'F':
                    if exon_top < exon_bottom:
                        y_start = exon_top - 2
                    else:   
                        y_start = exon_bottom - 2
                    label_pos.y1 = y_start # - (math.sin(45) * label_width)
                elif direction == 'R':
                    if exon_top < exon_bottom:
                        y_start = exon_bottom + 3
                    else:
                        y_start = exon_top + 3
                    label_pos.y1 = y_start # + (math.sin(45) * label_width)

        adjusted_positions[klump_name] = [label_pos, label_width, label_height, label]

    return adjusted_positions

########## plotting functions #############

def plot_seq(cairo_context, alignment: SAM, allocated_positions: float, seq_height: float,
              x_pos: float, overlap: bool, ref: str, leftbound: int, rightbound: int, section: float):
    """ plot sequence to scale to the longest sequence"""

    #get params
    align_blocks   = alignment.align_blocks.blocks
    block_del      = alignment.align_blocks.block_del
    covered_len    = alignment.align_blocks.covered_len
    ending_blocks  = alignment.align_blocks.get_ending_blocks()
    seq_id         = alignment.seq_name
    clipping_start = alignment.clipping_start
    adjust_start   = alignment.adjust_start
    clipping_end   = alignment.clipping_end
    adjust_end     = alignment.adjust_end
    seq_color      = alignment.seq_color

    # for clipping
    clipping_colors = {'S':   [0,1,0], #green
                       'H':   [1,0,0], #red
                        None: [0,0,0]} #black
    
    if len(ending_blocks) == 1:
        first_block = ending_blocks[0]
        last_block  = first_block
    else:
        first_block = ending_blocks[0]
        last_block  = ending_blocks[1]

    # make adjustments 0
    if adjust_start == None:
        adjust_start = 0
    if adjust_end == None:
        adjust_end   = 0

    # starting positions
    x1 = x_pos  # offset from left by x position
    y1 = seq_height  # y / vertical offset
    y2 = y1
    x2 = x_pos + (allocated_positions * covered_len)
    
    #check for clipping
    if clipping_start != None:
        clip_color = clipping_colors[clipping_start]
        clip_color.append(seq_color.alpha)
        clip_x_s   = x_pos + (allocated_positions * adjust_start) # go right after clip
        draw_borders(cairo_context, x_pos, clip_x_s, y1, clip_color, section)
    if clipping_end != None:
        clip_color = clipping_colors[clipping_end] 
        clip_color.append(seq_color.alpha)
        clip_x_e   = x2 - (allocated_positions * adjust_end) # go left of clip
        draw_borders(cairo_context, x2, clip_x_e, y1, clip_color, section)
        x2 = clip_x_e # replace to new end

    # draw the actual aligned portions & gaps
    for block, block_len in align_blocks.items():
        if clipping_start == None and clipping_end == None and len(align_blocks) == 1:
             # determine new x
            adjusted_start = x1
            adjusted_end   = x2
        else:
            if block == first_block:
                adjusted_start = x_pos + (allocated_positions * adjust_start)
                adjusted_end   = adjusted_start + (allocated_positions * block_len)
            elif block == last_block:
                adjusted_end = x2
            else:
                adjusted_end = adjusted_start + (allocated_positions * block_len)
       
        # if forward: grey else orangy-yellow, if overlapping, alpha 0.5 else 1
        if overlap:
            seq_color.alpha = 0.5
        if seq_id == ref:
            section = section * 1.25

        adjusted_height = section * 0.45
        top             = y1 - adjusted_height
        bottom          = y1 + adjusted_height
        cairo_context.move_to(adjusted_start, bottom) 
        cairo_context.line_to(adjusted_end, bottom)
        cairo_context.line_to(adjusted_end, top)
        cairo_context.line_to(adjusted_start, top)
        cairo_context.close_path()
        cairo_context.set_source_rgba(seq_color.red, seq_color.green, seq_color.blue, seq_color.alpha)
        cairo_context.fill_preserve()
        cairo_context.set_source_rgb(0, 0, 0)
        cairo_context.set_line_width((section * 0.05))
        cairo_context.stroke()
        
        # for plotting the deletions
        if block != last_block:
            del_start = adjusted_end
            del_end   = del_start + (allocated_positions * block_del[block])
            cairo_context.move_to(del_start, y1)
            cairo_context.line_to(del_end, y2)
            cairo_context.set_line_width(section * 0.25)
            cairo_context.set_source_rgba(0, 0, 0, seq_color.alpha) #black
            cairo_context.stroke()
            adjusted_start = del_end

    # add sequence name if not written
    if seq_id == ref:
        x, y = 50, seq_height - (seq_height * 0.05)

        cairo_context.set_source_rgb(0, 0, 0)
        cairo_context.set_font_size(0.75 * section) #used to be 75
        cairo_context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cairo_context.move_to(x, y)
        left   = "{:,}".format(leftbound)
        right  = "{:,}".format(rightbound)
        seq_id = f"{seq_id}: {left}-{right}"
        cairo_context.show_text(seq_id)
        cairo_context.stroke()
        return top, bottom
    else:
        return -1, -1

def draw_borders(cairo_context, x1: float, x2: float, y1: float, color: List, section: float):
    """draw borders for seq drawing"""

    adjusted_height = section * 0.45
    cairo_context.set_source_rgba(color[0], color[1], color[2], color[3])
    cairo_context.move_to(x1, y1 + adjusted_height) 
    cairo_context.line_to(x2, y1 + adjusted_height)
    cairo_context.line_to(x2, y1 - adjusted_height)
    cairo_context.line_to(x1, y1 - adjusted_height)
    cairo_context.close_path()
    cairo_context.set_line_width((section * 0.05))
    cairo_context.stroke()

def create_ticks(seq_length: int):
    """Find the appropriate marker lengths for tick marks"""

    marker_sets = {
        1e3:   ["bp", 100],
        5e3:   ["K", 1000],
        7.5e3: ["K", 1500],
        1e4:   ["K", 2000],
        2.5e4: ["K", 5000],
        5e4:   ["K", 10000],
        9e4:   ["K", 15000],
        1e5:   ["K", 20000],
        5e5:   ["K", 25000],
        9e5:   ["K", 30000],
        1e6:   ["M", 50000],
        5e6:   ["M", 70000],
        9e6:   ["M", 100000],
        1e7:   ["M", 150000],
        3e7:   ["M", 200000],
        5e7:   ["M", 500000],
        7e7:   ["M", 700000],
        9e7:   ["M", 900000],
        1e8:   ["M", 1000000],
        5e8:   ["M", 1500000],
        9e8:   ["M", 3000000],
        1e9:   ["M", 5000000],
              }

    multiplier = None

    for marker_length in marker_sets.keys():
        if seq_length <= marker_length:
            fields     = marker_sets[marker_length]
            multiplier = fields[1]
            break

    # multiplier will be used to show increments in bp length
    if multiplier != None:
        tick_ct = math.floor(seq_length/multiplier)
    else:
        sys.exit(f"Software was not prepared for sequence/segment of length {seq_length}")

    return tick_ct, multiplier

def draw_ticks(cairo_context, y_coordinate: float, seq_len: int, image_width: float, 
               x_pos: float, image_area: float, leftbound: int, section: float,
               tick_ct: int, multiplier: int):
    """add tick marks to the reference sequence"""

    # need to offset from the chrom lines
    mark_ypos1 = y_coordinate + (section * 0.55) # from chrom pos
    label_ypos = y_coordinate + (section * 1) # where the label is placed

    if tick_ct == None: # automatic calc
        tick_ct, multiplier = create_ticks(seq_len)

    # adjust for just ticks
    allocated_pos = (image_width / image_area) * \
        seq_len / (seq_len/multiplier)

    for i in range(1, tick_ct + 1):
        marker_num = i * multiplier  # interval scheme
        marker_num = marker_num + leftbound #adjust to ref
        # for rounding
        if marker_num < 1e3:
            # marker_num = marker_num/100
            marker = "bp"
        elif 1e3 <= marker_num < 1e6:
            marker_num = marker_num/1e3
            marker = "K"
        elif marker_num >= 1e6:
            marker_num = marker_num/1e6
            marker = "M" 
        marker_num   = round(marker_num, 2)
        marker_label = f"{marker_num}{marker}"
        marker_pos   = x_pos + (allocated_pos * i)
         # marker labels
        cairo_context.set_source_rgba(0, 0, 0, 1)
        cairo_context.set_font_size((section * 0.40))
        e          = cairo_context.text_extents(marker_label)
        label_xpos = marker_pos - (e.width / 2) # put it half way
        cairo_context.move_to(label_xpos, label_ypos) 
        cairo_context.show_text(marker_label)
        cairo_context.stroke()
        # now draw tick up to the top of the text
        top = label_ypos - e.height
        cairo_context.move_to(marker_pos, mark_ypos1)
        cairo_context.line_to(marker_pos, top)
        cairo_context.set_source_rgba(0, 0, 0, 1)  # black
        cairo_context.set_line_width(section * 0.05)
        cairo_context.stroke()

    return label_ypos
  
def plot_label(cairo_context, x: float, y: float, theta: float, label: str, midpoint: float, chrom_pos: float, klump_color: Feature_Color):
    """plot klump labels and the connecting dash line"""

    cairo_context.save()
    # create labels
    cairo_context.move_to(x, y)
    cairo_context.rotate(theta)
    cairo_context.set_source_rgb(0, 0, 0) # will always be black
    cairo_context.show_text(label)
    cairo_context.stroke()
    cairo_context.restore()

    # draw the line to the label from the ref sequence
    cairo_context.move_to(x, y)
    cairo_context.line_to(midpoint, chrom_pos)
    cairo_context.set_source_rgba(klump_color.red, klump_color.green, klump_color.blue, 0.50)
    cairo_context.set_line_width(1)
    cairo_context.set_dash([3.0, 1.0]) # same dash style as exons
    cairo_context.stroke()


def plot_klumps(cairo_context, y_coordinate: float, alignment: SAM, allocated_positions: float, 
                seq_klumps: dict, x_pos: float, overlap: bool, ref: str, leftbound: int,
                rightbound: int, section: float, klmp_color: Feature_Color, klump_colors: dict, 
                deletion_len: int, color_by_gene: bool, top_positions: list, bottom_positions: list,
                chrom_top_pos: float, chrom_bottom_pos: float, ylabel_pos: float, plt_height=None):
    """plot the klumps"""

    # fill in instead of making "klump"

    seq_name       = alignment.seq_name
    align_blocks   = alignment.align_blocks.blocks
    del_pos        = alignment.align_blocks.del_pos
    covered_len    = alignment.align_blocks.covered_len
    block_del      = alignment.align_blocks.block_del
    flag           = alignment.flag
    clipping_start = alignment.clipping_start
    adjust_start   = alignment.adjust_start
    clipping_end   = alignment.clipping_end
    adjust_end     = alignment.adjust_end
    seq_len        = alignment.seq_len

    # labels will alternate
    directions = ['F', 'R']
    i          = 0

    # will store x positions after drawing to
    # be the starting positions for the labels
    # before adjusting
    top_labels    = {}
    bottom_labels = {}
    midpoint_pos  = {} # store klump midpoint & klump color to connect line to label

    #remove tag if briding image
    for klump in seq_klumps[seq_name]:
        if klump.query_source == "None":
            continue
        # check if setting color to a new param
        if klump_colors != None:
            if klump.query_source in klump_colors:
                klmp_color = klump_colors[klump.query_source]
            elif color_by_gene:
                gene_name = '_'.join(klump.query_source.split('_')[:-1])
                if gene_name in klump_colors:
                    klmp_color = klump_colors[gene_name]
        if klump.pair_info:
            #check that klumps are with correct sequence
            if klump.pair_num != alignment.pair_num:
                    continue     
        #to avoid plotting klumps not in region of interest
        if seq_name != ref:
            if clipping_start == None:
                left_pos     = 0
                adjust_start = 0 # used when adjusting to x pos
            else:
                left_pos = adjust_start
            if clipping_end == None:
                right_pos = covered_len
            else:
                right_pos = covered_len - adjust_end
            # reverse klumps
            if (flag & 16) == 16:
                klump.start_pos = seq_len - klump.start_pos
                klump.end_pos   = seq_len - klump.end_pos
                # the end is now the start, and the start is now the end
                klump.start_pos, klump.end_pos = klump.end_pos, klump.start_pos
            # if out of range
            if left_pos <= klump.start_pos <= right_pos:
                if left_pos <= klump.end_pos <= right_pos:
                    pass
                else:
                    continue
            else:
                continue
            klumps_list = \
                adjust_klumps(adjust_start, klump.start_pos, klump.end_pos, 
                                align_blocks, block_del, del_pos, deletion_len)
            for klumps in klumps_list:
                klmp_start = klumps[0] 
                klmp_end   = klumps[1]
                # re-check if out of range after klumps are adjusted
                if left_pos <= klmp_start <= right_pos:
                    if left_pos <= klmp_end <= right_pos:
                        pass
                    else:
                        continue
                else:
                    continue
                if clipping_start == 'H':
                    klmp_start = klmp_start - adjust_start
                    klmp_end   = klmp_end - adjust_start
                # make height of seq
                fill_height = section * 0.425
                # added to fig
                _ = fill_in_matches(cairo_context, y_coordinate, x_pos,
                            allocated_positions, klmp_start, klmp_end,
                            overlap, fill_height, klmp_color)

        else:
            #filter out klumps out of range
            if leftbound <= klump.start_pos <= rightbound:
                if leftbound <= klump.end_pos <= rightbound:
                    pass
                else:
                    continue
            else:
                continue       
            #adjust by shifting leftbound             
            if (flag & 16) == 16:
                start_pos = (covered_len - klump.start_pos) - leftbound
                end_pos   = (covered_len - klump.end_pos) - leftbound
            else:
                start_pos = klump.start_pos - leftbound
                end_pos   = klump.end_pos - leftbound
            fill_height = section * 0.5315 # color up to borders
        # not a split klump
            k_midpoint = fill_in_matches(cairo_context, y_coordinate, x_pos,
                            allocated_positions, start_pos, end_pos,
                            overlap, fill_height, klmp_color)
            #check if vertical line for klumps
            if plt_height != None:
                if start_pos > end_pos:
                    vertical_start, vertical_end = end_pos, start_pos
                else:
                    vertical_start, vertical_end = start_pos, end_pos
                #make adjustments
                vertical_start = x_pos + (vertical_start * allocated_positions)
                vertical_end   =  x_pos + (vertical_end * allocated_positions)
                draw_vertical_line(cairo_context, vertical_start, vertical_end,
                                    y_coordinate, plt_height, klmp_color, fill_height)
            # set the dimensions prior to adjusting positions
            cairo_context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cairo_context.set_source_rgb(0, 0, 0)  # black
            cairo_context.set_font_size((section * 0.20))
            # create label
            klump_size = klump.klump_size
            query      = klump.query_source
            label      = f"{klump_size}-{query}"
            label_dim  = cairo_context.text_extents(label)
            # get the mid point of the text if i were not rotated
            start_pos      = x_pos + (start_pos * allocated_positions)
            end_pos        = x_pos + (end_pos * allocated_positions)
            klump_midpoint = (end_pos + start_pos) / 2
            direction      = directions[i % 2]
            i += 1
            if direction == 'F':
                y_pos = chrom_top_pos - 2
                # y_pos = yLabel - (section * 0.75)
                top_labels[klump.klump_name] = (klump_midpoint, label_dim.width, y_pos, label_dim.height, label)
            elif direction == 'R':
                y_pos = ylabel_pos + 2
                # y_pos = yLabel + (section * 0.75)
                bottom_labels[klump.klump_name] = (klump_midpoint, label_dim.width, y_pos, label_dim.height, label)
            midpoint_pos[klump.klump_name] = (k_midpoint, klmp_color) # store the midpoint for later
      
    # if ref, we may plot labels
    if seq_name == ref:
        # adjust the labels to prevent overlaps
        adjusted_tops    = adjust_klump_labels(top_labels, top_positions, 'F')
        adjusted_bottoms = adjust_klump_labels(bottom_labels, bottom_positions, 'R')
 
        # now to plot the labels and the lines
        # if they are empty, no elements will be returned

        for klump_name, label_dim in adjusted_tops.items():
            x1, y1                 = label_dim[0].x1, label_dim[0].y1
            label                  = label_dim[3]
            k_midpoint, klmp_color = midpoint_pos[klump_name]
            plot_label(cairo_context, x1, y1, math.radians(-45), label, k_midpoint, chrom_top_pos, klmp_color)
        
        for klump_name, label_dim in adjusted_bottoms.items():
            x1, y1                 = label_dim[0].x1, label_dim[0].y1
            label                  = label_dim[3]
            k_midpoint, klmp_color = midpoint_pos[klump_name]
            plot_label(cairo_context, x1, y1, math.radians(45), label, k_midpoint, chrom_bottom_pos, klmp_color)
            

def plot_exons(cairo_context, y_coordinate: float, exons: dict, allocated_positions: float,
               chrom_top: float, chrom_bottom: float, x_pos: float, leftbound: int, section: float, 
               ylabel_pos: float, plot_height: float, pdf_height: float):
    """plot the exons onto the reference"""

    # will be used to avoid plotting the same gene twice
    current_gene  = None
    prev_color    = None # as a safety measure
    label_height  = -float("inf")
    bottom_labels = [] # will be used to know where labels start/end
    top_labels    = []
    i             = 0 # used to assign direction
    directions    = ['+', '-']

    cairo_context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,
                                   cairo.FONT_WEIGHT_NORMAL)
    cairo_context.set_font_size((section * 0.25))

    # sort exons
    exons = dict(sorted(exons.items(), key = lambda exon: exon[1].start_pos))

    # plot ONLY the annotations onto the chrom
    for exon in exons.values():
        #adjust by shifting
        start_pos = exon.start_pos - leftbound
        end_pos   = exon.end_pos - leftbound
        # direction = exon.direction
        fill_in_annotation(cairo_context, y_coordinate, x_pos,
                           allocated_positions, start_pos, end_pos,
                           section, "exon", None, exon.gene_color)
        
        # check for vertical lines
        if plot_height != None:
            fill_height = section * 0.515
            start       = x_pos + (start_pos * allocated_positions)
            end         = x_pos + (end_pos * allocated_positions)
            draw_vertical_line(cairo_context, start, end, y_coordinate, plot_height, exon.gene_color, fill_height)

        # plot label based on direction
        if (current_gene != exon.gene_name) and (prev_color != exon.gene_color.name):
            current_gene = exon.gene_name
            prev_color   = exon.gene_color.name
        else:
            continue

        t_dim        = cairo_context.text_extents(current_gene)   
        label_height = max(label_height, t_dim.height)
        direction    = directions[i % 2]

        if direction == '-':
            start = x_pos + (start_pos * allocated_positions) # dash at start of label
            end   = start + t_dim.width
            bottom_labels.append([start, end, exon.gene_name, exon.gene_color])
        elif direction == '+':
            end   = x_pos + (start_pos * allocated_positions) # dash at end of label
            start = end - t_dim.width
            top_labels.append([start, end, exon.gene_name, exon.gene_color])
        i += 1

    # now to find the overlapping text
    overlap_groups_bottom = find_overlap_labels(bottom_labels)
    overlap_groups_top    = find_overlap_labels(top_labels)

    # used for klump labels
    top_positions    = []
    bottom_positions = []

    # now to draw the labels

    for i, labels_list in enumerate([overlap_groups_top, overlap_groups_bottom]):
        direction = directions[i]
        for label_sub_list in labels_list:
            if direction == '-':
                ybottom = ylabel_pos # + t_dim.height + 2
                label_sub_list.reverse() # only reverse if drawing on bottom
            elif direction == '+':
                ybottom = chrom_top - 1
            for j, sub_list in enumerate(label_sub_list, start = 1):
                x_position = sub_list[0] # will shift to prevent dash line overlap
                
                if direction == '+':
                    y_position  = ybottom - (label_height * j)
                    top_y       = y_position
                    bottom_y    = chrom_top - 1
                    x_position -= 1
                    dash_xpos   = sub_list[1]
                elif direction == '-':
                    y_position  = ybottom + (label_height * j)
                    top_y       = chrom_bottom + ((section * 0.025))
                    bottom_y    = y_position - label_height + ((section * 0.05))
                    x_position += 1
                    dash_xpos   = sub_list[0]

                label = sub_list[2]
                cairo_context.move_to(x_position, y_position)
                cairo_context.set_source_rgb(0, 0, 0)
                cairo_context.show_text(label)
                cairo_context.stroke()
                label_dim   = cairo_context.text_extents(label)
                x_end       = x_position + label_dim.width
                y_top_label = y_position - label_dim.height
                if direction == '+':
                    top_positions.append((x_position, x_end, y_position, y_top_label))
                elif direction == '-':
                    bottom_positions.append((x_position, x_end, y_position, y_top_label))
                # now for the line
                # print(direction, top_y, bottom_y, y_position - label_height)
                cairo_context.move_to(dash_xpos, top_y) # where top of dash starts
                cairo_context.line_to(dash_xpos, bottom_y) # move down to this y pos
                gene_color = sub_list[3]
                cairo_context.set_source_rgb(gene_color.red, gene_color.green, gene_color.blue)
                cairo_context.set_line_width(1)
                cairo_context.set_dash([3.0, 1.0]) # dashes
                cairo_context.stroke()
    
    return top_positions, bottom_positions

def plot_gaps(cairo_context, y_coordinate: float, gaps: List, allocated_positions: float, 
              x_pos: float, leftbound: int, section: float, plt_height: float):
    """plot the genes onto the reference"""

    # fill in where the gaps are located

    for gap in gaps:
        #adjust by shifting leftbound
        start_pos = gap.start_pos - leftbound
        end_pos   = gap.end_pos - leftbound
        fill_in_annotation(cairo_context, y_coordinate, x_pos,
                           allocated_positions, start_pos, end_pos,
                            section, "gap", plt_height)

def fill_in_matches(cairo_context, y: float, x_pos: float, allocated_pos: float, 
                    klump_start: float, klump_end: float, overlap: bool, \
                    fill_height: float, klmp_color: Feature_Color):
    """fill in seq with klump positions"""

    # checking for overlap (default is alpha = 1)
    if overlap:
        klmp_color.alpha = 0.5
    # in case of reverse aligned
    if klump_start > klump_end:
        klump_start, klump_end = klump_end, klump_start

    #make adjustments
    klump_start = x_pos + (klump_start * allocated_pos)
    klump_end   = x_pos + (klump_end * allocated_pos)

    #plot
    cairo_context.move_to(klump_start, y - fill_height)
    cairo_context.line_to(klump_end, y - fill_height)
    cairo_context.line_to(klump_end, y + fill_height)
    cairo_context.line_to(klump_start, y + fill_height)
    cairo_context.close_path()
    cairo_context.set_source_rgba(klmp_color.red, klmp_color.green, klmp_color.blue, klmp_color.alpha)
    cairo_context.fill()

    # get the midpoint for drawing the line
    return (klump_end + klump_start) / 2

def fill_in_annotation(cairo_context, y: float, x_pos: float, allocated_pos: float, 
                       start_pos: float, end_pos: float, section: float, an_type: str,
                       plt_height = None, ex_color = None):
    """fill in seq with inputted annotations"""

    # color is a violet if gene, transparent black if gap
    if an_type == "exon":
        color = ex_color
    elif an_type == "gap":
        color = Feature_Color(0,0,0,0.5)
    #fill height
    fhght = section * 0.5315

    #adjust positions
    start_pos = x_pos + (start_pos * allocated_pos)
    end_pos   = x_pos + (end_pos * allocated_pos)

    #plt
    cairo_context.move_to(start_pos, y - fhght)
    cairo_context.line_to(end_pos, y - fhght)
    cairo_context.line_to(end_pos, y + fhght)
    cairo_context.line_to(start_pos, y + fhght)
    cairo_context.close_path()
    cairo_context.set_source_rgba(color.red, color.green, color.blue, color.alpha)
    cairo_context.fill()

    #check if vertical line
    if an_type == "gap" and plt_height != None:
        draw_vertical_line(cairo_context, start_pos, end_pos, y, plt_height, color, fhght)

def draw_vertical_line(cairo_context, start_pos: float, end_pos: float, y_pos: float, 
                       plt_height: int, color: Feature_Color, fill_height: float):
    """draw vertical line above annotation"""

    # dash line start = midpoint of gap, widths extend <- & ->
    dash_start = start_pos + ((end_pos - start_pos)/2)
    cairo_context.set_line_width(end_pos - start_pos)
    cairo_context.set_dash([15.0, 5.0])
    cairo_context.move_to(dash_start, plt_height)
    cairo_context.line_to(dash_start, y_pos - fill_height)
    cairo_context.set_source_rgba(color.red, color.green, color.blue, 0.25)
    cairo_context.stroke()

def enumerate_seqs(cairo_context, ypos: float, xpos: float, section: float, seq_num: int):
    """enumerate sequences onto the figure"""

    # set the dimensions of the text & then place
    num_label = str(seq_num)
    cairo_context.set_source_rgb(0, 0, 0)
    cairo_context.set_font_size(0.75 * section)
    cairo_context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    label_dim = cairo_context.text_extents(num_label)
    x         = xpos - (label_dim.width * 1.2) # by 1/5th of the text label
    y         = ypos + (label_dim.height * 0.75)
    cairo_context.move_to(x, y)
    cairo_context.show_text(num_label)
    cairo_context.stroke()

def plot_sequences(alignments: dict, seq_lengths: dict, seq_klumps: dict, ref: str,
                   leftbound: int, rightbound: int, overlaps: dict, annotation: str,
                   vertical_line_exons: bool, gap_file: str, figure_height: int, figure_width: int, 
                   write_table: bool, enumerating: bool, klmp_color: Feature_Color, klump_colors: dict, 
                   color_by_gene: bool, vertical_line_gaps: bool, vertical_line_klumps: bool, 
                   deletion_len: int, group_seqs: bool, write_seqs: bool, outformat: str,
                   tick_count: int, tick_span: int):
    """plot alignments given all the annotations"""

    print("Plotting..")

    # set up the plot given the number of sequences and their aligment positions
    section, y_positions, leftmost_pos, \
        ref_area, figure_height, enumeration_dict = \
             set_up_plt(figure_height, alignments, ref, leftbound, enumerating)
    
    # below functions take dimensions as an int, so will do a conversion to be safe
    figure_height = int(figure_height)
    figure_width  = int(figure_width)
    
    # determine what format to draw to when creating the image surface
    if outformat == "pdf":
       ims = cairo.PDFSurface(f"Alignment_{ref}_{leftbound}-{rightbound}.pdf",
                               figure_width, figure_height)
    elif outformat == "png":
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, figure_width, figure_height)
    elif outformat == "svg":
        ims = cairo.SVGSurface(f"Alignment_{ref}_{leftbound}-{rightbound}.svg",
                               figure_width, figure_height)


    # will also write seqs from this function
    if write_seqs:
        outfh = open(f"Alignment_{ref}_{leftbound}-{rightbound}.fa", 'w')
        
    cairo_context = cairo.Context(ims)

    # offset by starting positions on both sides
    image_width = figure_width - (2*(figure_width * 0.025)) 

    # get x positions
    image_area  = scale_image_width(alignments, leftmost_pos, rightbound)
    x_positions = defaultdict(dict) 
    for seq, alignment_list in alignments.items():
        for algn in alignment_list:
            x_positions[seq][algn.map_num] = adjust_x(
                image_width, seq, alignments, leftmost_pos, leftbound, algn.position,\
                     image_area, figure_width, algn.clipping_start, algn.adjust_start)

    # create allocated posititions for sites
    allocated_pos = {}
    for aligns in alignments.values():
        for algn in aligns:
            allocated_pos[algn.map_num] = (
                (image_width/image_area) * algn.aligned_length) / algn.aligned_length
    #add ref
    allocated_pos[ref] = (
        (image_width/image_area) * seq_lengths[ref]) / seq_lengths[ref]
    ref_block = algn_blocks()
    ref_block.add_entry(0, [rightbound - leftbound], 0, 0)
    ref_block.covered_region(0, 0)
    ref_record = SAM(ref, leftbound, 0, ref, False, ref_block,
                          None, None, None, None, 100.0, rightbound - leftbound, True)
    ref_record.seq_color = Feature_Color(0.7, 0.7, 0.7) #light grey
    alignments[ref] = ref_record
    x_positions[ref]["alignment-0"] = adjust_x(image_width, ref, alignments, 
                                               leftmost_pos, leftbound,
                                               alignments[ref].position, image_area, 
                                               figure_width, None, 0)

    #avoid enumerating >1x
    if enumerating:
        enumerated = set()

    #save a irrelevant amount of time
    if type(seq_klumps) == dict:
        drawing_klumps = True
    else:
        drawing_klumps = False

    for algnments in alignments.values():
        # skip seqs not kept
        if type(algnments) == list:
            for algn in algnments:
                if algn.seq_name not in y_positions:
                    continue
                seq_name = algn.seq_name
                _, _ = plot_seq(cairo_context, algn, allocated_pos[algn.map_num],
                         y_positions[seq_name], x_positions[seq_name][algn.map_num], 
                         overlaps[seq_name], ref, leftbound, rightbound, section)
                if enumerating and seq_name not in enumerated:
                   enumerate_seqs(cairo_context, y_positions[seq_name], x_positions[seq_name][algn.map_num],
                                  section, enumeration_dict[seq_name])
                   enumerated.add(seq_name) 
                if drawing_klumps and seq_name in seq_klumps:
                    plot_klumps(cairo_context, y_positions[seq_name], algn, 
                                allocated_pos[algn.map_num], seq_klumps, x_positions[seq_name][algn.map_num],
                                overlaps[seq_name], ref, leftbound, rightbound, section, klmp_color, klump_colors, 
                                deletion_len, color_by_gene, [], [], 0, 0, 0) # no exon labels will be passed here
                if write_seqs:
                    if algn.IsPrimary:
                        outfh.write(f">{seq_name}\n{algn.seq}\n")
                
        else:
            # if reference seq, seqs are type list
            seq_name = algnments.seq_name
            top, bottom = plot_seq(cairo_context, algnments, allocated_pos[algn.map_num],
                     y_positions[seq_name], x_positions[seq_name]["alignment-0"], False, 
                     ref, leftbound, rightbound, ref_area)
            ylabel_pos = draw_ticks(cairo_context, y_positions[seq_name],
                       seq_lengths[ref], image_width, x_positions[seq_name]["alignment-0"], 
                       image_area, leftbound, ref_area, tick_count, tick_span)
            if annotation != None:
                exons = parse_annotation_file(annotation, leftbound, rightbound, ref)
                if vertical_line_exons:
                    plt_height = min(y_positions.values())
                else:
                    plt_height = None
                # tp = top positions
                # bp = bottom positions
                tp, bp = plot_exons(cairo_context, y_positions[seq_name], exons, allocated_pos[ref], 
                           top, bottom, x_positions[seq_name]["alignment-0"], leftbound, 
                           ref_area, ylabel_pos, plt_height, figure_height)
            else:
                tp, bp = [], [] # no labels
            if gap_file != None:
                gaps = parse_gap_file(gap_file, ref, leftbound, rightbound)
                if vertical_line_gaps:
                    plt_height = min(y_positions.values())
                else:
                    plt_height = None
                plot_gaps(cairo_context, y_positions[seq_name], gaps, allocated_pos[ref],
                          x_positions[seq_name]["alignment-0"], leftbound, ref_area, 
                          plt_height)
            if drawing_klumps and seq_name in seq_klumps:
                #check and if not, revert
                if vertical_line_klumps:
                    plt_height = min(y_positions.values())
                else:
                    plt_height = None
                plot_klumps(cairo_context, y_positions[seq_name], algnments, allocated_pos[ref], seq_klumps, 
                            x_positions[seq_name]["alignment-0"], False, ref, leftbound, rightbound, 
                            ref_area, klmp_color, klump_colors, deletion_len, color_by_gene, tp, bp, 
                            top, bottom, ylabel_pos, plt_height)
    # finish plot
    if outformat == "pdf":
        cairo_context.show_page()
    elif outformat == "png":
        ims.write_to_png(f"Alignment_{ref}_{leftbound}-{rightbound}.png")
    elif outformat == "svg":
        ims.finish()
        ims.flush()

    # finish fa if needed
    if write_seqs:
        outfh.close()

    # check if writing tsv
    if write_table:
        write_output(y_positions, leftbound, rightbound, ref, 
                        alignments, seq_lengths, enumerating, 
                        enumeration_dict, group_seqs)

def Alignment_Plot(args):
    """Parse, plot, and pray for good results"""

    # get arguments
    align_map, klump_file, ref, leftbound, rightbound, view_len, min_len, \
    klmp_size, percent, max_per, annotation, vertical_line_exons, figure_height, \
    figure_width, write_table, supplementary, gap_file, plotting_list, \
    enumerating, secondary, paired_end, klmp_color, klump_colors, color_by_gene, \
    vertical_line_gaps, vertical_line_klumps, no_primary, outformat, group_seqs, \
    deletion_len, align_offset, clip_tolerance, t_len, t_per, \
    per_overlap, del_tolerance, group_dels, write_groups, min_grp, \
    write_seqs, write_edge_seqs, limit, no_subsample, tick_count, tick_span = check_args(args)
 
    # klump info & seq lengths
    seq_klumps, seq_lengths = parse_klumps_out(klump_file, min_len, klmp_size, paired_end)

    # check for specific klump colors
    if klump_colors != None:
        klump_colors = parse_klump_color_list(klump_colors)

    # alignment info
    print(f"Parsing {os.path.basename(align_map)}")
    alignments, figure_height, figure_width, seq_lengths = \
        parse_sam(align_map, ref, leftbound, rightbound, min_len, seq_lengths, percent, 
                  max_per, figure_height, figure_width, supplementary, plotting_list, secondary,
                  no_primary, limit, no_subsample, paired_end, deletion_len, group_seqs, view_len, write_seqs)

    # check if grouping sequences
    if group_seqs:
        if seq_klumps != None:
            klump_info = True
        else:
            klump_info = False
            seq_klumps = {}
        alignments = \
            Group_Seqs(alignments, leftbound, rightbound, ref, align_offset, clip_tolerance,
                        del_tolerance, per_overlap, klump_info, seq_klumps, t_len, t_per, 
                        group_dels, write_groups, min_grp, write_edge_seqs, limit, False)
    # find if there are overlaps for coloration
    overlaps = identify_overlaps(alignments)
    # plot
    plot_sequences(alignments, seq_lengths, seq_klumps, ref, leftbound, 
                   rightbound, overlaps, annotation, vertical_line_exons, gap_file,
                   figure_height, figure_width, write_table, enumerating, klmp_color, 
                   klump_colors, color_by_gene,  vertical_line_gaps, vertical_line_klumps, 
                   deletion_len, group_seqs, write_seqs, outformat, tick_count, tick_span)
