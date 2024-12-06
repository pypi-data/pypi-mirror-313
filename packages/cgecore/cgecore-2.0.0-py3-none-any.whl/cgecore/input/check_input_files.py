

import gzip
from Bio import SeqIO
import os
import sys
from collections import defaultdict

class CheckFiles:
    def __init__(self, args) -> None:
        """Checks the input filepaths which are provided in a list for both fasta and fastq files. THen it puts them in the format set(tuple).
        The fastq files are already paired based on the read IDs.

        Args:
            args (_type_): _description_
        """
        self.fastq_out_file = self.check_fastq(args.inputfastq)
        self.fasta_out_file = self.check_fasta(args.inputfasta)
        self.all_files = self.fastq_out_file.union(self.fasta_out_file)
    
    @staticmethod
    def is_fasta(filename):
        """Check if a file is a FASTA file by attempting to parse it with Biopython."""
        try:
            if filename.endswith('.gz'):
                with gzip.open(filename, 'rt') as file:
                    # Attempt to parse the file with SeqIO
                    for record in SeqIO.parse(file, "fasta"):
                        return True
            else:
                with open(filename, 'r') as file:
                    # Attempt to parse the file with SeqIO
                    for record in SeqIO.parse(file, "fasta"):
                        return True
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return False
        return False
    
    @staticmethod
    def is_fastq(filename):
        """Check if a file is a FASTQ file by attempting to parse it with Biopython."""
        try:
            if filename.endswith('.gz'):
                with gzip.open(filename, 'rt') as file:
                    # Attempt to parse the file with SeqIO
                    for record in SeqIO.parse(file, "fastq"):
                        return True
            else:
                with open(filename, 'r') as file:
                    # Attempt to parse the file with SeqIO
                    for record in SeqIO.parse(file, "fastq"):
                        return True
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return False
        return False
    
    @staticmethod
    def read_ids_from_fastq(filename, num_reads=100):
        """Extract a set of read IDs from the first few reads of a FASTQ file."""
        read_ids = set()
        try:
            if filename.endswith('.gz'):
                with gzip.open(filename, 'rt') as file:
                    for i, record in enumerate(SeqIO.parse(file, "fastq")):
                        read_id = record.id.split(' ')[0]
                        read_ids.add(read_id)
                        if i >= num_reads - 1:
                            break
            else:
                with open(filename, 'r') as file:
                    for i, record in enumerate(SeqIO.parse(file, "fastq")):
                        read_id = record.id.split(' ')[0]
                        read_ids.add(read_id)
                        if i >= num_reads - 1:
                            break
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
        return read_ids
    

    
    def identify_paired_files(self, file_list, num_reads=100) :
        """Identify and group paired-end FASTQ files based on read IDs."""
        read_id_to_files = defaultdict(list)
        
        for file in file_list:
            if os.path.isfile(file):
                read_ids = self.read_ids_from_fastq(file, num_reads)
                for read_id in read_ids:
                    read_id_to_files[read_id].append(file)
            else:
                print(f"{file} does not exist.")
        
        # Group files by matching read IDs
        paired_files = set()
        unpaired_files = set()
        processed_files = set()
        
        for files in read_id_to_files.values(): # read ids which appear in two files will have those files as values
            if len(files) == 2:
                paired_files.add(tuple(sorted(files)))
            else:
                for file in files:
                    if file not in processed_files:
                        unpaired_files.add((file,))
            for file in files:
                processed_files.add(file)
        
        return paired_files.union(unpaired_files)
    
    def check_fastq(self, fastq_files:list):
        for file in fastq_files:
            if os.path.isfile(file):
                pass
            else:
                raise FileNotFoundError(f"File {file} not found.")
            if self.is_fastq(file):
                pass
            else:
                print(f"File {file} is not a valid FASTQ file.")
                return False
            
        paired_files = self.identify_paired_files(fastq_files)
        return paired_files
            
         
    def check_fasta(self, fasta_files:list):
        fasta_files = set()
        for file in fasta_files:
            if len(set(fasta_files)) == len(fasta_files):
                pass
            else:
                raise ValueError("Duplicate FASTA files found.")
            fasta_files.add((file))
        return fasta_files

