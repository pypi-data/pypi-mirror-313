# Copyright 2024:
#        Giovanni Madrigal <gm33@illinois.edu>
#        Julian Catchen <jcatchen@illinois.edu>
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

import argparse
import sys
import klumpy

Usage = f'''klumpy v{klumpy.__version__}

klumpy [analysis choice] --param1 input1 --param2 input2 etc...

Analysis Choices [must select one]:
    # primary subprograms
    find_klumps:                Find query klumps in a set of subject sequences
    scan_alignments:            Scan a SAM/BAM file for misassembled candidate regions

    # visualization subprograms
        alignment_plot:             Plot the alignments at a specified region using a SAM/BAM file
        klump_plot:                 Create a figure illustrating the klumps on the subject sequences
    
    # accessory subprograms
        combine_klumps:             Combine klump tsv files from multiple runs
        find_gaps:                  Create a tsv file containing the positions of gaps from a reference genome
        get_exons:                  Create a fasta file of exonic sequences from a list of genes
        kmerize:                    Find the coordinates of the query k-mers in the subject sequences
        klump_sizes:                Print out the expected klump sizes for each sequence

        
Options for `find_klumps`:
    --subject:                  Subject sequences in FAST[A|Q] format    
    --query:                    Query sequences in subject sequences, in FAST[A|Q] format
    --query_map:                The query_map file containing query matches generated after `find_klumps` or `kmerize`
    --output:                   Name of output file
    --range:                    Maximum distance two k-mers must be in order to be considered within the same klump (default = 1000)
    --min_kmers:                Minimum number of k-mers needed to form a klump (default = 1)
    --threads:                  Number of threads (default = 1)
    
    Advanced options:
        --ksize:                    Length of k-mer (must be an integer greater than 0) (default = 17)
        --query_count:              Minimum number of different queries a sequence is matched to (default = 1) 
        --klump_count:              Minimum number of klumps a sequence must have (default = 1)
        --limit:                    Number of subject sequences to load into memory at once (default 10000)        

        
Options for `scan_alignment`:
    --alignment_map:            A sorted and indexed SAM/BAM file [Required]
    --min_len:                  Minimum length a sequence must be to retain an alignment in the grouping analysis (default = 2000)
    --min_percent:              Minimum percent a sequence must be aligned for the alignment to be retained in the grouping analysis (default = 50)
    --threads:                  Number of threads (default = 1)
    --annotation:               Gene annotations in GTF/GFF3 format [Optional]

    Advanced options:
        --deletion_len:             Minimum length of deletion to draw and split alignment into blocks (default = 100)
        --assume_sep_del:           If set, remove the assumption that overlapping alignments with deletions can be automatically grouped if compatible
        --clip_tolerance:           Number of clipped base pairs to tolerate when comparing two alignments for compatibility (default = 400)
        --del_tolerance:            Length (in bp) covered by a deletion to be tolerated when comparing two alignments for compatibility (default = 50)
        --per_overlap:              Minimum percent two sequences need to overlap one another in order to confidently consider them compatible (default = 75)
        --t_len:                    Minimum length a sequence must be in order to trust its assignment when grouping (default = 2000)
        --t_per:                    Minimum percentage a sequence must be aligned in order to trust its assignment when grouping (default = 30)
        --align_offset:             Maximum number of base pairs apart for two sequences to be considered aligned at the same position (default = 100)
        --min_grp:                  Minimum number of sequences in a group in order to retain the group (default = 10)
        --window_size:              Length (in bp) for the sliding window to be (default = 50000)
        --window_step:              Length (in bp) for the sliding window to slide down to establish the next window (default = 25000) 
        --limit:                    Maximum number of alignments to process in a window (default 10000)
        --num_of_groups:            Number of groups at a window to flag the window (default = 3)
        --flag_excess_groups:       If set, will report regions with --num_of_groups Groups or more regardless if the region was tiled or not (default = False)


Options for `alignment_plot`:
    --alignment_map:            A sorted and indexed SAM/BAM file [Required]
    --reference:                Name of reference sequence
    --leftbound:                Leftmost Position in the reference genome (default = 0)
    --rightbound:               Rightmost Position in the reference genome (default = 50000)
    --region_num:               Region Number in a *_Candidate_Regions.tsv file generated by `scan_alignments` (default = 1)
    --candidates:               A *_Candidate_Regions.tsv file generated from `scan_alignments`
    --min_len:                  The Minimum length a sequence must be in order to retain it in the plot (default = 2000)
    --min_percent:              The Minimum percent of base pairs from a sequence that must be aligned for it to be retained in the plot (default = 50)
    --klumps_tsv:               Klump tsv output generated from `find_klumps`
    --gap_file:                 File containing locations of gaps in the reference (generated using `find_gaps`)
    --color:                    Color to use for drawing klumps (default = blue)
    --annotation:               Gene annotations in GTF/GFF3 format
    --list_colors:              If set, the program will list the available colors for klumps and exit
    --vertical_line_gaps:       If set, a vertical line above gaps will be drawn
    --vertical_line_klumps:     If set, a vertical line above the reference klumps will be drawn
    --vertical_line_exons:      If set, a vertical line above the exons will be drawn
    --format:                   Output format to draw image on. Choices are `pdf`, `png`, and `svg` (default = pdf)
    --group_seqs:               If set, the sequences in the plot will be grouped based on alignment patterns

    Advanced options:
        --min_klump_size:           Minimum number of k-mers a klump must contain to retain in the plot (default = 1)    
        --max_percent:              Maximum percent a sequence must be aligned for it to be retained in the plot (default = 100) 
        --height:                   Height (in pixels) of the pdf to be generated (default = 2000)
        --width:                    Width (in pixels) of the pdf to be generated (default = 2000)
        --klump_colors:             A tsv file containing the names of the klump sources and the color to use for drawing these klumps
        --color_by_gene:            If set and in combination with --klump_colors, will color all klumps belonging to the same gene
        --plotting_list:            List of sequences to plot (filters remain on)
        --deletion_len:             Minimum length of deletion to draw and split alignment into blocks (default = 100)
        --view_span:                Length (in bp) to view from the leftbound and the rightbound when parsing SAM/BAM file (default = 1000000)
        --number:                   If set, sequences on the plot will be numbered 
        --tick_count                If used, specify the number of ticks to use on the reference genome [Optional]
        --tick_span                 If used, specify how many base pairs the ticks on the reference genome should be apart [Optional]
        --write_table:              If set, general information on the sequences on the plot will be written out to a TSV file
        --paired:                   Set if working with paired-end data
        --no_primary:               If set, primary alignments will be filtered out
        --no_subsample:             If set, will not randomly subsample alignments when the number of alignments is greater than --limit
        --supplementary:            If set, supplementary alignments will be kept if they pass all other filters
        --secondary:                If set, secondary alignments will be kept if they pass all other filters
        --write_groups:             If set, the sequences for each group will be written out in fasta format (one file per group)
        --write_seqs:               If set, the sequences that were plotted will be written in fasta format
        --write_edge_seqs:          If set, sequences with clipped alignments at the edges/ends of their groups will have their names written to a list
        --assume_sep_del:           If set, remove the assumption that overlapping alignments with deletions can be automatically grouped if compatible
        --clip_tolerance:           Number of clipped base pairs to tolerate when comparing two alignments for compatibility (default = 150)
        --del_tolerance:            Length (in bp) covered by a deletion to be tolerated when comparing two alignments for compatibility (default = 50)
        --limit:                    Maximum number of alignments to process in a group analysis and draw (default 10000)
        --per_overlap:              Minimum percent two sequences need to overlap one another in order to confidently consider them compatible
        --t_len:                    Minimum length a sequence must be in order to trust its assignment when grouping (default = 2000)
        --t_per:                    Minimum percentage a sequence must be aligned in order to trust its assignment when grouping (default = 30)
        --align_offset:             Maximum number of base pairs apart for two sequences to be considered aligned at the same position (default = 100)
        --min_grp:                  Minimum number of sequences in a group in order to retain the group (default = 10)

        
Options for `klump_plot`:
    --klumps_tsv:               Klump tsv output generated from `find_klumps` [Required]
    --color:                    Color to use for drawing klumps (default = blue)
    --list_colors:              If set, the program will list the available colors for klumps and exit
    --fix_width:                If set, all the sequences in the figure will have the same `image` width
    --gap_file:                 File containing locations of gaps in the sequences (generated using `find_gaps`)
    --seq_name:                 Name of specific sequence to plot
    --format:                   Output format to draw image on. Choices are `pdf`, `png`, and `svg` (default = pdf)
    
    Advanced options:
        --klump_colors:             A tsv file containing the names of the query sources and the color to paint the query-specific klumps
        --color_by_gene:            If set and in combination with --klump_colors, will color all exons belonging to the same gene
        --leftbound:                Leftmost Position to plot --seq_name (default = 1) [requires --seq_name]
        --rightbound:               Rightmost Position to plot --seq_name (default = 50000) [requires --seq_name]
        --tick_count                If used, specify the number of ticks to use on the specified sequence [requires --seq_name]
        --tick_span                 If used, specify how many base pairs the ticks on the specified sequence should be apart [requires --seq_name]


Options for `combine_klumps`:
    --output:                   Name of output file [Optional]
    --klumps_tsv_list:          Names of files to combine (--klump_tsv_list file1.tsv file2.tsv file3.tsv etc...) [Required]

    
Options for `find_gaps`:
    --fasta:                    Reference genome in fasta format [Required]

    
Options for `get_exons`:
    --fasta:                    Reference genome in fasta format [Required]
    --annotation:               Gene annotations in GTF/GFF3 format [Required]
    --genes:                    Names of genes from which to extract exons from [Required] (e.g., --genes gene_name1 gene_name2 gene_name3)

    
Options for `kmerize`:
    --subject:                  Subject sequences to look for queried k-mers in FAST[A|Q] format [Required]    
    --query:                    Query sequences to generate query k-mers to search for in subject sequences, in FAST[A|Q] format [Required]
    --threads:                  Number of threads (default = 1)
    
    Advanced options:
        --ksize:                    Length of k-mer (must be an integer greater than 0) (default = 17)
        --output:                   Name of output file
        --limit:                    Number of subject sequences to load into memory at once (default 10000)
    

Options for `klump_sizes`:
    --fasta:                    Sequences to break down to k-mers, in FASTA format [Required]
    --ksize:                    Length of k-mer (must be an integer greater than 0) (default = 17)
'''

def get_arguments():
    """get the arguments"""

    parser = argparse.ArgumentParser(description="Klumpy: A bioinformatic tool for untangling collapsed genomes", prog="klumpy")
    parser.add_argument("analysis",               choices = ["alignment_plot", "combine_klumps", "find_gaps", "find_klumps", "get_exons", "kmerize", "klump_plot", "klump_sizes", "scan_alignments"])
    parser.add_argument("--align_offset",         default=250,  type=int)
    parser.add_argument("--alignment_map",        default=None, type=str)
    parser.add_argument("--annotation",           default=None, type=str)
    parser.add_argument("--assume_sep_del",       action="store_false")    
    parser.add_argument("--candidates",           default=None,   type=str)
    parser.add_argument("--clip_tolerance",       default=250,    type=int)
    parser.add_argument("--color",                default="blue", type=str)
    parser.add_argument("--color_by_gene",        action="store_true")
    parser.add_argument("--del_tolerance",        default=50,   type=float)
    parser.add_argument("--deletion_len",         default=100,  type=float)
    parser.add_argument("--fasta",                default=None, type=str)
    parser.add_argument("--flag_excess_groups",   action="store_true")
    parser.add_argument("--fix_width",            action="store_true")
    parser.add_argument("--format",               default="pdf", type=str, choices=["pdf", "png", "svg"])
    parser.add_argument("--gap_file",             default=None,  type=str)
    parser.add_argument("--genes",                default=None,  nargs='*')
    parser.add_argument("--group_seqs",           action="store_true")
    parser.add_argument("--height",               default=2000,  type=int)
    parser.add_argument("--klump_count",          default=1,     type=int)
    parser.add_argument("--klump_colors",         default=None,  type=str)
    parser.add_argument("--klumps_tsv",           default=None,  type=str)
    parser.add_argument("--klumps_tsv_list",      default=None,  nargs='*')
    parser.add_argument("--ksize",                default=17,    type=int)
    parser.add_argument("--leftbound",            default=1,     type=float)
    parser.add_argument("--limit",                default=10000,  type=int)
    parser.add_argument("--list_colors",          action="store_true")
    parser.add_argument("--max_percent",          default=100.0, type=float)
    parser.add_argument("--min_grp",              default=10,    type=int)
    parser.add_argument("--min_klump_size",       default=1,     type=int)
    parser.add_argument("--min_kmers",            default=1,     type=int)
    parser.add_argument("--min_len",              default=2000,  type=float)
    parser.add_argument("--min_percent",          default=0.50,  type=float)
    parser.add_argument("--no_primary",           action="store_true")
    parser.add_argument("--no_subsample",         action="store_true")
    parser.add_argument("--num_of_groups",        default=3,    type=int)
    parser.add_argument("--number",               action="store_true")
    parser.add_argument("--output",               default=None, type=str)
    parser.add_argument("--paired",               action="store_true") 
    parser.add_argument("--per_overlap",          default=0.50, type=float)
    parser.add_argument("--plotting_list",        default=None, type=str)
    parser.add_argument("--query",                default=None, type=str)
    parser.add_argument("--query_count",          default=1,    type=int)
    parser.add_argument("--query_map",            default=None, type=str)
    parser.add_argument("--range",                default=1000, type=int)
    parser.add_argument("--reference",            default=None, type=str)
    parser.add_argument("--region_num",           default=1,    type=int)
    parser.add_argument("--rightbound",           default=50000, type=float)
    parser.add_argument("--secondary",            action="store_true")
    parser.add_argument("--seq_name",             default=None, type=str)
    parser.add_argument("--subject",              default=None, type=str)
    parser.add_argument("--supplementary",        action="store_true")
    parser.add_argument("--t_len",                default=2000, type=float)
    parser.add_argument("--t_per",                default=0.30, type=float)
    parser.add_argument("--tick_count",           default=None, type=int)
    parser.add_argument("--tick_span",            default=None, type=float)
    parser.add_argument("--threads",              default=1,    type=int)
    parser.add_argument("--vertical_line_exons",  action="store_true")
    parser.add_argument("--vertical_line_gaps",   action="store_true")
    parser.add_argument("--vertical_line_klumps", action="store_true")
    parser.add_argument("--view_span",            default=1000000, type=float)
    parser.add_argument("--width",                default=2000,    type=int)
    parser.add_argument("--window_size",          default=50000,   type=float)
    parser.add_argument("--window_step",          default=25000,   type=float)
    parser.add_argument("--write_edge_seqs",      action="store_true")
    parser.add_argument("--write_groups",         action="store_true")
    parser.add_argument("--write_seqs",           action="store_true")
    parser.add_argument("--write_table",          action="store_true")

    # change usage
    parser.format_usage = lambda : Usage
    parser.format_help  = parser.format_usage

    # parse the arguements and return the entire collection of inputs
    args = parser.parse_args()

    return args
  
def main():

    args = get_arguments()

    # determine which pipeline will be run

    if args.analysis == "alignment_plot":
        klumpy.Alignment_Plot(args)
    elif args.analysis == "combine_klumps":
        klumpy.Combine_Klumps(args)
    elif args.analysis == "find_gaps":
        klumpy.Find_Gaps(args)
    elif args.analysis == "find_klumps":
        klumpy.Find_Klumps(args)
    elif args.analysis == "get_exons":
        klumpy.Get_Exons(args)
    elif args.analysis == "kmerize":
        klumpy.Kmerize(args)
    elif args.analysis == "klump_plot":
        klumpy.Klump_Plot(args)
    elif args.analysis == "klump_sizes":
        klumpy.Klump_Sizes(args)
    elif args.analysis == "scan_alignments":
        klumpy.Scan_Alignments(args)
    else:
        msg = "Something went wrong. None of the analysis choices seemed to be selected."
        sys.exit(msg)

if __name__ == "__main__":
    main()