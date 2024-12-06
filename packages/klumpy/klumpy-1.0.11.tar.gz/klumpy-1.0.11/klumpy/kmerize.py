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
import gzip
import os
import concurrent.futures
from   collections import defaultdict
from   datetime import datetime
from  .Classes import Seq_Record

def check_params(args):
    """do some assertions and checking for Nones"""

    warning_color = "\033[93m"
    end_color     = "\033[0m"

    if args.subject == None:
        msg = "--subject is required for kmerize"
        sys.exit(msg)
    assert os.path.isfile(args.subject), f"Could not find {args.subject}"
    if args.query == None:
        msg = "--query is required for kmerize"
        sys.exit(msg)
    assert os.path.isfile(args.query), f"Could not find {args.query}"
     # check limit
    assert type(args.ksize) is int, "Ksize must be an integer"
    assert args.ksize > 0,          "Ksize must be greater than 0"
    # check limit
    assert type(args.limit) is int, "Limit value must be an integer"
    assert args.limit > 0,          "Limit must be greater than 0"
    #check thread number is appropriate
    assert type(args.threads) is int, "Threads value must be an integer"
    # check threads
    assert args.threads > 0, "--threads must be greater than 0"
    if args.threads > os.cpu_count():
        msg = f"Detected only {os.cpu_count()} threads. Reducing --threads count"
        print(f"{warning_color}{msg}{end_color}")

    # now we set a constant output name
    output = "query_map.gz"
    
    return args.subject, args.query, args.ksize, output, args.limit, args.threads

########################
### Parsing functions ###
########################


def load_fasta_file(fasta_file: str, limit: int, query_kmers: dict, query_map: dict, ksize: int,
                    output_fh, record_cnt: int, hits: int, seq_cnt: int, query: bool, thread_num: int):
    """read fasta file in limited chunks"""

    #set up params
    records = []
    seq     = ''
    id      = None

    # did the user explicitly add a limit?
    limit_checked = ("--limit" in sys.argv)

    #
    # Read a gzipped file without any intervention.
    #
    if fasta_file.endswith(".gz"):
        fh = gzip.open(fasta_file, "rt")
    else:
        fh = open(fasta_file, 'r')
 
   #minus 1 to get last record
    for line in fh:
        # skip empty or commented lines
        if len(line) == 0 or line.startswith('#'):
            continue
        line = line.strip()
        if line.startswith(">"):
            # for the 1st record
            if seq == "":
                id = line[1:]
                continue
            else:
                seq_len = len(seq)
                # working with a genome or just records?
                # if (seq_len >= 1000000) and (limit_checked == False) and (limit > 3):
                #     msg = "Detected sequneces of >= 1 MB. Reducing number of subject records " + \
                #         "read into memory to 3 at a time"
                #     print(msg)
                #     limit         = 3
                #     limit_checked = True
                #     thread_num    = min(thread_num, 3) 
                if seq_len >= ksize:
                    records.append(Seq_Record(id, seq))
                else:
                    print(f"Excluded {id} due to sequence length ({len(seq)}bp)")   
                seq = ''
                id  = line[1:]
                if (len(records) == limit) and (query == False):
                    record_cnt += len(records)
                    if record_cnt > 1:
                        s = "sequences"
                    else:
                        s = "sequence"
                    print(f"Loaded {record_cnt} {s} from {os.path.basename(fasta_file)}", end = "\r")
                    seq_cnt, matches = kmer_pipeline(records, query_kmers, query_map, ksize, 
                                                     output_fh, seq_cnt, thread_num)
                    hits   += matches
                    records = []
                else:
                    pass
        else:
            seq += line.upper()

    # for the last record
    if len(seq) >= ksize:
        records.append(Seq_Record(id, seq))


    #process remaining seqs
    record_cnt = record_cnt + len(records)
    if record_cnt > 1:
        s = "sequences"
    else:
        s = "sequence"
    print(f"Loaded {record_cnt} {s} from {os.path.basename(fasta_file)}", end = "\r")
    
    #need to return query before pipeline begins
    if query:
        return records
    
    seq_cnt, matches = kmer_pipeline(records, query_kmers, query_map, ksize, output_fh, seq_cnt, thread_num)
    hits            += matches

    return hits

    
def load_fastq_file(fastq_file: str, limit: int, query_kmers: dict, query_map: dict, ksize: int, 
                    output_fh, record_cnt: int, hits: int, seq_cnt: int, query: bool, thread_num: int):
    """load fastq file in limited chunks as dict"""


    #set up variables
    records = [] #for multiple records

    #create file handle
    if fastq_file.endswith(".gz"):
        fh = gzip.open(fastq_file, "rt")
    else:
        fh = open(fastq_file, 'r')

    # assume legal fastq file
    line_num   = 0
    seq_header = 'r'
    
    # same limit check as fasta function
    limit_checked = ("--limit" in sys.argv)

    #begin reading
    for line in fh:
        if (len(records)) == limit and (query == False):
            record_cnt += len(records)
            print(f"Loaded {record_cnt} sequences from {os.path.basename(fastq_file)}", end = "\r")
            seq_cnt, matches = kmer_pipeline(records, query_kmers, query_map,
                                             ksize, output_fh, seq_cnt,
                                             thread_num)
            hits   += matches
            records = []
        #currently assumes fastq has no oddities
        if len(line) == 0:
            sys.exit(f"Please remove empty lines in {os.path.basename(fastq_file)}")
        line_num += 1
        line      = line.strip()
        if line_num % 4 == 1 and line.startswith("@"):
            seq_header = line[1:]
        #4 lines = 1 record
        elif line_num % 4 == 2:
            seq_len = len(line)
            # same safety check here
            # if (seq_len >= 1000000) and (limit_checked == False) and (limit > 3):
            #     msg = "Detected sequneces of >= 1 MB. Reducing number of subject records " + \
            #             "read into memory to 3 at a time"
            #     print(msg)
            #     limit         = 3
            #     limit_checked = True
            #     thread_num    = min(thread_num, 3)  
            if seq_len >= ksize:
                records.append(Seq_Record(seq_header, line))
            else:
                print(f"Excluded {seq_header} due to a sequence length of ({seq_len}bp)")  

    fh.close()

    record_cnt += len(records)
    print(f"Loaded {record_cnt} sequences from {os.path.basename(fastq_file)}", end = "\r")
    #need to return query before pipeline begins
    if query:
        return records
    
    seq_cnt, matches = kmer_pipeline(records, query_kmers, query_map,
                                     ksize, output_fh, seq_cnt,
                                     thread_num)
    hits += matches
    
    return hits

def load_query_records(file: str, ksize: int):
    """decide loading method"""

    file_name = str(os.path.basename(file))
    fasta_ext = ["fa", "fasta", "fna", "faa"]
    fastq_ext = ["fastq", "fq"]

    # in case format could not be determined
    message = f"Could not determine file type for {os.path.basename(file)} using its file extension"
    
    if file_name.endswith(".gz"):
        file_ext = file.split(".")[-2]
    else:
        file_ext = file.split(".")[-1]
    
    if file_ext in fasta_ext:
        records = load_fasta_file(file, None,  None, None, 17, None, 0, 0, 1, True, 1)
    elif file_ext in fastq_ext:
        records = load_fastq_file(file, None, None, None, 17, None, 0, 0, 1, True, 1)
    else:
        sys.exit(message)

    if len(records) == 0:
        message = f"Loaded 0 sequences from {os.path.basename(file)}. Exiting.."
        sys.exit(message)

    # parse query
    query_kmers, query_map = parse_query(records, ksize)

    return query_kmers, query_map

def determine_parsing_fun(file: str):
    """determine which method to parse file"""

    file = os.path.basename(file)

    fasta_ext = ["fa", "fasta", "fna", "faa"]
    fastq_ext = ["fastq", "fq"]

    # in case format could not be determined
    message   = f"Could not determine file type for {os.path.basename(file)} using its file extension"

    if file.endswith(".gz"):
        file_ext = file.split(".")[-2]
    else:
        file_ext = file.split(".")[-1]
    
    if file_ext in fasta_ext:
        return "fasta"
    elif file_ext in fastq_ext:
        return "fastq"
    else:
        sys.exit(message)

def parse_query(query_records: list, ksize: int):
    """create query kmers"""

    #dict to separate different queries & orientations
    query_kmers = defaultdict(list)
    query_map   = {}

    for i, record in enumerate(query_records):
        query_id                     = record.seq_name
        query_seq                    = record.seq
        query_seq_rc                 = record.seq_rc
        seq_length                   = record.seq_length
        query_kmers[f"{query_id}_F"] = build_kmers(query_seq, ksize, seq_length)
        #reverse kmer list for reverse kmers to have sorted output at the end
        query_kmers[f"{query_id}_R"] = build_kmers(query_seq_rc, ksize, seq_length)
        query_map[query_id]          = i # store source key 


    return query_kmers, query_map

##############################
### Housekeeping functions ###
##############################

def create_file_handle(ouput: str):
    """create file handle for appending output through analysis"""

    #check if we need to re-write
    if os.path.isfile(ouput):
        os.remove(ouput)
    output_fh = gzip.open(ouput, "at")
        
    return output_fh

########################
### Kmer functions ###
########################


def build_kmers(sequence: str, ksize: int, seq_length: int):
    """return a list of kmer objects or a set of kmers depending if it is query or subject"""

    kmers   = set()
    n_kmers = seq_length - ksize + 1

    for pos in range(n_kmers):
        kmer = sequence[pos:pos + ksize]
        kmers.add(kmer)
    
    # return the hash set of unique k-mers
    return kmers

def find_shared_kmers(queryKmers: dict, records: list, ksize: int, query_map: dict):
    """see if the query kmers can be found in the subject kmers"""

    kmer_results = []

    for record in records:

        # find common kmers
        kmer_info = ""
        for query_id, query_kmers in queryKmers.items():
            orientation = query_id[-1:]
            query_name  = query_id[:-2]
            query_index = query_map[query_name]
            #modify for easier parsing downstream
            query_name  = query_name.split(" ")[0].replace(":",";")
            n_kmers     = record.seq_length - ksize + 1

            for pos in range(n_kmers):
                kmer = record.seq[pos:pos + ksize]
                if kmer in query_kmers:
                    kmer_info += f"{pos} " + \
                                 f"{orientation} {query_index},"

        if kmer_info != '':
            #check if paired end to keep info
            seq_name         = record.seq_name.split(" ")[0] #get rid of extra info
            paired, pair_num = record.check_if_paired_end()
            if paired:
                seq_name = f"{seq_name}_PAIRED{pair_num}"
            # [:-1] to exclude last comma
            kmer_line = f"{seq_name} [{record.seq_length}]: {kmer_info[:-1]}\n"
            kmer_results.append(kmer_line)

    return kmer_results


########################
#### Main Pipeline  ####
########################


def kmer_pipeline(subject_records: list, query_kmers: dict, query_map: dict, ksize: int, output_fh, seq_cnt: int, thread_num: int):
    """function to run the pipeline on processing_seq_cnt of seq records"""

    # keep a tracker
    matches = 0

    if thread_num == 1:
        print() #spaceing b/t loaded print
        for record in subject_records:
            print(f"Processing sequence #{seq_cnt}", end='\r')
            seq_cnt += 1
            kmer_info = find_shared_kmers(query_kmers, [record], ksize, query_map)
            if len(kmer_info) != 0:
                matches += 1
                output_fh.write(kmer_info[0])
                output_fh.flush()
    
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # split records based on thread number
            thread_jobs = [executor.submit(find_shared_kmers, query_kmers,
                                            subject_records[i::thread_num],
                                            ksize, query_map) for i in range(thread_num)]
            # get results
            for thread_job in concurrent.futures.as_completed(thread_jobs):
                results     = thread_job.result()
                results_cnt = len(results)
                if results_cnt != 0:
                    matches += results_cnt
                    for result in results:
                        output_fh.write(result)
                    output_fh.flush()

    return seq_cnt, matches

def make_source_line(query_map: dict):
    """return a line listing the sources of the kmers by index number"""
    outline = "#Source"

    for qsrc, idx in query_map.items():
        if (idx < len(query_map) - 1):
            outline = outline + ' ' + qsrc + ' ' + str(idx) + ','
        else:
            outline = outline + ' ' + qsrc + ' ' + str(idx) + '\n'

    return outline

def Kmerize(args):
    """Find shared k-mers between subject and query sequences"""

    starting_time = datetime.now().strftime("%B %d, %Y: %H:%M:%S")
    print(f"Analysis Start Time: {starting_time}")

    # get arguments
    subject_file, query_file, ksize, output, \
    limit, thread_num = check_params(args)

    if thread_num == 1:
        print("Running in Sequential Mode")
    else:
        print("Running in Multithreaded Mode")

    # load query sequences
    query_kmers, query_map = load_query_records(query_file, ksize)
    print() #spacing b/t '\r' prints

    # create the coordinates file
    output_fh = create_file_handle(output)
    command   = "# klumpy " + \
         " ".join("\"" + arg + "\"" if " " in arg else arg for arg in sys.argv[1:]) + '\n'
    output_fh.write(command)
    output_fh.write(f"# k-size: {ksize}\n")
    output_fh.write(f"# Starting time: {starting_time}\n")
    results_format = "# Sequence [Sequence Length]: " + \
                     "Position_in_Seq Orientation_in_Seq Query_Source\n"
    source_line    = make_source_line(query_map)
    output_fh.write(results_format)
    output_fh.write(source_line)

    # run pipeline
    record_cnt, seq_cnt, hits = 0, 1, 0
    
    #determine if fasta or fastq
    ftype = determine_parsing_fun(subject_file)
    if ftype == "fastq":
        hits = load_fastq_file(subject_file, limit, query_kmers,
                               query_map, ksize, output_fh, record_cnt,
                               hits, seq_cnt, False, thread_num)
    
    elif ftype == "fasta":
        #kmer_pipeline nested in loading
        hits = load_fasta_file(subject_file, limit, query_kmers, query_map,
                               ksize, output_fh, record_cnt, hits,
                               seq_cnt, False, thread_num)

    # end analysis
    print(f"\nSequences with >=1 shared {ksize}mers: {hits}")
    ending_time = datetime.now().strftime("%B %d, %Y: %H:%M:%S")
    print(f"Query Mapping Ending time: {ending_time}")
    output_fh.write(f"# Ending time: {ending_time}")
    output_fh.close()