
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

class Seq_Record:
    
    @staticmethod
    def reverse_complement(seq: str):
        """reverse complement a seq"""

        seq_rc = ""

        rc_dict = {'A':'T',
                   'T':'A',
                   'C':'G', 
                   'G':'C',
                   'N':'N',
                   '-':'-',
                   'K':'M', # G||T : C||A
                   'M':'K', # C||A : G||T
                   'W':'W', # A||T : T||A
                   'S':'S', # G||C : C||G
                   'R':'Y', # A||G : T||C
                   'Y':'R', # T||C : A||G
                   'B':'V', # C||G||T : A||C||G
                   'V':'B', # A||C||G : C||G||T
                   'D':'H', # A||G||T : T||C||A
                   'H':'D'}

        for nuc in seq[::-1]:
            seq_rc += rc_dict[nuc.upper()]

        return seq_rc

    # construct record
    __slots__ = "seq_name", "seq", "seq_rc", "seq_length"

    def __init__(self, seq_name : str, seq: str):
        self.seq_name   = seq_name
        self.seq        = seq.upper()
        self.seq_rc     = Seq_Record.reverse_complement(seq) # will automatically create R.C.
        self.seq_length = len(seq)


    #use seq ID and assume short read
    def check_if_paired_end(self):
        if self.seq_length > 160:
            return False, None
        # short seq so check
        seq_name = self.seq_name
        #check /1 and /2 naming convenvtion
        if seq_name[-2:] in ["/1", "/2"]:
            if seq_name[-2:] == "/1":
                pair_num = 1
            else:
                pair_num = 2
            return True, pair_num
        #check seq_header [1|2]:[Y|N]:Num:Index convection
        elif len(seq_name.split(" ")) == 2:
            casava_info = seq_name.split(" ")[-1]
            if len(casava_info.split(":")) == 4:
                seq_info = casava_info.split(":")
                if seq_info[0] in ["1", "2"]:
                    # following casava 1.8 format
                    if seq_info[1].upper() in ["Y", "N"]:
                        paired   = True
                        pair_num = int(seq_info[0])
                    else:
                        paired   = False
                        pair_num = None
            else:
                paired   = False
                pair_num = None
            return paired, pair_num
        #error prone to conventional naming schemes
        else:
            return False, None

# store klump details
class Klump:
    def __init__(self, klump_name: str, start_pos: str, end_pos: str, query_source: str, klump_size: str, direction: str):
        self.klump_name   = klump_name
        self.start_pos    = int(start_pos)
        self.end_pos      = int(end_pos)
        self.query_source = query_source
        self.klump_size   = int(klump_size)
        self.direction    = direction
        self.pair_info    = False
        self.pair_num     = None
    
    # for paired data
    def add_pair_num(self, pair_num: int):
        self.pair_info = True
        self.pair_num  = pair_num


# for summarizing klumps
class KLUMPS:
    def __init__(self, seq_name: str):
        self.seq_name   = seq_name
        self.klumps     = []
        self.all_klumps = {}

    def add_klumps(self, klump: Klump):
        self.klumps.append(klump)

    # to keep details in one place
    def create_all_klumps(self):
        for klump in self.klumps:
            klump_name   = klump.klump_name
            start_pos    = int(klump.start_pos)
            end_pos      = int(klump.end_pos)
            query_source = klump.query_source
            size         = int(klump.klump_size)
            direction    = klump.direction
            self.all_klumps[klump_name] = [
                start_pos, end_pos, query_source, size, direction]

    def largest_klump(self):
        max_size = 0
        for klump in self.klumps:
            klump_size = klump.klump_size
            if klump_size > max_size:
                max_size = klump_size
        return max_size

    def num_of_klumps(self):
        return len(self.klumps)

    def show_me_klump(self, klump_name: str):
        if klump_name in self.all_klumps.keys():
            klumpInfo = self.all_klumps[klump_name]
            statement = f"{klump_name} has {klumpInfo[3]} k-mers from {klumpInfo[2]}: Positions - {klumpInfo[0]}:{klumpInfo[1]}"
            return statement

    def print_klumps(self):
        return self.all_klumps

    def klump_sizes(self):
        self.klmp_sizes = []
        for klmp_size in self.all_klumps.values():
            self.klmp_sizes.append(klmp_size[3])
        return self.klmp_sizes

    def queries(self):
        queries_list = list()
        for q in self.all_klumps.values():
            source = [s for s in q[2]]
            if source not in queries_list:
                queries_list.append(source)
        # flatten list
        flattened         = [query for source in queries_list for query in source]
        self.queries_list = flattened
        return self.queries_list

    def which_directions(self):
        self.directions = set()
        for k in self.all_klumps.values():
            # get directions
            self.directions.add(k[4])
        return self.directions

    def both_strands(self):
        strand_directions = ""
        for q in self.all_klumps.values():
            strand_directions += q[4]
        if 'F' in strand_directions and 'R' in strand_directions:
            return True
        else:
            return False

    def distances(self):
      # get distances b/t klumps
        if len(self.all_klumps) == 1:
            self.dist = [0]
        else:
            self.dist = []
            initial = True
            for vals in self.all_klumps.values():
                # for initial ends
                if initial is True:
                    end     = vals[1]
                    initial = False
                else:
                    start = vals[0]
                    self.dist.append(abs(start - end))
                    # set new end
                    end = vals[1]
        return self.dist

class SAM_FLAG:
    def __init__(self, flag: int):
        self.primary       = False
        self.secondary     = False
        self.supplementary = False
        self.fwd_seq       = False
        self.rev_seq       = False
        if (flag & 256) == 256:
            self.secondary = True
        elif (flag & 2048) == 2048:
            self.supplementary = True
        else:
            self.primary = True

# class for blocks of the alignment when deletions are present
class algn_blocks:
    def __init__(self):
        self.blocks         = {}
        self.block_del      = {} # large gaps separating block
        self.MiniDels       = {} # gaps within block
        self.aligned_length = 0
        self.covered_len    = 0
        self.del_pos        = None # used to hold positions of each deletion

    def add_entry(self, block_num: int, block: list, deletion_len: str, del_cnt: int):
        block_id = f"block{block_num}"
        # avoid putting gap cnt at beginning and end of block
        self.blocks[block_id]    = block # gaps within block
        self.block_del[block_id] = int(deletion_len)
        self.MiniDels[block_id]  = del_cnt

    # for clips, start block after clip
    def adjust_start(self):
        first_block           = self.blocks["block0"]
        clipped_site          = first_block[0]
        self.blocks["block0"] = first_block[1:] # get all but 1st element
        return clipped_site
        

    # for clips, adjust for last clipping
    def adjust_end(self, adjust_end: int):
        last_block              = list(self.blocks.keys())[-1]
        block                   = self.blocks[last_block]
        self.blocks[last_block] = sum(block) - adjust_end

    # to find overlapping alignments
    def covered_region(self, clipped_start: int, clipped_end: int):
        for block, values in self.blocks.items():
            # add deletion from within blocks
            del_cnt = self.MiniDels[block]
            # last block is type int, others are lists
            if type(values) == list:
                self.blocks[block]   = sum(values) + del_cnt
                self.aligned_length += sum(values) + del_cnt
            else:
                self.blocks[block]   = values + del_cnt
                self.aligned_length += values + del_cnt
        for value in self.block_del.values():
            self.aligned_length += value
        self.covered_len = self.aligned_length + clipped_start + \
                            clipped_end

    def get_ending_blocks(self):
        blocks = list(self.blocks.keys())
        if len(blocks) == 1:
            return blocks
        else:
            return [blocks[0], blocks[-1]]
        
    def add_del_pos(self, del_pos: dict):
        self.del_pos = del_pos

class SAM:
    # safe some space
    __slots__ = "seq_name", "position", "flag", "chromosome", "segment", "align_blocks", \
                "clipping_start", "adjust_start", "clipping_end", "adjust_end", "percent_aligned", \
                "seq_len", "IsPrimary", "map_num", "aligned_length", "pair_num", "seq_color", "seq", "group_num"
     
    def __init__(self, seq_name: str, position: int, flag: int, chromosome: str, 
                 segment: bool, align_blocks : dict, clipping_start: str, adjust_start: int, 
                 clipping_end: str, adjust_end: int, percent_aligned: float, seq_len: int, 
                 IsPrimary: bool, map_num=None):
        self.seq_name        = seq_name
        self.position        = int(position)
        self.flag            = int(flag)
        self.chromosome      = chromosome
        self.segment         = segment # for hard clips
        self.align_blocks    = align_blocks # aligned len (includes soft clips)
        self.aligned_length  = align_blocks.aligned_length
        self.clipping_start  = clipping_start
        self.adjust_start    = adjust_start
        self.clipping_end    = clipping_end
        self.adjust_end      = adjust_end
        self.percent_aligned = float(percent_aligned)
        self.seq_len         = seq_len
        self.IsPrimary       = IsPrimary
        self.map_num         = map_num #  used to figure out if a particular alignment 
                                       #  overlaps with another
        self.pair_num        = 0 # modify after initialization
        self.seq_color       = ""
        self.seq             = ""
        self.group_num       = None

class Feature_Color:
    __slots__ = "red", "green", "blue", "alpha", "name"

    def __init__(self, red: float, green: float, blue: float, alpha = 1, name = None):
        self.red   = red
        self.green = green
        self.blue  = blue
        self.alpha = alpha
        self.name  = name

# will serve as a parent class for classes with start & end position members
class Positions:
    def __init__(self, start_pos: int, end_pos: int):
        self.start_pos = int(start_pos)
        self.end_pos   = int(end_pos)

class EXON(Positions):
    __slots__ = "start_pos", "end_pos", "direction", "gene_color", "gene_name"
    def __init__(self, start_pos: int, end_pos: int, direction: str, gene_color: Feature_Color):
        super().__init__(start_pos, end_pos)
        self.direction  = direction
        self.gene_color = gene_color
        self.gene_name  = None
    
    def add_gene_name(self, gene_name: str):
        self.gene_name = gene_name

class GENE(Positions):
    def __init__(self, start_pos: int, end_pos: int, gene_name: str):
        super().__init__(start_pos, end_pos)
        self.gene_name = gene_name

class GAP(Positions):
    pass

class Kmer:
    __slots__ = "pos", "query", "direction"

    def __init__(self, pos: int, query: str, direction: str):
        self.pos       = int(pos)
        self.query     = query
        self.direction = direction

class STRUCTURE:

    __slots__ = "num_blocks", "num_del", "del_lengths", "align_pos", "align_end", "clipping_start", \
                "clipping_end", "clip_start_len", "clip_end_len", "covered_regions", "deletion_regions", \
                "clip_start", "clip_end", "seq_len", "percent_align", "num_align_bp", "seq_name", \
                "align_num", "clipfree", "trustworthy"
    
    def __init__(self, num_blocks: int, num_del: int, del_lengths: list, align_pos: int, 
                 align_end: int, clipping_start: str, clipping_end: str, clip_start_len: int, 
                 clip_end_len: int, covered_regions: list, deletion_regions: list, 
                 clip_start: int, clip_end: int, seq_len: int, percent_align: float, 
                 num_align_bp: int, seq_name: str, align_num: int):
        self.num_blocks       = num_blocks
        self.num_del          = num_del
        self.del_lengths      = del_lengths
        self.align_pos        = align_pos
        self.align_end        = align_end
        self.clipping_start   = clipping_start
        self.clipping_end     = clipping_end
        self.clip_start_len   = clip_start_len
        self.clip_end_len     = clip_end_len
        self.covered_regions  = covered_regions # struct [[int, int], [int, int], ..]
        self.deletion_regions = deletion_regions
        self.clip_start       = clip_start
        self.clip_end         = clip_end
        self.seq_len          = seq_len
        self.percent_align    = percent_align
        self.num_align_bp     = num_align_bp
        self.seq_name         = seq_name
        self.align_num        = align_num
        # members to be checked upon evaluation
        self.clipfree         = True
        self.trustworthy      = True

    def evaluate(self, min_len: int, t_per: float, clip_tolerance: int):
        if (self.clip_start_len <= clip_tolerance) and (self.clip_end_len <= clip_tolerance):
            self.clipfree = True
        else:
            self.clipfree = False
        if self.seq_len < min_len or self.percent_align < t_per:
            self.trustworthy = False

class Del_Window(Positions):
    def __init__(self, start_pos: int, end_pos: int, seq: str):
        super().__init__(start_pos, end_pos)
        self.seqs = set([seq])

    def __str__(self):
        s = f"Start: {self.start_pos}, End: {self.end_pos}, Seqs: {list(self.seqs)}"
        return s 

# compatibility score
class C_Score:
    __slots__ = "incompatible", "groupable", "likely", "reasonable", "unlikely", \
                "possible", "evidence", "POE"

    def __init__(self):
        self.incompatible = False
        self.groupable    = False
        self.likely       = False
        self.reasonable   = False
        self.unlikely     = False
        self.possible     = False
        self.evidence     = 0
        self.POE          = []

    def __str__(self):
        s = f"Incompatibility = {self.incompatible}, Groupable = {self.groupable}, " + \
            f"Likely = {self.likely}, Reasonable = {self.reasonable}, Unlikely = {self.unlikely}, " + \
            f"Possible = {self.possible}"
        return s 
    
# to retain gene identifiers in GTF/GFF files
class GeneRecord:
    def __init__(self):
        self.gene_name  = None # GTF ids
        self.gene_id    = None
        self.id         = None # GFF ids
        self.prot_id    = None
        self.parent     = None # to trace back to ID
        self.name       = None # may be the same as ID in some cases
        self.other_ids  = set() # store other ids for the record
        self.visited    = list() # to know if a new record has been encountered
        self.exon_list  = list()
        self.prev_added = set() # just in case exon already added
        self.retain     = list() # to store entries not added to visited
        self.ref        = None # used for get exons to remember which ref seq

    def prune_id(gene_id: str):
        # remove extra information from gene attributes subfield 
        # not a optimal approach as it keeps reconstructing a str obj

        for s in ["gene", "exon", "rna", "transcript"]:
            if gene_id.lower().startswith(s):
                s_len   = len(s)
                prunned = False
                for e in ['-', ':', '_']:
                    if gene_id.lower().startswith(f"{s}{e}"):
                        gene_id = gene_id[s_len:]
                        prunned = True
                        break
                if not prunned:
                    gene_id = gene_id[s_len-1:]
                break
        
        # check for trailing numbers
        p = len(gene_id) - 1
        while p >= 0:
            if gene_id[p] == '-':
                if (p + 1 != len(gene_id)):
                    if (gene_id[p+1:].isdigit()):
                        if (p - 1 >= 1):
                            if gene_id[p-2:].startswith(".1"):
                                gene_id = gene_id[:p]
                break
            p -= 1

        return gene_id

    # process the attributes field
    def parse_attributes(self, entry_info: str):

        info_map = {}

        # make a dict of the of the info
        for field in entry_info.split(';'):
            field    = field.strip()
            key_vals = field.split(' ')
            if len(key_vals) == 1: # not space separated
                key_vals = field.split('=') # assume = delimited
            try:
                id_key = key_vals[0].lower()
                 # remove quotes & spaces
                id_val           = key_vals[1].replace('"', '').replace(' ', '')
                id_val           = GeneRecord.prune_id(id_val)
                info_map[id_key] = id_val
            except:
                # if last field is empty
                continue

        # add whatever ids we obtained
        if "gene_id" in info_map:
            if self.gene_id == None:
                self.gene_id = info_map["gene_id"]
            else:
                self.other_ids.add(info_map["gene_id"])
        if "gene_name" in info_map:
            if self.gene_name == None:
                self.gene_name = info_map["gene_name"]
            else:
                self.other_ids.add(info_map["gene_name"])
        if "id" in info_map:
            if self.id == None: # hasn't been set by prev entry
                self.id = info_map["id"]
            else:
                self.other_ids.add(info_map["id"])
        if "protein_id" in info_map:
            if self.prot_id == None:
                self.prot_id = info_map["protein_id"]
            else:
                self.other_ids.add(info_map["protein_id"])
        if "name" in info_map:
            if self.name == None:
                self.name = info_map["name"]
            else:
                self.other_ids.add(info_map["name"])
        if "parent" in info_map:
            if self.parent == None:
                self.parent = info_map["parent"]
            else:
                self.other_ids.add(info_map["parent"])

    # following what I think is the hierarchy
    def get_gene_name(self):
        if self.gene_id != None:
            return self.gene_id
        elif self.gene_name != None:
            return self.gene_name
        elif self.name != None:
            return self.name
        elif self.id != None:
            return self.id
        elif self.prot_id != None:
            return self.prot_id
        elif self.parent != None:
            return self.parent
        elif len(self.other_ids) > 0:
                for i in self.other_ids:
                    return i # return 1st entry
        else:
            return "NA" # default
    
    # update current record info        
    def update(self, entry_type: str):
        if entry_type in self.visited:
            if entry_type != self.visited[-1]: # transitioning
                # some entries are cds cds cds .. exon exon exon
                # while others could be cds exon cds exon
                alter = None
                if entry_type == "exon":
                    alter = "cds"
                elif entry_type == "cds":
                    alter = "exon"
                # check for alternating
                if alter == None:
                    self.retain.append(entry_type)
                    return True
                elif self.visited[-1] == alter:
                    self.visited.append(entry_type) # keep pattern going
                else:
                    # i don't think this will ever be reached
                    # but better to be safe
                    self.retain.append(entry_type)
                    return True

        else:
            self.visited.append(entry_type)

        return False
    
        # reset object
    def clear(self):
        self.gene_name = None
        self.gene_id   = None
        self.id        = None
        self.prot_id   = None
        self.parent    = None
        self.name      = None
        self.other_ids.clear()
        self.visited.clear()
        self.exon_list.clear()
        self.prev_added.clear()
        self.ref       = None

        # move prev entries haven't added during update check
        self.visited = self.retain[::] # this should construct a new copy
        self.retain.clear()
     
    def add_exon(self, left: int, right: int, direction: str, gene_color: Feature_Color, line: str):
        
        # some safety checks
        if left > right:
            right, left = left, right
        assert left  >= 0, f"Encountered an entry where left ({left}) is less than 0. Offending line:\n{line}"
        assert right >= 0, f"Encountered an entry where right ({right}) is less than 0. Offending line:\n{line}"
        assert direction in ['+', '-'], f"Encountered an entry where direction ({direction}) cannot be determined. Offending line:\n{line}"
        
        # avoid dup entries
        if (left, right, direction) not in self.prev_added:
            self.exon_list.append(EXON(left, right, direction, gene_color))
            self.prev_added.add((left, right, direction)) # assuming positions will always be dup

    def empty(self):
        return len(self.exon_list) == 0
    
    def store_ref(self, ref: str):
        if self.ref == None:
            self.ref = ref
    
    def get_ref(self):
        return self.ref if self.ref != None else ''
    
    # a function for get_exons to see if id in any in the current ids
    def in_record(self, genes: list):
        # put all ids together
        all_ids = set()
        ids_    = [self.gene_id, self.gene_name, self.id, 
                   self.prot_id, self.parent, self.name]
        
        # non-Nones
        for i in ids_:
            if i != None:
                all_ids.add(i)
        
        # add just in case
        for i in self.other_ids:
            all_ids.add(i)
         
        # now check for id & bring the matching entry
        in_rec = False
        gen_id = ''
        for gene in genes:
            if gene in all_ids:
                in_rec = True
                gen_id = gene
                break
        
        return in_rec, gen_id

    # we add the exons in the bounds to the exons dict
    def incorporate(self, leftbound: int, rightbound: int, exons: dict, genes_found: list):

        geneName = self.get_gene_name()
        
        for i, exon in enumerate(self.exon_list, start = 1):
            keep = False
            if leftbound <= exon.start_pos <= rightbound:
                keep = True
                if exon.end_pos <= rightbound:
                    pass
                else:
                    exon.end_pos = rightbound
            elif leftbound <= exon.end_pos <= rightbound:
                keep = True
                exon.start_pos = leftbound
            elif exon.start_pos <= leftbound <= exon.end_pos:
                keep = True
                exon.start_pos = leftbound
            if keep:
                if geneName not in genes_found:
                    genes_found.append(geneName)
                exon_name = f"{geneName}_E{i}"
                exon.add_gene_name(geneName)
                exons[exon_name] = exon
            
        self.clear()
        return exons, genes_found
    
class Label_Position:
    def __init__(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4

    def shift_right(self, pixel_cnt: float):
        self.x1 += pixel_cnt
        self.x2 += pixel_cnt
        self.x3 += pixel_cnt
        self.x4 += pixel_cnt

    def make_tuple(self):
        return ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3), (self.x4, self.y4))

    def __str__(self):
        return f"x1, y1 {(self.x1, self.y1)}, x2, y2 {(self.x2, self.y2)}, x3, y3 {(self.x3, self.y3)}, x4, y4 {(self.x4, self.y4)}"