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
import gc
import os
import copy
import multiprocessing
import gzip
from  .Classes        import SAM, SAM_FLAG, GENE, GeneRecord
from  .alignment_plot import estimate_seq_length, parse_cigar, group_assert, percent_check
from  .grouping       import Group_Seqs, within_window


def clear_dict(map_dict: dict):
    """currently a temporary fix to remove possible circular references"""

    for v in map_dict.values():
        v.clear()
    map_dict.clear()
    map_dict = None # deallocate pointer

######### parsing functions ############

def parse_sam_header(align_map: str, window_size: int, num_of_threads: int):
    """get the lengths of each ref seq in order to establish scanning scheme"""

    ref_seqs      = {} # will sort to run largest chroms 1st
    ref_seqs_list = [] # for preserving initial order when writing
    threads_list  = [[] for _ in range(num_of_threads)]

    # just get the header
    cmd = f"samtools view -H {align_map}"
    fh  = os.popen(cmd, 'r')

    skip_cnt = 0
    total_bp = 0

    for line in fh:
        if line.startswith("@SQ"):
            # expected format:
            # @SQ\tSN:Seq_Name\tLN:Seq_Len
            fields   = line.strip('\n').split('\t')
            seq_name = fields[1]
            seq_name = seq_name.replace("SN:", '')
            seq_len  = fields[2]
            seq_len  = int(seq_len.replace("LN:", ''))
            if seq_len < window_size:
                skip_cnt += 1
                continue
            ref_seqs[seq_name] = seq_len
            total_bp += seq_len
            ref_seqs_list.append(seq_name)
    
    if skip_cnt > 0:
        seq_str = "reference sequence"
        if skip_cnt > 1:
            seq_str += 's'
        ws = f"{window_size:,}"
        print(f"Ignoring {skip_cnt} {seq_str} shorter than window size of {ws} bp", flush=True)

    slen = f'{total_bp:,}' # scanned length
    print(f"Identified {len(ref_seqs)} reference sequences composed of {slen} bp")
    
    fh.close()

    # now sort
    sorted_refs = [(ref, rlen) for ref, rlen in sorted(ref_seqs.items(), key = lambda item:item[1], reverse = True)]

    for i, ref_tuple in enumerate(sorted_refs):
        threads_list[i % num_of_threads].append(ref_tuple)

    return threads_list, ref_seqs_list

def check_args(args):
    """determine if params are acceptable"""

    warning_color = "\033[93m"
    end_color = "\033[0m"

    # check if alignment file exists and samtools is in path
    if args.alignment_map == None:
        msg = "--alignment_map SAM/BAM file is required for scan_alignment"
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

    # check window params
    assert args.window_size > 0, "--window_size must be greater than 0"
    assert args.window_step > 0, "--window_step must be greater than 0"
    args.window_size = int(args.window_size)
    args.window_step = int(args.window_step)

    # if a gtf/gff3 is supplied, only report windows where a gene is found   
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
                print(f"{warning_color}{msg}{end_color}", flush=True)
        else:
            sys.exit(f"Could not find {args.annotation}")

    # convert min_len to int
    args.min_len = int(args.min_len)

    # other params to verify
    args.deletion_len   = group_assert(args.deletion_len, "Deletion length")
    args.align_offset   = group_assert(args.align_offset, "Alignment Offset")
    args.min_len        = group_assert(args.min_len, "Minimum length")
    args.clip_tolerance = group_assert(args.clip_tolerance, "Clip tolerance")
    args.del_tolerance  = group_assert(args.del_tolerance, "Deletion tolerance")
    args.t_len          = group_assert(args.t_len, "Trustworthy length")
    args.min_grp        = group_assert(args.min_grp, "Minimum group")
    args.num_of_groups  = group_assert(args.num_of_groups, "Number of groups")
    assert args.limit  >= 0, "--limit must be >= 0"
    
    # check other boolean params
    assert type(args.supplementary)      is bool, "--supplementary does not taken any positional values"
    assert type(args.secondary)          is bool, "--secondary does not take any positional values"
    assert type(args.assume_sep_del)     is bool, "--assume_sep_del does not take any positional values"
    assert type(args.flag_excess_groups) is bool, "--flag_excess_groups does not take any positional values"

    #check for percentages
    msg = "Minimum mapping"
    args.min_percent = percent_check(args.min_percent, msg)
    msg = "Minimum percent for trusting a sequence when grouping"
    args.t_per = percent_check(args.t_per, msg)
    msg = "Minimum percent for confidently grouping two sequences"
    args.per_overlap = percent_check(args.per_overlap, msg)
    
    msg = f"WARNING: Grouping Sequences currently only uses primary alignments. " 
    if args.supplementary == args.secondary == True:
        msg = msg + "Excluding supplementary and secondary alignments"
        print(f"{warning_color}{msg}{end_color}", flush=True)
        args.supplementary = False
        args.secondary = False
    elif args.supplementary:
        msg = msg + "Excluding supplementary alignments"
        print(f"{warning_color}{msg}{end_color}", flush=True)
        args.supplementary = False
    elif args.secondary:
        msg = msg + "Excluding secondary alignments"
        print(f"{warning_color}{msg}{end_color}", flush=True)
        args.secondary = False
    if args.paired:
        msg = "WARNING: scan_alignments currently only supports non-paired-end sequences"
        print(f"{warning_color}{msg}{end_color}", flush=True)
        args.group_seqs = False

    # check threads
    assert args.threads > 0, "--threads must be greater than 0"
    if args.threads > os.cpu_count():
        msg = f"Detected only {os.cpu_count()} threads. Reducing --threads count"
        print(f"{warning_color}{msg}{end_color}")
        args.threads = os.cpu_count()

    return args.alignment_map, args.annotation, args.min_len, args.min_percent, \
           args.deletion_len, args.align_offset, args.clip_tolerance, args.t_len, args.t_per, \
           args.per_overlap, args.del_tolerance, args.assume_sep_del, args.min_grp, \
           args.window_size, args.window_step, args.num_of_groups, args.threads, args.limit, \
           args.flag_excess_groups

def get_genes(annotation: str, ref_lists: list):
    """return a dictionary of genes that will be used to only report windows of interest"""

    print(f"Parsing {annotation}")

    # check which fields will be sought for

    genome_genes = {}
    # will use a set to avoid duplciates
    rec_types    = ["gene", "mrna"]
    visited      = set()

    # collapse the lists of lists to a single "list"
    ref_seqs = set()
    for ref_list in ref_lists:
        for ref_tuple in ref_list:
            ref_seqs.add(ref_tuple[0])

    fh = gzip.open(annotation, "rt") if annotation.endswith(".gz") else open(annotation, 'r')

    gene_record = GeneRecord()

    gene_count = 0 # used to track total num of annotations
    
    for line in fh:
        if line[0] == '#':
            continue
        fields = line.strip('\n').split('\t')
        chr = fields[0]
        # only keep genes for seqs being scanned
        if chr not in ref_seqs:
            continue
        if fields[2].lower() in rec_types:
            chr = fields[0]
            # ignoring direction for window scanning
            start     = int(fields[3])
            end       = int(fields[4])
            direction = fields[6]
            if (start, end, direction) in visited:
                continue
            visited.add((start, end, direction))
            gene_record.parse_attributes(fields[8])
            gene_name = gene_record.get_gene_name()
            gene = GENE(start, end, gene_name)
            gene_count += 1
            if chr not in genome_genes:
                genome_genes[chr] = [gene]
            else:
                genome_genes[chr].append(gene)
            gene_record.clear() # reset names

    fh.close()

    gene_ct = f"{gene_count:,}"
    print(f"Found {len(genome_genes)} out of {len(ref_seqs)} reference sequences with annotations")
    print(f"A total of {gene_ct} annotations will be used to anchor windows")

    return genome_genes

def genes_in_window(window_start: int, window_end: int, genes_list: list):
    """move onto window where there is a gene"""

    genes = []

    for gene in genes_list:
        if window_start <= gene.start_pos <= window_end:
            genes.append(gene.gene_name)
        elif window_start <= gene.end_pos <= window_end:
            genes.append(gene.gene_name)
        # TODO: consider removing these two checks
        # they seem redundant
        elif gene.start_pos <= window_start <= gene.end_pos:
            genes.append(gene.gene_name)
        elif gene.start_pos <= window_end <= gene.end_pos:
            genes.append(gene.gene_name)
        
    return genes

def process_window(alignments: dict, window_start: int, window_end: int, ref: str, 
                   align_offset: int, clip_tolerance: int, del_tol: int, per_overlap: float,
                   t_len: int, t_per: float, group_dels: bool, min_grp: int, 
                   num_of_groups: int, using_genes: bool, chr_genes: list, 
                   limit: int, flag_excess_groups: bool, outfh):
    """will determine if the current window will be written to output"""

    # assume we will group the sequences
    will_group = True

    if using_genes: # if only reporting regions with genes
        if chr_genes != None:
            genes = genes_in_window(window_start, window_end, chr_genes)
            if len(genes) == 0:
                will_group = False # no genes here
        else:
            will_group = False # no genes in this ref seq
    
    if will_group: # okay-ed to group
        group_count = Group_Seqs(alignments, window_start, window_end, ref, align_offset,
                                   clip_tolerance, del_tol, per_overlap, False,
                                   {}, t_len, t_per, group_dels, False, min_grp, False,
                                   limit, True)
 
        # not able to be tiled or if reporting regions with >N groups
        if (group_count < 0 or (flag_excess_groups and abs(group_count) >= num_of_groups)):
            group_count = abs(group_count)
            endl  = '\n'
            
            if using_genes:
                # add genes to outline
                endl = '\t' + ','.join(genes) + '\n' 

            if (flag_excess_groups):
                tiled = 'F' if (group_count < 0) else 'T'
                outline = f"{ref}\t{window_start}\t{window_end}\t{tiled}\t{group_count}{endl}"
            else:
                outline = f"{ref}\t{window_start}\t{window_end}\t{group_count}{endl}"

            # assume file handle is open
            try:
                outfh.write(outline)
                outfh.flush() 
            except:
                # open file
                outfh = open(f"Temp_{ref}.txt", 'w')
                outfh.write(outline)
                outfh.flush() 

    # return it just in case
    return outfh

def scan_align_map(align_map: str, ref_list: list, window_size: int, window_step: int,
                   min_len: int, min_percent: float, limit: int, deletion_len: int,
                   min_grp: int, num_of_groups: int, align_offset: int, clip_tolerance: int, 
                   del_tol: int, per_overlap: float, t_len: int, t_per: int, group_dels: bool,
                   using_genes: bool, flag_excess_groups: bool, ref_genes: dict):
    """go through the alignment bam and look for regions that may be missassembled"""

    for ref_tuple in ref_list:
        ref     = ref_tuple[0]
        ref_len = ref_tuple[1]
        # delete previous temps if they are still present
        if os.path.isfile(f"Temp_{ref}.txt"):
            os.remove(f"Temp_{ref}.txt")
        if using_genes:
            chr_genes = ref_genes[ref] # get the genes once
        else:
            chr_genes = None
        
        # set up the parameters
        outfh            = None # only open file if missassembled region found
        tmp              = None # will be used to hold next window sam records
        window_start     = 0
        window_end       = window_size + 0
        cmd              = f"samtools view {align_map} " + f'"{ref}' + '"'
        alignments       = {}
        next_window_seqs = list()
        fh = os.popen(cmd, 'r')

        # now go in and slide through the alignments
        for line in fh:
            if window_start == 4800000:
                fff = copy.deepcopy(alignments)
            if line.startswith('@'):
                continue
            fields = line.strip('\n').split('\t')
            seq_name = fields[0]
            seq_flag = int(fields[1])
            sam_flag = SAM_FLAG(seq_flag)
            # only primary seqs are used for grouping
            if not sam_flag.primary:
                continue
            seq_cigar    = fields[5]
            leftmost_pos = int(fields[3])
            seq_length   = estimate_seq_length(seq_cigar)
            # filtering for unreliable alignments is still applied
            if seq_length < min_len:
                continue
            align_len, clipping_start, adjust_start, clipping_end, \
                adjust_end, align_blocks = parse_cigar(seq_cigar, deletion_len)
            if adjust_start == None:
                clipped_start = 0
            else:
                clipped_start = adjust_start
            if adjust_end == None:
                clipped_end = seq_length
            else:
                clipped_end = seq_length - adjust_end
            percent_aligned = (clipped_end - clipped_start)/seq_length
            if percent_aligned < min_percent:
                continue
            if align_len == seq_length:
                    segment = False
            else:
                segment = True
            sam_record = SAM(seq_name, leftmost_pos, seq_flag, ref, segment,
                            align_blocks, clipping_start, adjust_start,
                            clipping_end, adjust_end, percent_aligned, seq_length,
                            sam_flag.primary)

            # determine if in current & next window
            next_start = window_start + window_step
            next_end   = window_end   + window_step
            in_current = within_window(leftmost_pos, align_blocks, window_start,
                                       window_end, clipped_start)
            in_next    = within_window(leftmost_pos, align_blocks, next_start, 
                                       next_end, clipped_start)
            if in_current and in_next:
                # keeping in list to make grouping functions combatible
                # with scanning pipeline
                alignments[seq_name] = [sam_record] # keeping in list
                next_window_seqs.append(seq_name)
            elif in_current:
                alignments[seq_name] = [sam_record]
            elif in_next and not in_current:
 
                # now do the grouping here
                if len(alignments) >= min_grp and len(alignments) > 0:
                    outfh = process_window(alignments, window_start, window_end, ref, align_offset,
                                           clip_tolerance, del_tol, per_overlap, t_len, t_per,
                                           group_dels, min_grp, num_of_groups, using_genes, chr_genes,
                                           limit, flag_excess_groups, outfh)
 
                # save next windows in a temp dict b/c limit can be trigged, and remove
                # next window alignments
                if len(next_window_seqs) > 0:                
                    tmp        = {s:v for s,v in alignments.items() if s in next_window_seqs} 
                    alignments = copy.deepcopy(tmp)
                    clear_dict(tmp)
                    next_window_seqs.clear()
                else:
                    clear_dict(alignments)
                
                # start refilling the alignments again
                alignments[seq_name] = [sam_record]
                window_start += window_step
                window_end   += window_step

                next_start = window_start + window_step
                next_end = window_end   + window_step
                for seq in alignments:
                    sr = alignments[seq][0]
                    if sr.adjust_start == None:
                        clipped_start = 0
                    else:
                        clipped_start = sr.adjust_start
                    if within_window(sr.position, sr.align_blocks, next_start, next_end, clipped_start):
                        next_window_seqs.append(seq)

            elif not in_current and not in_next:
                
                if len(alignments) >= min_grp and len(alignments) > 0:
                    # process current alignments
                    outfh = process_window(alignments, window_start, window_end, ref, align_offset,
                                           clip_tolerance, del_tol, per_overlap, t_len, t_per,
                                           group_dels, min_grp, num_of_groups, using_genes, chr_genes,
                                           limit, flag_excess_groups, outfh)
                # clear current containers just in case
                if (len(next_window_seqs) > 0):
                    start_tmp = next_start
                    end_tmp   = next_end
                    alignments = {k:v for k, v in alignments.items() if k in next_window_seqs}
                    next_window_seqs.clear()
                else:
                    start_tmp = None
                    end_tmp   = None
                    clear_dict(alignments)
                # slide over to the next window
                while (in_current == False):
                    attempts = 0
                    window_start += window_step
                    window_end += window_step
                    in_current = within_window(leftmost_pos, align_blocks, window_start,
                                       window_end, clipped_start)
                    # should not happen, but just in case, start over and move forward
                    if window_start > ref_len:
                        if attempts == 1:
                            break
                        window_start = 0
                        window_end   = 0 + window_size
                        attempts    += 1
                # check if we are at a different window
                if len(alignments) >= min_grp and len(alignments) > 0 and start_tmp != window_start:
                    outfh = process_window(alignments, start_tmp, end_tmp, ref, align_offset,
                                           clip_tolerance, del_tol, per_overlap, t_len, t_per,
                                           group_dels, min_grp, num_of_groups, using_genes, chr_genes,
                                           limit, flag_excess_groups, outfh)
                elif (len(alignments) < min_grp) and (start_tmp != window_start):
                    clear_dict(alignments)
                alignments[seq_name] = [sam_record]
                next_start = window_start + window_step
                next_end   = window_end + window_step
                # still on the same record
                for seq in alignments:
                        sr = alignments[seq][0]
                        if sr.adjust_start == None:
                            clipped_start = 0
                        else:
                            clipped_start = sr.adjust_start
                        if within_window(sr.position, sr.align_blocks, next_start, next_end, clipped_start):
                            next_window_seqs.append(seq)
        fh.close()
        # check for last remaining seqs (a just in case situation)
        if len(alignments) >= min_grp and len(alignments) > 0:
            outfh = process_window(alignments, window_start, window_end, ref, align_offset,
                                           clip_tolerance, del_tol, per_overlap, t_len, t_per,
                                           group_dels, min_grp, num_of_groups, using_genes, chr_genes,
                                           limit, flag_excess_groups, outfh)

        # remove any remaining data
        clear_dict(alignments)
        next_window_seqs.clear()
        if tmp != None:
            clear_dict(tmp) # dict created

        # close output file
        if outfh != None:
            outfh.close()
        
        # do some clean up
        gc.collect()

        print(f"Finished scanning {ref}", flush=True)

def merge_genes(current_window: list, next_window: list):
    """take two strings where gene names are comma separated, & merge them without duplicates"""

    current_genes = current_window[2].split(',')
    next_genes = next_window[2].split(',')
    for gene in next_genes:
        if gene not in current_genes:
            current_genes.append(gene)

    return ','.join(current_genes)


def combine_columns(current_window: list, next_window: list, using_genes: bool, flag_excess_groups: bool):
    """combine the tile, number of groups, and gene (if present) columns"""

    new_window = [current_window[0], current_window[1]]


    if (flag_excess_groups):
        # add tile column
        new_window.append(current_window[2] + ',' + next_window[2])

        # add number of groups column
        new_window.append(current_window[3] + ',' + next_window[3])

        if (using_genes):
            current_genes = current_window[4].split(',')
            next_genes    = next_window[4].split(',')
            for gene in next_genes:
                if gene not in current_genes:
                    current_genes.append(gene)
            new_window.append(','.join(current_genes))
    else:
        # repeated code - TODO
        new_window.append(current_window[2] + ',' + next_window[2])

        if (using_genes):
            current_genes = current_window[3].split(',')
            next_genes    = next_window[3].split(',')
            for gene in next_genes:
                if gene not in current_genes:
                    current_genes.append(gene)
            new_window.append(','.join(current_genes))

    
    return new_window


def combine_scan_results(ref_seqs: list, align_map: str, window_step: int, using_genes: bool, flag_excess_groups: bool):
    """combine the Temp results into a single file"""

    printed = False

    # create output file
    align_map_name = os.path.basename(align_map)
    if align_map_name.endswith(".gz"):
        ext_cnt = 2
    else:
        ext_cnt = 1
    outname = '.'.join(align_map_name.split('.')[:-ext_cnt])
    outname = outname + "_Candidate_Regions.tsv"
    outfh   = open(outname, 'w')
    # write command & header
    # store arguments to tsv file
    command = "# klumpy " + \
         " ".join("\"" + arg + "\"" if " " in arg else arg for arg in sys.argv[1:]) + '\n'
    outfh.write(command)
    if (flag_excess_groups):
        header = "Region_Number\tReference_Seq\tStart\tEnd\tTiled\tNumber_of_Groups"
    else:
        header = "Region_Number\tReference_Seq\tStart\tEnd\tNumber_of_Groups"
    if using_genes:
        header = header + "\tGenes"
    outfh.write(header + '\n')

    region_cnt = 0 # used to track number of regions
    ref_count = 0 # used to track number of ref seqs

    for seq in ref_seqs:
        file_name = f"Temp_{seq}.txt"
        if os.path.isfile(file_name):
            current_window = None
            ref_count += 1
            if not printed:
                print("Merging results..")
                printed = True
            with open(file_name, 'r') as fh:
                for line in fh:
                    if current_window == None:
                        current_window = line.strip('\n').split('\t')[1:]
                    else:
                        current_start = int(current_window[0])
                        current_end = int(current_window[1])
                        next_window = line.strip('\n').split('\t')[1:]
                        next_start = int(next_window[0])
                        next_end = int(next_window[1])
                        if current_start + window_step == next_start:
                            current_window[1] = next_end
                            current_window = combine_columns(current_window, next_window, using_genes, flag_excess_groups)
                            # if using_genes:
                            #     current_window[2] = merge_genes(current_window, next_window)
                        elif current_end + window_step == next_end:
                            current_window[1] = next_end
                            current_window = combine_columns(current_window, next_window, using_genes, flag_excess_groups)
                            # if using_genes:
                            #     current_window[2] = merge_genes(current_window, next_window)
                        elif current_end >= next_start:
                            current_window[1] = next_end
                            current_window = combine_columns(current_window, next_window, using_genes, flag_excess_groups)
                            # if using_genes:
                            #     current_window[2] = merge_genes(current_window, next_window)
                        else:
                            # write to outfh
                            region_cnt += 1
                            outline = f"{region_cnt}\t{seq}\t" + '\t'.join([str(v) for v  in current_window]) + '\n'
                            outfh.write(outline)
                            outfh.flush()
                            current_window = next_window                
                            
                # get last window
                region_cnt += 1
                outline = f"{region_cnt}\t{seq}\t" + '\t'.join([str(v) for v in current_window]) + '\n'
                outfh.write(outline)
                outfh.flush()
                os.remove(file_name)
    
    outfh.close()
    print(f"Found {region_cnt} candidate regions across {ref_count} reference sequences", flush=True)

def Scan_Alignments(args):
    """Scan through a SAM/BAM file and find possible misassemblied regions"""

    # get arguments
    align_map, annotation, min_len, percent, deletion_len, align_offset, \
    clip_tolerance, t_len, t_per, per_overlap, del_tolerance, group_dels, \
    min_grp, window_size, window_step, num_of_groups, num_of_threads, limit, \
    flag_excess_groups    = check_args(args)

     # first, get the ref IDs to only analyze seqs >= window size
    ref_seqs, ref_seqs_list = parse_sam_header(align_map, window_size, num_of_threads)

    # check if we are using a gtf file
    if annotation != None:
        genome_genes = get_genes(annotation, ref_seqs)
        using_genes = True
    else:
        genome_genes = {}
        using_genes = False

    # put args into a list that will serve as an agruements list
    scan_args = [align_map, window_size, window_step, min_len, percent, limit,
                deletion_len, min_grp, num_of_groups, align_offset, clip_tolerance,
                del_tolerance, per_overlap, t_len, t_per, group_dels, using_genes, 
                flag_excess_groups]
    
    # if not multi-processing
    if num_of_threads == 1:
        ref_list = ref_seqs[0]
        ref_genes = {}
        if using_genes:
            tmp = []
            for ref_tuple in ref_list:
                if ref_tuple[0] in genome_genes:
                    ref_genes[ref_tuple[0]] = genome_genes[ref_tuple[0]]
                    tmp.append(ref_tuple)
            ref_list = tmp
        scan_args.insert(1, ref_list)
        scan_args.append(ref_genes)
        scan_align_map(*scan_args)
    else:
        # to contain all the processes
        processes = []

        for i in range(num_of_threads):
            ref_list = ref_seqs[i]
            ref_genes = {}
            if using_genes:
                tmp = []
                for ref_tuple in ref_list:
                    if ref_tuple[0] in genome_genes:
                        ref_genes[ref_tuple[0]] = genome_genes[ref_tuple[0]]
                        tmp.append(ref_tuple)
                ref_list = tmp
            scan_args_cp = copy.copy(scan_args)
            scan_args_cp.insert(1, ref_list)        
            scan_args_cp.append(ref_genes)
            proc = multiprocessing.Process(target = scan_align_map, args = scan_args_cp)
            proc.start()
            processes.append(proc)
        for proc in processes:
            proc.join()
        processes.clear()

    
    # now clean up
    combine_scan_results(ref_seqs_list, align_map, window_step, using_genes, flag_excess_groups)
    