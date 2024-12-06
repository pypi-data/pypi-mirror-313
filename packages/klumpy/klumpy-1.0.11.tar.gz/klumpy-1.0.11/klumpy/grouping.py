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



# this code will not be run as a pipeline
# but instead, will be called by scan_alignments &
# alignment_plot to perform the grouping algorithm

import os, random
from .Classes    import STRUCTURE, Del_Window, C_Score, Feature_Color, algn_blocks
from typing      import List
from collections import defaultdict
from .           import alignment_plot


def clear_dict(map_dict: dict):
    """currently a temporary fix to remove possible circular references"""

    for v in map_dict.values():
        v.clear()
    map_dict.clear()
    map_dict = None # deallocate pointer

def check_blocks(s1_struct: STRUCTURE, s2_struct: STRUCTURE, del_tol: int):
    """determine if the two sequences are incompatible due to covered regions overlapping deletions"""

    for cov_blck in s1_struct.covered_regions:
        cov_blk_start = cov_blck[0]
        cov_blk_end = cov_blck[1]
        for del_blck in s2_struct.deletion_regions:
            del_start = del_blck[0]
            del_end   = del_blck[1]
            # buffers of tolerance
            del_start_b = del_start + del_tol
            del_end_b   = del_end - del_tol
            if del_start_b < cov_blk_start < del_end_b:
                return True
            elif del_start_b < cov_blk_end < del_end_b:
                return True
            # now do check for deletions being within the covered blocks
            del_len = del_end_b - del_start_b
            if cov_blk_start < del_start_b < del_end_b < cov_blk_end:
                if del_len > del_tol:
                    return True

    return False

def calc_overlap(s1_struct: STRUCTURE, s2_struct: STRUCTURE):
    """calculate the number of bases two sequences overlap"""

    tot_cov = 0

    if s1_struct.align_pos <= s2_struct.align_pos:
        s1_blks = s1_struct.covered_regions
        s2_blks = s2_struct.covered_regions
    else:
        s1_blks = s2_struct.covered_regions
        s2_blks = s1_struct.covered_regions

    for blk1 in s1_blks:
        blk1_start = blk1[0]
        blk1_end   = blk1[1]
        for blk2 in s2_blks:
            blk2_start = blk2[0]
            blk2_end = blk2[1]
            if blk1_end < blk2_start:
                continue
            if blk1_start < blk2_start:
                start = blk2_start
            else:
                start = blk1_start
            if blk1_end > blk2_end:
                end = blk2_end
            else:
                end = blk1_end
            tot_cov += (end - start)

    return tot_cov

def Within_Range(pos1: int, pos2: int, offset: int):
    """check if two positions are close enough to be considered the 'same' """

    pos1_left  = pos1 - offset
    pos1_right = pos1 + offset
    pos2_left  = pos2 - offset
    pos2_right = pos2 + offset

    if pos1_left <= pos2 <= pos1_right:
        return True
    elif pos2_left <= pos1 <= pos2_right:
        return True
    
    return False

def check_clip_status(s1_struct: STRUCTURE, s2_struct: STRUCTURE, clip_tolerance : int):
    """check if the clipping tolerance is acceptable"""

    # straight forward
    if (s1_struct.clipfree) and (s2_struct.clipfree):
        return True
    
    # same overall struct
    if s1_struct.num_blocks == s2_struct.num_blocks:
        # if seq 2 is contained within seq 1
        if s1_struct.align_pos <= s2_struct.align_pos <= s2_struct.align_end <= s1_struct.align_end: 
            if s2_struct.clipfree:
                return True
            # only the beginning of the alignment is clipped
            elif (s2_struct.clipping_start) and (s2_struct.clipping_end == False):
                clip_pos = s2_struct.clip_start
                # if clip is entirely in seq 1
                if clip_pos > s1_struct.align_pos:
                    clip_len = s2_struct.clip_start_len
                else:
                    clip_len = s2_struct.align_pos - s1_struct.align_pos    
                if clip_len <= clip_tolerance:
                    return True
            # only the end of the alignment is clipped
            elif (s2_struct.clipping_start == False) and (s2_struct.clipping_end):
                clip_pos = s2_struct.clip_end
                if clip_pos > s1_struct.align_end:
                    clip_len = s1_struct.align_end - s2_struct.align_end
                else:
                    clip_len = s2_struct.clip_end_len
                if clip_len <= clip_tolerance:
                    return True
            # both are clipped
            else:
                clip_pos_s = s2_struct.clip_start
                clip_pos_e = s2_struct.clip_end
                if clip_pos_s > s1_struct.align_pos:
                    clip_len_s = s2_struct.clip_start_len
                else:
                    clip_len_s = s2_struct.align_pos - s1_struct.align_pos
                if clip_pos_e > s1_struct.align_end:
                    clip_len_e = s1_struct.align_end - s2_struct.align_end
                else:
                    clip_len_e = s2_struct.clip_end_len
                if clip_len_s <= clip_tolerance and clip_len_e <= clip_tolerance:
                    return True
        # seq 1 is, instead, within seq 2
        elif s2_struct.align_pos <= s1_struct.align_pos <= s1_struct.align_end <= s2_struct.align_end:
            if s1_struct.clipfree:
                return True
            # only the beginning of the alignment is clipped
            elif (s1_struct.clipping_start) and (s1_struct.clipping_end == False):
                clip_pos = s1_struct.clip_start
                # if clip is entirely in seq 1
                if clip_pos > s2_struct.align_pos:
                    clip_len = s1_struct.clip_start_len
                else:
                    clip_len = s1_struct.align_pos - s2_struct.align_pos    
                if clip_len <= clip_tolerance:
                    return True
            # only the end of the alignment is clipped
            elif (s1_struct.clipping_start == False) and (s1_struct.clipping_end):
                clip_pos = s1_struct.clip_end
                if clip_pos > s2_struct.align_end:
                    clip_len = s2_struct.align_end - s1_struct.align_end
                else:
                    clip_len = s1_struct.clip_end_len
                if clip_len <= clip_tolerance:
                    return True
            # both are clipped
            else:
                clip_pos_s = s1_struct.clip_start
                clip_pos_e = s1_struct.clip_end
                if clip_pos_s > s2_struct.align_pos:
                    clip_len_s = s1_struct.clip_start_len
                else:
                    clip_len_s = s1_struct.align_pos - s2_struct.align_pos
                if clip_pos_e > s2_struct.align_end:
                    clip_len_e = s2_struct.align_end - s1_struct.align_end
                else:
                    clip_len_e = s1_struct.align_end
                if (clip_len_s <= clip_tolerance) and (clip_len_e <= clip_tolerance):
                    return True
        # seq 2 overlaps at the beginning
        elif s1_struct.align_pos <= s2_struct.align_pos <= s1_struct.align_end:
            clip_pos = s2_struct.clip_start
            if clip_pos < s1_struct.align_pos:
                clip_len = s2_struct.align_pos - s1_struct.align_pos
            else:
                clip_len = s2_struct.clip_start_len
            if clip_len <= clip_tolerance:
                return True
        elif s1_struct.align_pos <= s2_struct.align_end <= s1_struct.align_end:
            clip_pos = s2_struct.align_end
            if clip_pos > s1_struct.align_end:
                clip_len = s1_struct.align_end - s2_struct.align_end
            else:
                clip_len = s2_struct.clip_end_len
            if clip_len <= clip_tolerance:
                return True
        # now seq 1 is the one that partially overlaps seq 1
        elif s2_struct.align_pos <= s1_struct.align_pos <= s2_struct.align_end:
            clip_pos = s1_struct.clip_start
            if clip_pos < s2_struct.align_pos:
                clip_len = s1_struct.align_pos - s2_struct.align_pos
            else:
                clip_len = s1_struct.clip_start_len
            if clip_len <= clip_tolerance:
                return True
        elif s2_struct.align_pos <= s1_struct.align_end <= s2_struct.align_end:
            clip_pos = s1_struct.align_end
            if clip_pos > s2_struct.align_end:
                clip_len = s2_struct.align_end - s1_struct.align_end
            else:
                clip_len = s1_struct.clip_end_len
            if clip_len <= clip_tolerance:
                return True

    # not supported
    return False

def find_overlap(s1_struct: STRUCTURE, s2_struct: STRUCTURE, clip_tolerance: int, min_per: float):
    """determine if two alignments have an overlap"""
    overlap = False

    # rearrange
    if s1_struct.align_pos > s2_struct.align_pos:
        s1_struct, s2_struct = s2_struct, s1_struct

    if s1_struct.align_pos <= s2_struct.align_pos <= s1_struct.align_end:
        overlap = True
    elif s2_struct.align_pos <= s1_struct.align_pos <= s2_struct.align_end:
        overlap = True
    if s1_struct.align_pos <= s2_struct.align_end <= s1_struct.align_end:
        overlap = True
    elif s2_struct.align_pos <= s1_struct.align_end <= s2_struct.align_end:
        overlap = True

    if overlap:
        if (s1_struct.clipfree) and (s2_struct.clipfree):
            return overlap
        else:

            num_passes = 0
            
            # calc & overlap between the two
            cov_bases       = calc_overlap(s1_struct, s2_struct)
            s1_prop_aligned = (cov_bases / s1_struct.num_align_bp) * 100
            s2_prop_aligned = (cov_bases / s2_struct.num_align_bp) * 100

            if (s1_prop_aligned >= min_per) and (s2_prop_aligned >= min_per):
                num_passes += 1
            # both are clipped at the beginning
            if (s1_struct.clipping_start) and (s2_struct.clipping_start):
                if s1_struct.align_pos < s2_struct.align_pos:
                    if s1_struct.align_pos < s2_struct.clip_start:
                        clip_dist = s2_struct.clip_start_len
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                    else:
                        clip_dist = s2_struct.align_pos - s1_struct.align_pos
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                elif s2_struct.align_pos < s1_struct.align_pos:
                    if s2_struct.align_pos < s1_struct.clip_start:
                        clip_dist = s1_struct.clip_start_len
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                    else:
                        clip_dist = s1_struct.align_pos - s2_struct.align_pos
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
            # only 1 sequence is clipped 
            elif s1_struct.clipping_start:
                if s1_struct.align_pos < s2_struct.align_pos: # clip is before overlap
                    num_passes += 1
                elif s1_struct.clip_start < s2_struct.align_pos < s1_struct.align_pos:
                    clip_dist = s1_struct.align_pos - s2_struct.align_pos
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s2_struct.align_pos < s1_struct.align_pos < s2_struct.align_end:
                    clip_dist = s1_struct.clip_start_len
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s2_struct.align_pos < s1_struct.clip_start < s2_struct.align_end:
                    clip_dist = s2_struct.align_end - s1_struct.clip_start
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
            # seq 2 is clipped at the start
            elif s2_struct.clipping_start:
                if s2_struct.align_pos < s1_struct.align_pos: # clip is before overlap
                    num_passes += 1
                elif s2_struct.clip_start < s1_struct.align_pos < s2_struct.align_pos:
                    clip_dist = s2_struct.align_pos - s1_struct.align_pos
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s1_struct.align_pos < s2_struct.align_pos < s1_struct.align_end:
                    clip_dist = s2_struct.clip_start_len
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s1_struct.align_pos < s2_struct.clip_start < s1_struct.align_end:
                    clip_dist = s1_struct.align_end - s2_struct.clip_start
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
            # now for the clipping ends
            if (s1_struct.clipping_end) and (s2_struct.clipping_end):
                if s2_struct.align_end < s1_struct.align_end:
                    if s2_struct.clip_end < s1_struct.align_end:
                        clip_dist = s2_struct.clip_end_len
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                    else:
                        clip_dist = s1_struct.align_end - s2_struct.align_end
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                elif s1_struct.align_end < s2_struct.align_end:
                    if s1_struct.clip_end < s2_struct.align_end:
                        clip_dist = s1_struct.clip_end_len
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                    else:
                        clip_dist = s2_struct.align_end - s1_struct.align_end
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
            elif s1_struct.clipping_end:
                if s2_struct.align_end < s1_struct.align_end:
                    num_passes += 1
                elif s1_struct.align_end < s2_struct.align_end < s1_struct.clip_end:
                    clip_dist = s2_struct.align_end - s1_struct.align_end
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s1_struct.align_end < s2_struct.align_end:
                    if s1_struct.clip_end < s2_struct.align_end:
                        clip_dist = s1_struct.clip_end_len
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
                    else:
                        clip_dist = s2_struct.align_end - s1_struct.align_end
                        if clip_dist <= clip_tolerance:
                            num_passes += 1
            elif s2_struct.clipping_end:
                if s1_struct.align_end < s2_struct.align_end:
                    num_passes += 1
                elif s2_struct.align_end < s1_struct.align_end < s2_struct.clip_end:
                    clip_dist = s1_struct.align_end - s2_struct.align_end
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
                elif s2_struct.align_end < s1_struct.align_end:
                    if s2_struct.clip_end < s1_struct.align_end:
                        clip_dist = s2_struct.clip_end_len
                    else:
                        clip_dist = s1_struct.align_end - s2_struct.align_end
                    if clip_dist <= clip_tolerance:
                        num_passes += 1
            if num_passes < 2:
                overlap = False

    return overlap


def make_group_rep(align_structs: dict, seqs: set):
    """create a representing alignment using the aligned blocks for the seqs"""

    # first, lets sort by first position of covered regions
    sorted_seqs = [s for s, _ in sorted(align_structs.items(), key = lambda item:item[1].covered_regions[0][0]) if s in seqs]

    # initialize with first alignment (is this really better than using copy.deepcopy?)
    first_blk  = align_structs[sorted_seqs[0]].covered_regions[0][0] + 0 # add 0 to make copy
    second_blk = align_structs[sorted_seqs[0]].covered_regions[0][1] + 0 
    group_blks = [[first_blk, second_blk]]

    if len(seqs) < 2:
        return group_blks # only 1 seq

    for seq in sorted_seqs[1:]:
        seq_struct = align_structs[seq]
        for blk in seq_struct.covered_regions:
            blk_start = blk[0]
            blk_end   = blk[1]
            added     = False
            # now to add the current blk to the group blocks
            for i, rep_blk in enumerate(group_blks):
                rep_start = rep_blk[0]
                rep_end   = rep_blk[1]
                if rep_start <= blk_start <= blk_end <= rep_end:
                    added = True
                    break # end rep_blk loop
                elif rep_start <= blk_start <= rep_end <= blk_end:
                    rep_blk[1] = blk_end
                    added = True
                    break # break to move onto next seq block
                elif blk_start <= rep_start <= blk_end <= rep_end:
                    rep_blk[0] = blk_start
                    added = True
                    break
                elif blk_start <= rep_start <= rep_end <= blk_end:
                    rep_blk[0] = blk_start
                    rep_blk[1] = blk_end
                    added = True
                    break
                elif blk_end < rep_start:
                    if i == 0:
                        # add to the beginning
                        group_blks.insert(i, blk)
                        added = True
                        break
                    elif group_blks[i-1][1] <= blk_start < rep_start:
                        # insert in-between two blocks
                        if blk_start == group_blks[i-1][1]:
                            group_blks[i-1][1] = blk_end
                            added = True
                            break
                        else:
                            group_blks.insert(i, blk)
                            added = True
                            break
                    elif group_blks[i-1][0] < blk_start < group_blks[i-1][1] < rep_start:
                        # add to previous block
                        group_blks[i-1][1] = blk_end
                        added = True
                        break
            # extend the covered spots
            if not added and (blk_start > group_blks[-1][1]):
                group_blks.append(blk)

    return group_blks
                    
def covered_by_rep(seq1_struct: STRUCTURE, rep_seq: list, del_tol: int, clip_tolerance: int, align_offset: int):
    "check if a block in a representative sequence group covers an alignment blocks"

    for blk in rep_seq:
        # offset from left & right
        blk_start = blk[0] - align_offset
        blk_end = blk[1] + align_offset
        if blk_start <= seq1_struct.align_pos <= seq1_struct.align_end <= blk_end:
            if seq1_struct.clipfree and seq1_struct.num_del == 0:
                return True
            passes = 0
            if seq1_struct.clipping_start:
                if blk_start <= seq1_struct.clip_start:
                    if seq1_struct.clip_start_len <= clip_tolerance:
                        passes += 1
                else:
                    clip_dist = seq1_struct.align_pos - blk_start
                    if clip_dist <= clip_tolerance:
                        passes += 1
            else:
                passes += 1
            if seq1_struct.clipping_end:
                if blk_end >= seq1_struct.clip_end:
                    if seq1_struct.clip_end_len <= clip_tolerance:
                        passes += 1
                else:
                    clip_dist = blk_end - seq1_struct.align_end
                    if clip_dist <= clip_tolerance:
                        passes += 1
            else:
                passes += 1
            if seq1_struct.num_del > 0:
                tot_del_length = sum(seq1_struct.del_lengths)
                if tot_del_length <= del_tol:
                    passes += 1
            else:
                passes += 1
            if passes == 3:
                return True
            
    return False

def extend_to_rep(seq1_struct: STRUCTURE, rep_seq: list, clip_tolerance: int, align_offset: int):
    """if the sequence can be added to the ends of the represented group"""

    last_blk_num = len(rep_seq) - 1
    tot_blocks   = len(rep_seq)

    for i, blk in enumerate(rep_seq):
        blk_start = blk[0] - align_offset
        blk_end   = blk[1] + align_offset
        if (tot_blocks == 1):
            if ((seq1_struct.align_pos <= blk_start <= seq1_struct.align_end <= blk_end) and seq1_struct.clip_end_len <= clip_tolerance) or \
                (seq1_struct.align_pos <= blk_start <= blk_end <= seq1_struct.align_end) or \
                ((blk_start <= seq1_struct.align_pos <= blk_end <= seq1_struct.align_end) and seq1_struct.clip_start_len <= clip_tolerance):
                return True
            if (seq1_struct.clip_start_len > 0):
                if (blk_start < seq1_struct.align_pos - seq1_struct.clip_start_len):
                    if (seq1_struct.clip_start_len > clip_tolerance):
                        return False
                    else:
                        return True
                elif (blk_start < seq1_struct.align_pos):
                    if (seq1_struct.align_pos - blk_start < clip_tolerance):
                        return True
                    else:
                        return False
            if (seq1_struct.clip_end_len > 0):
                if (blk_start <= seq1_struct.align_end <= blk_end):
                    if (seq1_struct.align_end + seq1_struct.clip_end_len < blk_end):
                        if (seq1_struct.clip_end_len <= clip_tolerance):
                            return True
                        else:
                            return False
                    elif (blk_end - seq1_struct.align_pos <= clip_tolerance):
                        return True
                    else:
                        return False
        if i == 0:
            okayed = False
            if seq1_struct.align_pos <= blk_start <= seq1_struct.align_end <= blk_end or \
               seq1_struct.align_pos <= blk_start <= blk_end <= seq1_struct.align_end:
                okayed = True
        if not okayed:
            if i == last_blk_num:
                if (blk_start <= seq1_struct.align_pos <= blk_end <= seq1_struct.align_end) and \
                    (((blk_start - seq1_struct.align_pos) <= clip_tolerance) or seq1_struct.clip_start_len < clip_tolerance):
                    okayed = True
            else:
                continue
        if okayed:
            passed = False
            if i == 0 or tot_blocks == 1:
                if seq1_struct.clipping_end:
                    if seq1_struct.clip_end_len <= clip_tolerance:
                        passed = True
                else:
                    passed = True
            if passed == False:
                if i == last_blk_num or tot_blocks == 1:
                    if seq1_struct.clipping_start:
                        if seq1_struct.clip_start_len <= clip_tolerance:
                            passed = True
                    else:
                        passed = True
            if passed:
                return True
    return False

def compare_alignments(s1_struct : STRUCTURE, s2_struct: STRUCTURE, klump_info: bool, s1_klumps: list, s2_klumps: list,
                       del_tol: int, del_windows: List[Del_Window], align_offset: int, percent_overlap: float, clip_tolerance: int):
    """compare the structs of 2 alignments"""
    
    # no proof yet
    cscore = C_Score()

    # first, flag down clear examples of incompatibilities
    if s1_struct.clipping_start:
        if s1_struct.clip_start <= s2_struct.align_pos <= s2_struct.align_end <= s1_struct.align_pos:
            cscore.incompatible = True
            return cscore
    if s2_struct.clipping_start:
        if s2_struct.clipping_start <= s1_struct.align_pos <= s1_struct.align_end <= s2_struct.align_pos:
            cscore.incompatible = True
            return cscore
    if s1_struct.clipping_end:
        if s1_struct.align_end <= s2_struct.align_pos <= s2_struct.align_end <= s1_struct.clip_end:
            cscore.incompatible = True
            return cscore
    if s2_struct.clipping_end:
        if s2_struct.align_end <= s1_struct.align_pos <= s1_struct.align_end <= s2_struct.clip_end:
            cscore.incompatible = True
            return cscore

    # it is possible that they can be grouped
    # need to gather evidence
    cscore.possible = True

    # do they overlap at all
    if s1_struct.align_pos <= s2_struct.align_pos <= s1_struct.align_end:
        cscore.evidence += 1
        # cscore.POE.append("s1 align_pos <= s2 align_pos <= s1 align_end")
    elif s2_struct.align_pos <= s1_struct.align_pos <= s2_struct.align_end:
        cscore.evidence += 1
        # cscore.POE.append("s2 align_pos <= s1 align_pos <= s2 align_end")
    # overlapping at the 3' 
    if s1_struct.align_pos <= s2_struct.align_end <= s1_struct.align_end:
        cscore.evidence += 1
        # cscore.POE.append("s1 align_pos <= s2 align_end <= s1 align_end:")
    elif s2_struct.align_pos <= s1_struct.align_end <= s2_struct.align_end:
        cscore.evidence += 1
        # cscore.POE.append("s2 align_pos <= s1 align_end <= s2 align_end")
    # no evidence so they align at separate parts of the assembly
    if cscore.evidence == 0:
        return cscore # these two cannot be bridged on their own
    
    # alternatively, if evidence is 2 and they both are in agreement
    # with the reference, they are compatible
    if (s1_struct.num_blocks == 1) and (s1_struct.clipfree) and (s2_struct.num_blocks == 1) and (s2_struct.clipfree):
        if (cscore.evidence  == 2):
            cscore.groupable = True
            return cscore
    
    # are there any deletions overlapping the sequences
    if (s1_struct.num_blocks > 1) or (s2_struct.num_blocks > 1):
        # check if they can be grouped
        for del_wind in del_windows:
            if (s1_struct.seq_name in del_wind.seqs) and (s2_struct.seq_name in del_wind.seqs):
                cscore.groupable = True
                return cscore
          
        #check if start & end positions of blocks match
        for blk1 in s1_struct.covered_regions:
            blk1_start = blk1[0]
            blk1_end = blk1[1]
            for blk2 in s2_struct.covered_regions:
                blk2_start = blk2[0]
                blk2_end = blk2[1]
                if Within_Range(blk1_start, blk2_start, align_offset):
                    cscore.groupable = True
                    return cscore
                elif Within_Range(blk1_end, blk2_end, align_offset):
                    cscore.groupable = True
                    return cscore
                
        # check both ways if non-grouped seqs are incompatible
        incomp = check_blocks(s1_struct, s2_struct, del_tol)
        if incomp:
            cscore.incompatible = True
            return cscore
        incomp = check_blocks(s2_struct, s1_struct, del_tol)
        if incomp:
            cscore.incompatible = True
            return cscore
    
    # calc & overlap between the two
    cov_bases       = calc_overlap(s1_struct, s2_struct)
    s1_prop_aligned = (cov_bases / s1_struct.num_align_bp) * 100
    s2_prop_aligned = (cov_bases / s2_struct.num_align_bp) * 100

    # check if they can grouped
    if (s1_prop_aligned >= percent_overlap) and (s2_prop_aligned >= percent_overlap):
        cscore.evidence += 1
        # cscore.POE.append("s1_prop_aligned >= per overlap and s2_prop_aligned >= per overlap")
        acceptable = check_clip_status(s1_struct, s2_struct, clip_tolerance)
        if acceptable:
            cscore.groupable = True
            return cscore 

    # probability that two sequences align at the same spot is low, so that's evidence
    if s1_struct.align_pos == s2_struct.align_pos:
        cscore.evidence += 2
        cscore.likely = True
        # cscore.POE.append("s1 align_pos == s2 align_pos")
    elif Within_Range(s1_struct.align_pos, s2_struct.align_pos, align_offset):
        cscore.evidence += 1
        cscore.likely = True
        # cscore.POE.append("Within_Range(s1 align_pos, s2 align_pos, align_offset)")
    if s1_struct.align_end == s2_struct.align_end:
        cscore.evidence += 2
        cscore.likely = True
        # cscore.POE.append("s1 align_end == s2 align_end")
    elif Within_Range(s1_struct.align_end, s2_struct.align_end, align_offset):
        cscore.evidence += 1
        cscore.likely = True
        # cscore.POE.append("Within_Range(s1 align_end, s2 align_end, align_offset)")
    # same thing for deletions
    if s1_struct.num_del == s2_struct.num_del:
        cscore.evidence += 1
        # cscore.POE.append("s1 num_del == s2 num_del")
        # if deletions are the same length, that is strong evidence
        if s1_struct.num_del > 0:
            if sum(s1_struct.del_lengths) == sum(s2_struct.del_lengths):
                cscore.evidence += 1
                cscore.groupable = True
                # cscore.POE.append("sum(s1 del_lengths) == sum(s2 del_lengths)")
                return cscore

    # do they have the same number of blocks
    if s1_struct.num_blocks == s2_struct.num_blocks:
        # check for clear compatibilitiy
        if (s1_struct.num_blocks == 1) and (s2_struct.num_blocks == 1):
            acceptable = check_clip_status(s1_struct, s2_struct, clip_tolerance)
            if acceptable:
                cscore.evidence += 1
                # cscore.POE.append("check_clip_status(s1, s2, clip_tolerance) - acceptable")

    # do they have the same clipping patterns
    if s1_struct.clipping_start == s2_struct.clipping_start:
        cscore.evidence += 1
        # cscore.POE.append("s1 clipping_start == s2 clipping_start")
    if s1_struct.clipping_end == s2_struct.clipping_end:
        cscore.evidence += 1
        # cscore.POE.append("s1 clipping_end == s2 clipping_end")

    # use klump info if present
    if klump_info and (len(s1_klumps) > 0) and (len(s2_klumps) > 0):
        s1_sources = set()
        s2_sources = set()
        for k in s1_klumps:
            s1_sources.add(k.query_source)
        for k in s2_klumps:
            s2_sources.add(k.query_source)
        s1_diff = s1_sources.difference(s2_sources)
        s2_diff = s2_sources.difference(s1_sources)
        if len(s1_diff) == 0 or len(s2_diff) == 0:
            cscore.evidence += 1
            # cscore.POE.append("len(s1_diff) == 0 or len(s2_diff) == 0")
    
    if cscore.evidence >= 10:
        cscore.likely = True
    elif cscore.evidence >= 6:
        cscore.reasonable = True
    else:
        cscore.unlikely = True
    
    return cscore

def can_be_grouped(align_structs: dict, seq: str, del_tol: int, clip_tolerance: int, per_overlap: float, 
                   seq_set: set, bck_trace: list = []):
    """looks for incompatibilities and overlap of seq 1 in reference to seq 2"""
    
    compatible = True
    overlap    = False

    s1_struct = align_structs[seq]

    # a check for clipping issues at certain stages
    if bck_trace:
        if not s1_struct.clipfree:
            if (s1_struct.clip_start_len > clip_tolerance) or (s1_struct.clip_end_len > clip_tolerance):
                for bck_seq in bck_trace:
                    acceptable = check_clip_status(s1_struct, align_structs[bck_seq], clip_tolerance)
                    if not acceptable:
                        return acceptable, overlap

    for seq2 in seq_set:
        # this happens when trying to group seqs that need grouping
        if seq == seq2:
            continue
        s2_struct = align_structs[seq2]
        if not s2_struct.trustworthy:
            continue
        incompatible = check_blocks(s1_struct, s2_struct, del_tol)
        if incompatible:
            compatible = False
            return compatible, overlap
        if find_overlap(s1_struct, s2_struct, clip_tolerance, per_overlap):
            overlap = True 

    return compatible, overlap

def Group_Seqs(alignments: dict, leftbound: int, rightbound: int, ref: str, align_offset: int, 
               clip_tolerance: int, del_tol: int, per_overlap: float, klump_info: bool, 
               seq_klumps: dict, t_len: int, t_per: float, group_dels: bool, write_groups: bool,
               min_grp: int, write_edge_seqs: bool, limit: int, scan: bool):
    """group sequences by alignment patterns"""

    if not scan:
        print("Grouping sequences..")

    coverage = len(alignments)

    if coverage > limit:
        if not scan:
            print(f"Randomly subsampling {limit} alignment records for grouping analysis")
        alignments = dict(random.sample(alignments.items(), limit))

    # keep track of the structure of each alignment
    align_structs = {}

    # keep track of the alignment positions for each sequence
    align_starts  = {}

    left_flank  = leftbound # default
    right_flank = rightbound

    del_windows  = []
    clipped_seqs = []
    good_aligns  = set()
    align_num    = 0

    # fill out using alignments
    for seq, aligns in alignments.items():
        if seq == ref:
            continue
        # only using primary alignments
        for align in aligns:
            if align.IsPrimary: # only groups primary alignments
                clip_start_len = align.adjust_start
                clipping_start = align.clipping_start
                clip_end_len   = align.adjust_end
                clipping_end   = align.clipping_end
                align_pos      = align.position
                align_len      = align.aligned_length
                align_blocks   = align.align_blocks.blocks
                del_blocks     = align.align_blocks.block_del
                align_end      = align_pos + align_len - 1
                per_align      = align.percent_aligned
                # check for blocks out of chrom bound
                if clipping_start == None:
                    clip_start     = align_pos # range will not produce a value
                    clip_start_len = 0
                    clipping_start = False
                else:
                    clip_start = align_pos - clip_start_len
                    clipping_start = True
                if clipping_end == None:
                    clip_end     = align_end
                    clip_end_len = 0
                    clipping_end = False
                else:
                    clip_end     = align_end + clip_end_len
                    clipping_end = True
                # do a check here so I don't have to put several checks if already added
                if clipping_start or clipping_end:
                    clipped_seqs.append(seq)
                # keep record of alignment structure
                covered_regions  = []
                deletion_regions = []
                seq_len          = align.seq_len
                num_blocks       = len(align_blocks)
                del_lengths      = list(del_blocks.values())
                del_lengths      = del_lengths[:-1] # last block always has 0 deletions
                num_dels         = len(del_lengths)
                num_align_bp     = 0
                blk_start = align_pos
                for blk in align_blocks:
                    blk_len = align_blocks[blk]
                    del_len = del_blocks[blk]
                    blk_end = blk_start + blk_len
                    blk_tup = [blk_start, blk_end]
                    num_align_bp += blk_len
                    covered_regions.append(blk_tup)
                    del_start = blk_end + 1
                    del_end   = del_start + del_len   
                    del_tup   = [del_start, del_end]
                    if del_start != del_end:
                        if len(del_windows) == 0:
                            first_wind = Del_Window(del_start, del_end, seq)
                            del_windows.append(first_wind)
                        else:
                            added = False
                            for del_win in del_windows:
                                if del_win.start_pos - del_tol <= del_start <= del_win.start_pos + del_tol:
                                    added = True
                                    if del_start < del_win.start_pos:
                                        del_win.start_pos = del_start
                                if del_win.end_pos - del_tol <= del_end <= del_win.end_pos + del_tol:
                                    added = True
                                    if del_end > del_win.end_pos:
                                        del_win.end_pos = del_end
                                if added:
                                    del_win.seqs.add(seq)
                                    break
                            if not added:
                                del_win = Del_Window(del_start, del_end, seq)
                                del_windows.append(del_win)
                    deletion_regions.append(del_tup)
                    blk_start = del_end + 1
                deletion_regions = deletion_regions[:-1] # remove last 0 length block
                struct = \
                    STRUCTURE(num_blocks, num_dels, del_lengths, align_pos, 
                              align_end, clipping_start, clipping_end,
                              clip_start_len, clip_end_len, covered_regions,
                              deletion_regions, clip_start, clip_end,
                              seq_len, per_align, num_align_bp, seq, align_num)
                struct.evaluate(t_len, t_per, clip_tolerance)
                if (struct.num_del == 0) and (struct.clipfree):
                    good_aligns.add(seq)
                align_structs[seq] = struct
                align_starts[seq]  = clip_start
                if clip_start < left_flank:
                    left_flank = clip_start
                if clip_end > right_flank:
                    right_flank = clip_end
                align_num += 1

    # sort from left to right and start from leftmost alignment
    sorted_good_aligns = []

    for s in dict(sorted(align_starts.items(), key = lambda x : x[1])).keys():
        if s in good_aligns:
            sorted_good_aligns.append(s)
 
    group_sets        = defaultdict(list)
    has_group         = set()
    compatibility_map = {}
    good_aligns.clear()

    # first, try to tile across with the "good" alignments and assume the reference
    # is correct. In other words, can we find a path across the region?

    ns = len(sorted_good_aligns)

    for i, seq in enumerate(sorted_good_aligns):
        seq1_struct = align_structs[seq]
        if seq not in compatibility_map:
            compatibility_map[seq] = {}
            seq1_klumps = seq_klumps.get(seq, []) # default to empty list
        if i + 1 == ns:
            break
        j = i
        for seq2 in sorted_good_aligns[i+1:]:
            j += 1
            if seq2 in compatibility_map[seq]:
                continue
            if seq2 not in compatibility_map:
                compatibility_map[seq2] = {}
            seq2_struct = align_structs[seq2]
            if not seq2_struct.trustworthy:
                continue
            seq2_klumps = seq_klumps.get(seq2, [])
            cscore      = compare_alignments(seq1_struct, seq2_struct, klump_info, seq1_klumps, seq2_klumps, 
                                             del_tol, del_windows, align_offset, per_overlap, clip_tolerance)
            if cscore.groupable:
                group_sets[seq].append(seq2)
                has_group.add(seq)
                has_group.add(seq2)
            compatibility_map[seq][seq2] = compatibility_map[seq2][seq] = cscore

    group_map     = {}
    grp_cnt       = 0
    grp_backtrace = defaultdict(set)

    for i, seq in enumerate(sorted_good_aligns):
        if seq not in has_group:
            continue
        if seq not in group_map:
            grp_cnt       += 1
            group_map[seq] = grp_cnt
            grp_backtrace[grp_cnt].add(seq)
        # else:
        #     continue
        grp_num         = group_map[seq]
        compatible_seqs = group_sets[seq]
        if i + 1 == ns:
            break
        j = i
        for seq2 in sorted_good_aligns[i+1:]:
            j += 1
            if (seq2 in group_map) or (align_structs[seq2].trustworthy == False):
                continue
            # if already considered groupable
            if (compatibility_map[seq][seq2].groupable):
                compatible, overlap = True, True
            else:
                compatible, overlap = \
                    can_be_grouped(align_structs, seq2, del_tol, clip_tolerance, 
                                   per_overlap, compatible_seqs, grp_backtrace[grp_num])
            if compatible:
                if overlap:
                    if seq2 not in group_map:
                        group_map[seq2] = grp_num
                        grp_backtrace[grp_num].add(seq2)
                # check the updated groups
                else:
                    j -= 1
                    while (j != i):
                        seq3 = sorted_good_aligns[j]
                        if seq3 in grp_backtrace[grp_num]:
                            if seq3 in compatibility_map[seq2]:
                                cscore = compatibility_map[seq2][seq3]
                                if (cscore.groupable) and (seq2 not in group_map):
                                    group_map[seq2] = grp_num
                                    grp_backtrace[grp_num].add(seq2)
                                    break
                        j -= 1
                    # align_num = align_structs[seq2].align_num
                    # for seq3 in reversed(sorted_good_aligns[:align_num - 1]):
                    #     if seq3 in grp_backtrace[grp_num]:
                    #         if seq3 in compatibility_map[seq2]:
                    #             cscore = compatibility_map[seq2][seq3]
                    #             if cscore.groupable and seq2 not in group_map:
                    #                 group_map[seq2] = grp_num
                    #                 grp_backtrace[grp_num].append(seq2)

    # no longer needed
    sorted_good_aligns.clear()
    clear_dict(group_sets)
    
    rep_seqs = {}
    for grp_id, seqs in grp_backtrace.items():
        rep_seqs[grp_id] = make_group_rep(align_structs, seqs)

    # now this is where we attempt to go through and add different seqs
    # ideally at each stage, the seqs needing grouping will grow smaller
    # and smaller

    for seq in align_starts.keys():
        if seq in group_map:
            continue
        if not align_structs[seq].trustworthy:
            continue
        seq1_struct = align_structs[seq]
        for grp_num, seq_rep in rep_seqs.items():
            # NOTE: true will only occur if the seq is within the rep
            compatible = covered_by_rep(seq1_struct, seq_rep, del_tol, clip_tolerance, align_offset)
            if compatible:
                group_map[seq] = grp_num
                grp_backtrace[grp_num].add(seq)
                break

    # next, group by deletion windows if there are any
    grp_num = len(grp_backtrace)
    del_seqs = []
    marked = set()
    for del_wind in del_windows:
        # putting seqs in same window, next to each other
        for seq in del_wind.seqs:
            if seq not in marked: 
                del_seqs.append(seq)
                marked.add(seq)
    
    # clear the marked set now
    marked.clear()

    # here, we compare all the seqs with deletions to one another
    for i, seq in enumerate(del_seqs):
        if seq not in compatibility_map:
            compatibility_map[seq] = {}
            seq1_klumps = seq_klumps.get(seq, []) # default to empty list
        seq1_struct = align_structs[seq]
        if i + 1 == len(del_seqs):
            break # avoid mem error
        for seq2 in del_seqs[i+1:]:
            # skip comparing twice
            if seq2 in compatibility_map[seq]:
                continue
            if seq2 not in compatibility_map:
                compatibility_map[seq2] = {}
            seq2_struct = align_structs[seq2]
            seq2_klumps = seq_klumps.get(seq2, [])
            cscore      = compare_alignments(seq1_struct, seq2_struct, klump_info, seq1_klumps, seq2_klumps, 
                                             del_tol, del_windows, align_offset, per_overlap, clip_tolerance)
            if cscore.groupable:
                has_group.add(seq)
                has_group.add(seq2)
            compatibility_map[seq][seq2] = compatibility_map[seq2][seq] = cscore
            
    del_seqs.clear()

    # next, we will group sequences containing deletions
    # will create an inverted map that will be used to group
    # seqs without deletions

    # here, we will move compatible seqs into the group map
    # before it was del_seqs?
    for seq, cscore_dict in compatibility_map.items():
        if seq not in group_map:
            grp_cnt = len(grp_backtrace) + 1
            group_map[seq] = grp_cnt
        grp_num = group_map[seq]
        if seq not in grp_backtrace[grp_num]:
            grp_backtrace[grp_num].add(seq)
        for seq2, cscore in cscore_dict.items():
            if seq2 in group_map:
                continue
            if cscore.groupable or cscore.likely:
                if seq2 not in group_map:
                    group_map[seq2] = grp_num
                    has_group.add(seq2)
                    if seq2 not in grp_backtrace[grp_num]:
                        grp_backtrace[grp_num].add(seq2)
            # assume alignments with deletions represent the same locus
            elif group_dels:
                compatible, overlap = \
                    can_be_grouped(align_structs, seq2, del_tol, clip_tolerance,
                                   per_overlap, grp_backtrace[grp_num])
                if compatible and overlap:
                    if seq2 not in group_map:
                        group_map[seq2] = grp_num
                        has_group.add(seq2)
                        if seq2 not in grp_backtrace[grp_num]:
                            grp_backtrace[grp_num].add(seq2)
    
    clear_dict(compatibility_map)

    # create new rep alignments
    for grp_id, seqs in grp_backtrace.items():
        rep_seqs[grp_id] = make_group_rep(align_structs, seqs)
        # if (grp_id not in rep_seqs) and (len(seqs) >= min_grp):

    # # now to added clipped seqs under the assumption that if they start at the same position, they are of the same locus
    clip_dict = defaultdict(list)
    
    in_set = set()
    for i, seq in enumerate(clipped_seqs):
        if seq in group_map:
            continue
        seq1_struct = align_structs[seq]
        if (not seq1_struct.trustworthy):
            continue
        if (i + 1 >= len(clipped_seqs)):
            # only clipped seq in the set of alignments
            if (len(clipped_seqs) == 1):
                clip_dict[seq] = []
                break
            continue
        for seq2 in clipped_seqs[i+1:]:
            seq2_struct = align_structs[seq2]
            if (not seq2_struct.trustworthy) or (seq2 in group_map):
                continue
            if Within_Range(seq1_struct.align_pos, seq2_struct.align_pos, align_offset) or \
                Within_Range(seq1_struct.align_end, seq2_struct.align_end, align_offset):
                clip_dict[seq].append(seq2)
                clip_dict[seq2].append(seq)
                in_set.add(seq)
                in_set.add(seq2)
        if (seq not in clip_dict):
            clip_dict[seq] = [] # will be a stand alone
            in_set.add(seq)

    # others will remain as a set of size 1
    for seq in clipped_seqs:
        if (seq not in in_set):
            clip_dict[seq] = []
    
    in_set.clear()

    # now we create a new dict and sort by the size of the clipping
    sorted_clips = {}
    for seq, seq_list in clip_dict.items():
        cur_max = align_structs[seq].clip_start_len + align_structs[seq].clip_end_len
        for s in seq_list:
            s_struct = align_structs[s]
            if (s_struct.clip_start_len + s_struct.clip_end_len) > cur_max:
                cur_max = s_struct.clip_start_len + s_struct.clip_end_len
        sorted_clips[seq] = cur_max
    
    sorted_clip_list = []
    for s in dict(sorted(sorted_clips.items(), key = lambda x : x[1])).keys():
        sorted_clip_list.append(s)


    # now to add the group map          
    # first, will attempt to add to trailing ends
    # of current groups

    for seq_name in sorted_clip_list:
        seq_list = clip_dict[seq_name]
        if seq_name not in group_map:
            compatible = False
            seq1_struct = align_structs[seq_name]
            for group_num, sequence_rep in rep_seqs.items():
                compatible = \
                      extend_to_rep(seq1_struct, sequence_rep,
                                    clip_tolerance, align_offset)
                if compatible:
                    group_map[seq_name] = group_num
                    break
            # if it remained false the entire time
            if not compatible:
                new_grp_num         = len(grp_backtrace) + 1
                group_map[seq_name] = new_grp_num
            # now use the group number for seq
            # to assign the other clipped sequences
            # that are within its alignment range
            seq_grp_num = group_map[seq_name]
            grp_backtrace[seq_grp_num].add(seq_name)
            for s in seq_list:
                if s not in group_map:
                    group_map[s] = seq_grp_num
                    grp_backtrace[seq_grp_num].add(s)
            # now to recreate the new rep sequence
            if compatible:
                rep_seqs[seq_grp_num] = make_group_rep(align_structs, grp_backtrace[seq_grp_num])

    # last bit of filtering
    grp_cnt   = 0
    to_remove = []
    rep_seqs.clear()
    for grp_id, seqs in grp_backtrace.items():
        if len(seqs) < min_grp:
            for seq in seqs:
                del group_map[seq]
            to_remove.append(grp_id)
        else:
            grp_cnt += 1
            rep_seqs[grp_cnt] = make_group_rep(align_structs, seqs)
        
    # remove from back trace
    for grp_id in to_remove:
        del grp_backtrace[grp_id]

    # if not scanning, then plot the results & maybe write output
    if not scan:

        msg = f"Found {grp_cnt} group"

        if grp_cnt == 1:
            print(msg)
        else:
            print(msg + 's')

        # rename arbitrary IDs
        tmp = {}
        for i, grp_id in enumerate(grp_backtrace):
            for seq in grp_backtrace[grp_id]:
                group_map[seq] = i
            tmp[i] = grp_backtrace[grp_id]
        grp_backtrace = tmp

        # create files to write groups to
        if write_groups:
            for grp, seqs in grp_backtrace.items():
                with open(f"Group{grp}_Seqs.fa", 'w') as fh:
                    for seq in seqs:
                        aligns = alignments[seq]
                        for a in aligns:
                            if a.IsPrimary:
                                line = f">{seq}\n{a.seq}\n"
                                fh.write(line)
                                break
            # now for the ungrouped seqs
            with open(f"Ungrouped_Seqs.fa" , 'w') as fh:
                for seq, aligns in alignments.items():
                    if seq not in group_map:
                        for a in aligns:
                            if a.IsPrimary:
                                line = f">{seq}\n{a.seq}\n"
                                fh.write(line)
                                break
        
        # create a dict of seqs with clips per group 
        # since we are already going through the alignments
        if write_edge_seqs:
            clip_dict  = defaultdict(list)
            final_grps = defaultdict(list)
                            
        # change color of alignments based on group number
        for seq, aligns in alignments.items():
            if seq == ref:
                continue
            elif seq not in group_map:
                for align in aligns:
                    align.seq_color = Feature_Color(1, 1, 1) # white is reserved for background & off switch
            else:
                grp    = group_map[seq]
                aligns = alignments[seq]
                for align in aligns:
                    if align.IsPrimary:
                        align.seq_color = alignment_plot.get_color(False, True, grp)
                        align.group_num = grp
                        # add seqs to write
                        if write_edge_seqs:
                            final_grps[grp].append(seq)
                            if not align_structs[seq].clipfree:
                                clip_dict[grp].append(seq)
                        break
        
        # if determining writing edge seqs
        if write_edge_seqs:
            # the idea is to check clip portions that the end of the covered regions
            # This currently requires reconstruction of rep seqs
            # TODO figure out a way to update rep seq earlier
            rep_seqs = {}
            for grp, seqs in final_grps.items():
                rep_seqs[grp] = make_group_rep(align_structs, seqs)

            # write out the list of clipped edge seqs for the group
            for grp in final_grps.keys():
                clipped_seqs = clip_dict[grp]
                # if no clip seqs present, continue
                if len(clipped_seqs) == 0:
                    continue
                outfh = open(f"Group{grp}_Edge_Seqs.txt", 'w')
                grp_blks = rep_seqs[grp]
                first_blk = grp_blks[0]
                last_blk = grp_blks[-1]
                wrote = False # if it stays False, remove empty file
                for seq in clipped_seqs:
                    written = False
                    seq1_struct = align_structs[seq]
                    if seq1_struct.clipping_start:
                        if seq1_struct.clip_start < first_blk[0] <= seq1_struct.align_pos:
                            outfh.write(seq + '\n')
                            written = True
                            wrote = True
                    if not written:
                        if seq1_struct.clipping_end:
                            if seq1_struct.align_pos <= last_blk[1] < seq1_struct.clip_end:
                                outfh.write(seq + '\n')
                                written = True
                                wrote = True
                outfh.close()
                # remove any empty files
                if not wrote:
                    os.remove(f"Group_{grp}_Informative_Seqs.txt")

        # colors have changed
        return alignments
    else:
        group_map.clear()
        for rep_sequence in rep_seqs.values():
            for blk in rep_sequence:
                if blk[0] <= leftbound <= rightbound <= blk[1]:
                    return grp_cnt
        clear_dict(grp_backtrace)
        align_structs.clear()
        # none were able to be tiled
        return (grp_cnt * -1)

        
def within_window(seq_pos: int, align_blocks: algn_blocks, start: int, end: int, clipped_start: int):
    """determine if the sequence is within the current and next window"""

    # current window
    if start <= seq_pos <= end:
        return True
    elif start <= seq_pos - clipped_start <= end:
        return True
    elif start <= seq_pos + align_blocks.aligned_length <= end:
        return True
    elif start <= seq_pos + (align_blocks.covered_len - clipped_start) <= end:
        return True
    elif seq_pos <= start <= seq_pos + align_blocks.aligned_length:
        return True
    elif seq_pos <= end <= seq_pos + align_blocks.aligned_length:
        return True
    elif seq_pos <= start <= seq_pos + (align_blocks.covered_len - clipped_start):
        return True
    elif seq_pos <= end <= seq_pos + (align_blocks.covered_len - clipped_start):
        return True

    return False
