# Created by Alfred Ferrer Florensa
"""Contains utils"""
import os
import json
import numpy as np
import pandas as pd


class FormatFile:

    @staticmethod
    def is_gzipped(file_path):
        ''' Returns True if file is gzipped and False otherwise.
            The result is inferred from the first two bits in the file read
            from the input path.
            On unix systems this should be: 1f 8b
            Theoretically there could be exceptions to this test but it is
            unlikely and impossible if the input files are otherwise expected
            to be encoded in utf-8.
        '''
        with open(file_path, mode='rb') as fh:
            bit_start = fh.read(2)
        if(bit_start == b'\x1f\x8b'):
            return True
        else:
            return False

    @staticmethod
    def get_input_format(input_files):
        """
        Takes all input files and checks their first character to assess
        the file format. Returns one of the following strings; fasta, fastq,
        other or mixed. fasta and fastq indicates that all input files are
        of the same format, either fasta or fastq. other indiates that all
        files are not fasta nor fastq files. mixed indicates that the inputfiles
        are a mix of different file formats.
        """

        # Open all input files and get the first character
        file_format = []
        invalid_files = []
        for infile in input_files:
            if is_gzipped(infile):
                f = gzip.open(infile, "rb")
                fst_char = f.read(1)
            else:
                f = open(infile, "rb")
                fst_char = f.read(1)
            f.close()
            # Assess the first character
            if fst_char == b"@":
                file_format.append("fastq")
            elif fst_char == b">":
                file_format.append("fasta")
            else:
                invalid_files.append("other")
        if len(set(file_format)) != 1:
            return "mixed"
        return ",".join(set(file_format))



class FormatVariable:

    @staticmethod
    def is_list_or_strings(lst):
        if isinstance(lst, str):
            return [lst]
        elif(bool(lst) and isinstance(lst, list)
                and all(isinstance(elem, str) for elem in lst)):
            return lst
        else:
            raise TypeError("The datasets variable have to be a string or a"
                            "list of strings")

    @staticmethod
    def is_a_list(lst):
        if isinstance(lst, list):
            list_lst = lst
        else:
            try:
                list_lst = list(lst)
            except ValueError:
                raise ValueError("Could not convert string to float: %s" % lst)
        return list_lst
