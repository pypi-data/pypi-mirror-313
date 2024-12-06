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
import textwrap
from  .Classes import EXON, Seq_Record, GeneRecord

def determine_annotation_type(annotation: str):
    """determine whether the annotation file is a gtf or gff3 file"""
    
    # just a list of conditionals to check file extension
    if (annotation.endswith(".gtf.gz"))   or (annotation.endswith(".gtf")):
        pass
    elif (annotation.endswith(".gff.gz")) or (annotation.endswith(".gff")) or \
        (annotation.endswith(".gff3.gz")) or (annotation.endswith(".gff3")):
        pass
    else:
        msg = f"No .gtf, .gtf.gz, .gff, .gff.gz, .gff3, or .gff3.gz file extension detected in {annotation}" + \
                    "\nAssuming proper input"
        print(msg)

def check_args(args):
    """determine if params are acceptable"""

    # check gtf/gff file given & exists
    if args.annotation == None:
        msg = "--annotation [input_file] is required for get_exons"
        sys.exit(msg)
    if not os.path.isfile(args.annotation):
        msg = f"Could not find {args.annotation}"
        sys.exit(msg)
    # same for fasta
    if args.fasta == None:
        msg = "--fasta input.fa is required for get_exons"
        sys.exit(msg)
    if not os.path.isfile(args.fasta):
        msg = f"Could not find {args.fasta}"
        sys.exit(msg)
    # now for genes
    if args.genes == None:
        msg = "--genes gene_names is required for get_exons"
        sys.exit(msg)
    if len(args.genes) == 0:
        msg = "No genes were provided to --genes"
        sys.exit(msg)

    # one last check to get annotation type
    determine_annotation_type(args.annotation)
   
    return args.annotation, args.fasta, args.genes

# this function is a bit different since we are not looking for genes 
# in a specific seq (i.e.,) chrom, but instead, take a genes list
def get_exons_from_annotation(annotation: str, genes: list):
    """get the exons from the genes list"""

    if annotation.endswith(".gz"):
        fh = gzip.open(annotation, "rt")
    else:
        fh = open(annotation, 'r')

    ref_seqs       = {} # store reference & gene names
    found_gene     = False
    gene_container = {} # this will handle duplicate genes in annotation
    gene_record    = GeneRecord()
    rec_types      = ["gene", "mrna", "exon", "cds"] # determine which fields to look for

    for line in fh:
        if line[0] == '#':
            continue
        fields = line.strip('\n').split('\t')
        rec_type = fields[2].lower()
        if rec_type in rec_types:
            update = gene_record.update(fields[2])
            if update:
                found_gene, gene = gene_record.in_record(genes)
                if found_gene:
                    ref = gene_record.get_ref()
                    if ref not in ref_seqs:
                        ref_seqs[ref] = set()
                    ref_seqs[ref].add(gene)
                    if gene not in gene_container:
                        gene_container[gene] = [[]]
                    else:
                        gene_container[gene].append([])
                    # now add the exons
                    for ex in gene_record.exon_list:
                        gene_container[gene][-1].append(ex)
                gene_record.clear()
            gene_record.parse_attributes(fields[8])
            if rec_type in ["exon", "cds"]:
                gene_record.store_ref(fields[0]) # store for later
                left_pos  = int(fields[3])
                right_pos = int(fields[4])
                direction = fields[6]           # color won't be used
                gene_record.add_exon(left_pos, right_pos, direction, 0, line)

    # check last record
    if not gene_record.empty():
        found_gene, gene = gene_record.in_record(genes)
        if found_gene:
            ref = gene_record.get_ref()
            if ref not in ref_seqs:
                ref_seqs[ref] = set()
            ref_seqs[ref].add(gene)
            if gene not in gene_container:
                gene_container[gene] = [[]]
            else:
                gene_container[gene].append([])
            # now add the exons
            for ex in gene_record.exon_list:
                gene_container[gene][-1].append(ex)


    if len(gene_container) == 0:
        msg = f"No matching records found in {annotation}"
        print(msg)
        sys.exit(0)

    # struct of gene_container: {gene: [[exon set 1], [exon set 2], etc..]}
    return gene_container, ref_seqs

def write_to_fasta(seq: str, gene_container: dict, gene_set: set, ofh):
    """write a set of genes to the fasta output file handle"""

    for gene_name in gene_set: # for each gene in set
        exon_lists = gene_container[gene_name] # get list of lists
        duplicated = (len(exon_lists) != 1)
        for i, exon_list in enumerate(exon_lists, start = 1): # for each sub list in list
            for j, exon in enumerate(exon_list, start = 1): # for each exon obj in subj list
                start = exon.start_pos - 1 # gtf/gff are 1-based files
                end   = exon.end_pos # indexing is already excluding last pos
                if end > len(seq) - 1: # safety measurement
                    end = len(seq) - 1
                direction = exon.direction
                exon_seq  = seq[start:end]
                if direction == '-':
                    exon_seq = Seq_Record.reverse_complement(exon_seq)
                exon_seq = textwrap.fill(exon_seq, width = 80)
                if duplicated:
                    header_name = f">{gene_name}_{i}_E{j}\n"
                else:
                    header_name = f">{gene_name}_E{j}\n"
                try:
                    ofh.write(header_name + exon_seq + '\n')
                except:
                    ofh = open("exon_sequences.fa", 'w')
                    ofh.write(header_name + exon_seq + '\n')
    # return the file handle
    return ofh


def parse_fasta(fasta: str, gene_container: dict, ref_seqs: dict):
    """given a list of exons, write them out to a fasta file"""

    #
    # Read a gzipped file without any intervention.
    #
    if fasta.endswith(".gz"):
        fh = gzip.open(fasta, "rt")
    else:
        fh = open(fasta, 'r')

    seq   = ''
    id    = None
    found = False
    ofh   = None # only write if an exon found

    for line in fh:
        # skip empty or commented lines
        if len(line) == 0 or line.startswith('#'):
            continue
        line = line.strip('\n')
        if line.startswith(">"):
            # for the 1st record
            if seq == "":
                id = line[1:].split(" ")[0]
                if id in ref_seqs:
                    found = True
            elif found:
                # write exons to fasta
                ofh   = write_to_fasta(seq, gene_container, ref_seqs[id], ofh)
                found = False
                seq   = ''
            id = line[1:].split(" ")[0]
            if id in ref_seqs:
                found = True
            else:
                found = False
                seq   = '' # just for safe measures
        elif found:
            seq += line.upper()

    # for last seq
    if id in ref_seqs and len(seq) > 0:
        ofh = write_to_fasta(seq, gene_container, ref_seqs[id], ofh)

    # close
    if ofh != None:
        ofh.close()

def Get_Exons(args):
    """get the exon seqs from the requested genes"""

    # get arguments
    annotation, fasta, genes = check_args(args)

    # get the exon positions
    gene_container, ref_seqs = \
        get_exons_from_annotation(annotation, genes)

    # now to parse them out of the fasta file
    parse_fasta(fasta, gene_container, ref_seqs)
    