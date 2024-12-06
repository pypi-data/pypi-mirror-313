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
import os
import cairo
import sys
import gzip
from .alignment_plot import get_color, parse_klump_color_list, check_tick_params, find_coordinates, overlapping_labels
from .Classes import Klump, GAP

def check_args(args):
    """do some initial checks to make sure there is nothing immediately off"""

    # this must be checked first as we can exit without doing anything else
    assert type(args.list_colors) is bool, "--list_colors does not take any positional values"
    args.color = get_color(args.list_colors, False, 0, args.color)

    if args.klumps_tsv == None:
        msg = "--klumps_tsv is required for klump_plot"
        sys.exit(msg)
    assert os.path.isfile(args.klumps_tsv), f"Could not find {args.klumps_tsv}"
    assert type(args.fix_width) is bool, "--fix_width does not take any positional arguments"

    if args.gap_file != None:
        assert os.path.isfile(args.gap_file), f"Could not find {args.gap_file}"
        fh = gzip.open(args.gap_file, "rt") if args.gap_file.endswith(".gz") else open(args.gap_file, 'r')
        for line in fh:
            if len(line.strip().split("\t")) != 3:
                sys.exit(f"Check if {args.gap_file} is a three column file")
            else:
                break
    
    if args.klump_colors != None:
        assert os.path.isfile(args.klump_colors), f"Could not find {args.klump_colors}"
        assert type(args.color_by_gene) == bool,   "--color_by_gene does not take any arguments"
    
    # if a reference, leftbound, and rightbound are applied
    update_bounds = False
    if args.seq_name != None:
        # check if leftbound & rightbound are provided in args
        if (("--leftbound" in sys.argv) == False) or (("--rightbound" in sys.argv) == False):
            # set to default for now, but will update later
            args.leftbound  = 1
            args.rightbound = 50000
            update_bounds = True
        
        assert args.rightbound > args.leftbound, "--rightbound must be greater than --leftbound"
        assert args.leftbound >= 0,              "--leftbound must be greater than or equal to 0"
        
        # only check now if we can
        if update_bounds == False:
            args.tick_count, args.tick_span = \
                check_tick_params(args.tick_count, args.tick_span, args.leftbound, args.rightbound)

    # return args
    return args.klumps_tsv, args.color, args.fix_width, args.gap_file, args.klump_colors, \
            args.color_by_gene, args.seq_name, int(args.leftbound), int(args.rightbound), args.format, \
            args.tick_count, args.tick_span, update_bounds

######### parsing functions ############

def parse_klumps_out(klump_file: str, SEQ_NAME: str, leftbound: int, rightbound: int, update_bounds: bool,
                     tick_count: int, tick_span: int):
    """get klump info per sequence or if specified, a particular locus"""

    seq_klumps  = {}
    seq_lengths = {}
    src_dict    = {}

    fh = gzip.open(klump_file, "rt") if klump_file.endswith(".gz") else open(klump_file, 'r')

    for line in fh:
        if line.startswith("Sequence\t"):
            continue
        if (line[0] == '#'):
            if (line.startswith("#Source ") == False): continue
            line    = line.replace("#Source ", '')
            sources = line.strip('\n').split(',')
            for source in sources:
                source = source.strip(' ').split(' ')
                src, idx = source[0], source[1]
                src_dict[idx] = src
            continue
        fields = line.strip().split("\t")
        fields = line.strip().split("\t")
        seq = r'{}'.format(fields[0])
        # check if plotting a specific seq and region
        if SEQ_NAME != None:
            # skip
            if seq != SEQ_NAME:
                continue
        # keep track of seq length
        seq_lengths[seq] = int(fields[1])
        # check if rightbound is reasonable
        if SEQ_NAME != None:
            if update_bounds:
                rightbound = seq_lengths[seq]
                # now verify the tick count & span
                tick_count, tick_span = check_tick_params(tick_count, tick_span, leftbound, rightbound)
                update_bounds = False # now checked
            # otherwise, check provided bounds
            elif rightbound > seq_lengths[seq]:
                msg = f"Rightbound ({rightbound}) found to be greater than sequence length ({seq_lengths[seq]})\n" + \
                    "Setting rightbound to sequence length"
                print(msg)
                rightbound = seq_lengths[seq]
        qsrc = src_dict.get(fields[5], fields[5])
        # klump name, start pos, end pos,
        # query source, klump size, direction
        klmp = Klump(fields[2], fields[3], fields[4],
                     qsrc, fields[6], fields[7])
        # check if keeping the klump
        if SEQ_NAME != None:
            # out of bounds
            if klmp.end_pos < leftbound:
                continue
            if klmp.start_pos > rightbound:
                continue
            # adjust to section
            if klmp.start_pos < leftbound:
                klmp.start_pos = leftbound
            if klmp.end_pos > rightbound:
                klmp.end_pos   = rightbound
            klmp.start_pos = int(klmp.start_pos - leftbound)
            klmp.end_pos   = int(klmp.end_pos - leftbound)
        if seq not in seq_klumps:
            seq_klumps[seq] = [klmp]
        else:
            seq_klumps[seq].append(klmp)
    
    fh.close()

    # verify that there is something to plot
    if SEQ_NAME != None:
        if len(seq_lengths) == 0:
            msg = f"Could not find {SEQ_NAME}"
            sys.exit(msg)
        if len(seq_klumps) == 0:
            msg = f"No klump records found between {leftbound} and {rightbound} bp"
            sys.exit(msg)
    elif len(seq_klumps) == 0: # none found throughout entire file
        msg = f"No klump records were able to be parsed out {os.path.basename(klump_file)}"
        sys.exit(msg)
            
    return seq_klumps, seq_lengths, rightbound, tick_count, tick_span


def parse_gap_file(seq_klumps: dict, gap_file: str, SEQ_NAME: str, leftbound: int, rightbound: int):
    """get gaps to plot onto sequences - function varies a bit from alignment_plot sister function"""

    #column 0: seq_id
    #column 1: start position
    #column 2: end position

    gaps = {}

    fh = gzip.open(gap_file, "rt") if gap_file.endswith(".gz") else open(gap_file, 'r')

    for line in fh:
        fields = line.strip().split('\t')
        if fields[0] in seq_klumps:
            if SEQ_NAME == None:
                seq       = fields[0]
                start_pos = int(fields[1])
                end_pos   = int(fields[2])
                if seq not in gaps:
                    gaps[seq] = []
                gaps[seq].append(GAP(start_pos, end_pos))
            else:   
                #0-based positions
                if leftbound <= int(fields[1]) <= rightbound or \
                    leftbound <= int(fields[2]) <= rightbound:
                    start_pos = int(fields[1])
                    end_pos   = int(fields[2])

                    #just in case gap crosses boundaries                    
                    if start_pos < leftbound:
                        start_pos = leftbound
                    if end_pos > rightbound:
                        end_pos   = rightbound
                    if SEQ_NAME not in gaps:
                        gaps[SEQ_NAME] = []
                    gaps[SEQ_NAME].append(GAP(start_pos, end_pos))

    fh.close()

    return gaps

########## helper functions #############

def adjust_x(image_width: float, seq_name: str, seq_lengths: dict, fix_width: bool):
    """"estimate where to plot seqs by first align length"""


    # if img width is fixed, return
    if fix_width:
        return 150

    # adjust
    max_seq_length = max(list(seq_lengths.values()))
    seq_length     = seq_lengths[seq_name]

    # longest seq starts in normal position
    if max_seq_length == seq_length:
        return 150
    else:
        # attempt to align the middles of each seq
        # idea:
        #       |-----|
        #    |-----------|

        longer_half   = max_seq_length/2
        shorter_half  = seq_length/2
        allocated_pos = image_width / max_seq_length

        # find relative position of the longer seq
        adjusted_longer_half = 150 + (allocated_pos * longer_half)
        # make adjustment for seq
        adjusted_x = adjusted_longer_half - (shorter_half * allocated_pos)
        return adjusted_x


def create_y_positions(seq_lengths: dict):
    """adjust pdf height for # of seqs"""

    # how many pixel are allocated per sequence
    seq_space     = 275
    offset        = 200
    figure_height = (len(seq_lengths)*seq_space) + offset
    y_positions   = {}

    # reverse order to have longest seq at top
    sorted_seq_lengths = dict(sorted(seq_lengths.items(), key=lambda seq: seq[1], reverse=True))

    for i, seq in enumerate(sorted_seq_lengths):
        y_pos            = figure_height - offset - (i * seq_space)
        y_positions[seq] = y_pos

    return figure_height, y_positions

# TODO prevent overlapping between klump labels
# def adjust_klump_labels(klumps_labels: dict, direction: str):
#     """establish label positions to avoid overlapping labels"""

#     adjusted_positions = {}
#     prev_label_dim = None

#     # sort by x positions just in case
#     sorted_labels = [k for k,v in sorted(klumps_labels.items(), key = lambda item: item[1][0])]

#     # helper function to unpack tuple values
#     def unpack_tuple(label_tuple: tuple, direction: str):
#         x_start = label_tuple[0]
#         y_pos = label_tuple[1]
#         label_width = label_tuple[2]
#         label_height = label_tuple[3]
#         return find_coordinates(x_start, y_pos, label_width, label_height, direction)


#     for i, klump_name in enumerate(sorted_labels):
#         # tuple = (x pos, y pos, width, height, label, color)
#         label_tuple = klumps_labels[klump_name]
#         label_dim = unpack_tuple(label_tuple, direction)
#         if prev_label_dim == None:
#             prev_label_dim = label_dim
#             continue
#         if overlapping_labels(prev_label_dim, label_dim):
#             pass
            

########## plotting functions #############


def plot_seq(cairo_context, seq_lengths: dict, seq_id: str, allocated_positions: float,
              seq_height: float, x_pos: float, SEQ_NAME: str, leftbound: int, rightbound: int):
    """ plot sequence to scale to the longest sequence"""
    
    sequence_id   = seq_id
    allocated_pos = allocated_positions[seq_id]

    # starting positions
    x1 = x_pos  # offset from left by x position
    y1 = seq_height  # y / vertical offset

    # determine new x
    x2 = x_pos + (allocated_pos * seq_lengths[seq_id])  # scale to longest seq

    # draw a rectange and fill with light grey
    offset = 14
    cairo_context.move_to(x1, y1 + offset) # top right
    cairo_context.line_to(x2, y1 + offset) # top left
    cairo_context.line_to(x2, y1 - offset) # bottom left
    cairo_context.line_to(x1, y1 - offset) # bottom right
    cairo_context.close_path() # seal path
    cairo_context.set_source_rgba(0.7, 0.7, 0.7, 1) # light grey
    cairo_context.fill_preserve()
    cairo_context.set_source_rgb(0, 0, 0)  # black
    cairo_context.set_line_width(3)
    cairo_context.stroke()

    # add sequence name based if align_pos to top
    x = 100
    y = seq_height - 100

    cairo_context.set_source_rgb(0, 0, 0)
    cairo_context.set_font_size(42) # prev 75
    cairo_context.select_font_face(
        "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
    )
    cairo_context.move_to(x, y)
    if SEQ_NAME != None:
        left = "{:,}".format(leftbound)
        right = "{:,}".format(rightbound)
        sequence_id = f"{sequence_id}: {left}-{right}"
    cairo_context.show_text(sequence_id)
    cairo_context.stroke()


def create_ticks(seq_length: int):
    """Find the appropriate marker lengths for tick marks"""

    #10 ticks per sequence (at most)
    marker_sets = {
        1e3: 100,
        5e3: 500,
        7.5e3: 750,
        1e4: 1000,
        2.5e4: 2500,
        5e4: 5000,
        9e4: 9000,
        1e5: 10000,
        5e5: 50000,
        9e5: 90000,
        1e6: 100000,
        5e6: 500000,
        9e6: 1000000,
        1e7: 2000000,
        3e7: 3000000,
        5e7: 5000000,
        7e7: 7000000,
        9e7: 9000000,
        1e8: 10000000,
        5e8: 50000000,
        9e8: 90000000,
        1e9: 100000000,
        1e10: 1000000000,
        1e11: 10000000000,

    }

    multiplier = None

    for marker_length in marker_sets.keys():
        if seq_length <= marker_length:
            multiplier = marker_sets[marker_length]
            break

    # multiplier will be used to show increments in bp length
    if multiplier != None:
        tick_ct = math.floor(seq_length/multiplier)
    else:
        sys.exit(f"Software was not prepared for sequence/segment of length {seq_length}")

    return tick_ct, multiplier


def draw_ticks(cairo_context, y_coordinate: float, seq_len: int, image_width: float, 
               orientation: str, x_pos: float, fix_width: bool, max_seq_length: int,
               SEQ_NAME: str, leftbound: int, rightbound: int, tick_count: int,
               tick_span: int):
    """add tick marks to the reference sequence"""

    # need to offset from seq drawing
    if orientation == "top":
        mark_ypos1 = y_coordinate - 13 # 23
        mark_ypos2 = y_coordinate - 32 # 75
        label_ypos = y_coordinate - 35 # 80
    elif orientation == "bottom":
        mark_ypos1 = y_coordinate + 13
        mark_ypos2 = y_coordinate + 23
        label_ypos = y_coordinate + 46 # this is the bottom of the text label

    if SEQ_NAME != None:
        adjust  = True
        org_len = seq_len
        seq_len = rightbound - leftbound
    else:
        adjust = False
    
    # manual adjustment of ticks only when plotting a specific site
    if SEQ_NAME != None and tick_count != None:
        tick_ct, multiplier = int(tick_count), int(tick_span) # convert as a safe mechanism
    else:
        tick_ct, multiplier = create_ticks(seq_len)

    # adjust for just ticks
    if fix_width:
        allocated_pos = ((image_width / max_seq_length) * \
            max_seq_length) / (seq_len/multiplier)
    else:
        allocated_pos = ((image_width / max_seq_length) * \
            seq_len) / (seq_len/multiplier)
        
    # TODO repeated code that can be reduced
        
    # we get the marker label once since we are plotting the entire seq
    if not adjust:
        marker = "BP"
        if 1e3 <= seq_len <= 1e6:
            marker = "K"
        elif 1e6 <= seq_len <= 1e9:
            marker = "M"
        elif seq_len > 1e9:
            marker = "G"
 
    for i in range(1, tick_ct + 1):
        marker_num = i * multiplier  # interval scheme
        if adjust:
            marker_num = marker_num + leftbound
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
            marker_num = round(marker_num, 2)
        else:
            if marker_num < 1e3:
                if marker == 'K':
                    marker_num = marker_num/1000
                else:
                    marker_num = marker_num/100
            elif marker_num < 1e6:
                if marker == 'M' and marker_num > 10:
                    marker_num = marker_num/1e6
                else:
                    marker_num = marker_num/1e3
            elif 1e6 <= marker_num <= 1e7:
                marker_num = marker_num/1e6
            elif marker_num <= 1e8:
                marker_num = (marker_num/1e7) * 10
            else:
                marker_num = (marker_num/1e8) * 100
            marker_num - round(marker_num, 1)
        marker_label = f"{str(marker_num)}{marker}"
        marker_pos = x_pos + (allocated_pos * i)  # x pos offset for image

        # plot each tick and its label
        cairo_context.move_to(marker_pos, mark_ypos1)
        cairo_context.line_to(marker_pos, mark_ypos2)
        cairo_context.set_source_rgba(0, 0, 0, 1)  # black
        cairo_context.set_line_width(2.5)
        cairo_context.stroke()
        # marker labels
        cairo_context.set_source_rgba(0, 0, 0, 1)
        cairo_context.set_font_size(30) # prev 55
        cairo_context.move_to(marker_pos - 35, label_ypos)
        cairo_context.show_text(marker_label)
        cairo_context.stroke()


def plot_label(cairo_context, y: float, theta: float, label: str, midpoint: float):
    """plot klump labels"""

    new_x = midpoint
    new_y = y - 63
    cairo_context.save()
    # create labels
    cairo_context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL,
                                   cairo.FONT_WEIGHT_NORMAL)
    cairo_context.set_source_rgb(0, 0, 0)  # black
    cairo_context.set_font_size(14) # prev 25
    cairo_context.move_to(new_x, new_y)
    cairo_context.rotate(theta)
    cairo_context.show_text(label)
    cairo_context.stroke()
    cairo_context.restore()


def plot_klumps(cairo_context, y_coordinate: float, seq_name: str, allocated_positions: float, 
                seq_klumps: dict, x_pos: float, color, klump_colors: dict, color_by_gene: bool):
    """plot the klumps and then plot the labels"""

    # TODO adjust labels in the future? for now, alternate positions
    directions = ['F', 'R']
    i = 0

    # fill in instead of making "klump"
    allocated_pos = allocated_positions[seq_name]

    # make a copy of the color obj just in case to avoid over writing
    if klump_colors != None:
        org_color = color

    # dicts to store top vs bottom labels separate
    # top_labels = {}
    # bottom_labels = {}

    # sort and then plot, but need to calculate the midpoints
    midpoints = {}

    for seq, klumps in seq_klumps.items():
        if seq == seq_name:
            for klump in klumps:
                if klump_colors != None:
                    if color_by_gene:
                        ksource = '_'.join(klump.query_source.split('_')[:-1])
                    else:
                        ksource = klump.query_source
                    color = klump_colors.get(ksource, org_color) # default to current color
                fill_in_matches(cairo_context, y_coordinate, x_pos,
                                allocated_pos, klump.start_pos, klump.end_pos, color)

                # get direction to see if klump is on forward or reverse (currently alternating)
                # create label & get dimensions
                klump_size = klump.klump_size
                query      = klump.query_source
                label      = f"{klump_size}-{query}"
                # label_dim = cairo_context.text_extents(label)
                # get the mid point of the text if i were not rotated
                start_pos                   = x_pos + (klump.start_pos * allocated_pos)
                end_pos                     = x_pos + (klump.end_pos * allocated_pos)
                klump_midpoint              = (end_pos + start_pos) / 2
                midpoints[klump.klump_name] = (label, klump_midpoint)

    sorted_labels = [k for k,v in sorted(midpoints.items(), key = lambda item: item[1][1])]

    for i, k in enumerate(sorted_labels):
        direction = directions[i % 2]
        if direction == 'F':
            yLabel = y_coordinate + 42 # prev 30
            angle  = -45
        elif direction == 'R':
            yLabel = y_coordinate + 90 # 105
            angle  = 45
        # convert to radians
        theta          = math.radians(angle)
        k_tuple        = midpoints[k]
        klump_midpoint = k_tuple[1]
        label          = k_tuple[0]
        # create labels
        plot_label(cairo_context, yLabel, theta, label, klump_midpoint)


def fill_in_matches(cairo_context, y: float, x_pos: float, allocated_pos: float, 
                    klump_start: int, klump_end: int, color):
    """fill in seq with klump positions"""

    # using a for loop instead of drawing a square b/c although
    # less accurate, it is easier to see the annotations on a chr scale
    y1 = y - 12.5
    y2 = y + 12.5
    for k in range(klump_start, klump_end + 1):
        x = x_pos + (k * allocated_pos)
        cairo_context.move_to(x, y1)
        cairo_context.line_to(x, y2)
        cairo_context.set_source_rgb(color.red, color.green, color.blue)
        cairo_context.set_line_width(1)
        cairo_context.stroke()


def draw_gaps(cairo_context, seq, y, x_pos, allocated_pos, gaps):
    """draw the gaps onto the figure"""

    # return if not present
    if seq not in gaps:
        return
    
    # get the list of gaps
    gaps_list = gaps[seq]

    y1 = y - 13 # starting on top of the seq
    y2 = y - 100 # move upwards by 160 pixels

    # adjust
    for gap in gaps_list:
        start_pos = x_pos + (gap.start_pos * allocated_pos)
        end_pos   = x_pos + (gap.end_pos   * allocated_pos)
        # mid point between start & end
        dash_start = start_pos + ((end_pos - start_pos)/2)
        cairo_context.set_line_width(end_pos - start_pos)
        cairo_context.set_dash([15.0, 5.0])
        cairo_context.move_to(dash_start, y1)
        cairo_context.line_to(dash_start, y2)
        cairo_context.set_source_rgb(0, 0, 0) # solid black to stand out
        cairo_context.stroke()

def plot_seq_klumps(seq_lengths: dict, seq_klumps: dict, output_name: str, 
                    color, fix_width: bool, gaps: list, klump_colors: dict, 
                    color_by_gene: bool, SEQ_NAME: str, leftbound: int, rightbound: int, 
                    outformat: str, tick_count: int, tick_span: int):
    """function to create the klump plot after parsing inputs"""

    figure_height, y_positions = create_y_positions(seq_lengths)
    figure_width = 2500 # perv 4500

    if outformat == "pdf":
        ims = cairo.PDFSurface(output_name, figure_width, figure_height)
    elif outformat == "png":
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, figure_width, figure_height)
    elif outformat == "svg":
        ims = cairo.SVGSurface(output_name, figure_width, figure_height)

    cairo_context = cairo.Context(ims)
    image_width   = figure_width - 400  # offset by starting positions on both sides

    # change length if needed
    if SEQ_NAME != None:
        org_len               = seq_lengths[SEQ_NAME]
        seq_lengths[SEQ_NAME] = rightbound - leftbound

    # get x positions
    x_positions = {}
    for seq in seq_lengths.keys():
        x_positions[seq] = adjust_x(image_width, seq, seq_lengths, fix_width)

    # create allocated posititions for sites
    max_seq_length = max(list(seq_lengths.values()))
    allocated_pos  = {}

    for seq_id, seq_len in seq_lengths.items():
        # if img is fixed
        if fix_width:
            allocated_pos[seq_id] = \
                ((image_width/max_seq_length) * max_seq_length) / seq_len
        else:
            # adjust
            allocated_pos[seq_id] = (
                (image_width/max_seq_length) * seq_len) / seq_len

    # plot seqs
    for seq, seq_len in seq_lengths.items():
        plot_seq(cairo_context, seq_lengths, seq, allocated_pos, y_positions[seq],
                      x_positions[seq], SEQ_NAME, leftbound, rightbound)
        if SEQ_NAME == None:
            orientation = "top"
        else:
            orientation = "bottom"
            seq_len     = org_len
        draw_ticks(cairo_context, y_positions[seq], seq_len, image_width,
                    orientation, x_positions[seq], fix_width, max_seq_length,
                    SEQ_NAME, leftbound, rightbound, tick_count, tick_span)
        plot_klumps(cairo_context, y_positions[seq],
                    seq, allocated_pos, seq_klumps, x_positions[seq],
                    color, klump_colors, color_by_gene)
        # if gaps provided
        if gaps != None:
            # get original dash (no dash)
            org_dash = cairo_context.get_dash()
            draw_gaps(cairo_context, seq, y_positions[seq], 
                      x_positions[seq], allocated_pos[seq], gaps)
            # and set back to default
            cairo_context.set_dash(org_dash[0])

    # finish plot
    if outformat == "pdf":
        cairo_context.show_page()
    elif outformat == "png":
        ims.write_to_png(output_name)
    elif outformat == "svg":
        ims.finish()
        ims.flush()

def Klump_Plot(args):
    """Get the arguments, parse the necessary files, and visualize the klumps!"""

    # get arguments
    klump_file, color, fix_width, gap_file, klump_colors, \
    color_by_gene, SEQ_NAME, leftbound, rightbound, outformat, \
    tick_count, tick_span, update_bounds = check_args(args)

    # klump info
    seq_klumps, seq_lengths, rightbound, tick_count, tick_span =\
          parse_klumps_out(klump_file, SEQ_NAME, leftbound, rightbound, 
                           update_bounds, tick_count, tick_span)

    # get gaps if present
    if gap_file != None:
        gaps = parse_gap_file(seq_klumps, gap_file, SEQ_NAME, leftbound, rightbound)
        if len(gaps) == 0:
            print(f"Could not find any gaps for sequences in {os.path.basename(klump_file)}")
    else:
        gaps = None

    # check if using klump specific colors
    if klump_colors != None:
        klump_colors = parse_klump_color_list(klump_colors)

    # run the entire script
    if SEQ_NAME == None:
        extension   = str(klump_file).split(".")[-1]
        output_name = os.path.basename(klump_file).replace(extension, outformat)
    else:
        output_name = f"{SEQ_NAME}_{leftbound}-{rightbound}_klump_plot.{outformat}"
        
    plot_seq_klumps(seq_lengths, seq_klumps, output_name, color, fix_width,
                    gaps, klump_colors, color_by_gene, SEQ_NAME, leftbound, rightbound,
                    outformat, tick_count, tick_span)

