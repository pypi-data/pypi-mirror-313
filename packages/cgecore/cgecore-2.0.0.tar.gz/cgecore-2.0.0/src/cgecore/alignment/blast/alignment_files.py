# Created by Alfred Ferrer Florensa
"""Contains objects for reading alignment files"""

import gzip
import io
import pandas as pd
import signal
import sys
from cgecore.sequence.SeqHit import AlnHit, BlastnHit
from cgecore.utils.file_mixin import _Parse_File, CGELibFileParseError
from Bio.Blast.NCBIXML import parse as BioXMLParse

class Iterator_XMLFile(_Parse_File):

    STD_header = {
        "queryID": "queryID",
        "templateID": "templateID",
        "query": "query_aln",
        "sbjct": "template_aln",
        "pident": "query_identity",
        "sbjct_start": "template_start_aln",
        "sbjct_end": "template_end_aln",
        "expect": "evalue",
        "align_length": "aln_length",
        "qcov": "query_coverage",
        "query_start": "query_start_aln",
        "query_end": "query_end_aln",
        "bits": "bitscore",
        "score": "score",
        "num_alignments": "n_alignments",
        "match": "aln_scheme",
        "identities": "n_identity",
        "positives": "n_positives",
        "gaps": "gaps",
        "strand": "strand",
        "frame": "frame"
    }

    EXTENSION = None

    def __init__(self, path):

        _Parse_File.__init__(self, path)
        self.iterator_XML = BioXMLParse(self.file)
        self.extension = "xml"
        self.recordblast = None
        self.recordaln = None
        self.recordhsp = None
        self.queryID = None


    def __iter__(self):
        return self

    def __next__(self):
        new_line = True
        while new_line:
            if self.recordblast is None:
                recordblast = self.parse_line(file_type="xml")
                self.recordblast = iter(recordblast.__dict__["alignments"])
                self.queryID = recordblast.__dict__["query"]
            if self.recordblast:
                if self.recordaln is None:
                    try:
                        self.recordaln = next(self.recordblast)
                        self.recordhsp = iter(self.recordaln.__dict__["hsps"])
                    except StopIteration:
                        self.recordblast = None
                        self.recordhsp = None
                        self.recordblast = None
                        #new_line=False
                if self.recordhsp:
                    try:
                        hsp_data = next(self.recordhsp)
                        new_line=False
                        hit = Iterator_XMLFile.format_entry(
                                                    queryID=self.queryID,
                                                    aln_info=self.recordaln,
                                                    hsp_info=hsp_data)
                        return hit
                    except StopIteration:
                        self.recordaln = None
                        self.recordhsp = None



    @staticmethod
    def format_entry(queryID, aln_info, hsp_info):
        hit = {}
        hit["queryID"] = queryID
        aln_dict = aln_info.__dict__
        hit["gene_length"] = aln_dict["length"]
        hit["templateID"] = aln_dict["hit_def"]
        hsp_dict = hsp_info.__dict__
        hit.update(hsp_dict)
        return hit




class Iterator_BlastSepFile(_Parse_File):

    STD_header = {
        "qseqid": "queryID",
        "qgi": "queryGI",
        "qacc": "query_accuracy",
        "sseqid": "templateID",
        "sallseqid": "templateIDs",
        "sgi": "templateGI",
        "sallgi": "templateGIs",
        "sacc": "template_accuryacy",
        "sallacc": "template_accuracies",
        "qstart": "query_start",
        "qend": "query_end",
        "pident": "query_identity",
        "sstart": "template_start_aln",
        "send": "template_end_aln",
        "qseq": "query_aln",
        "sseq": "template_aln",
        "evalue": "evalue",
        "length": "aln_length",
        "qstart": "query_start_aln",
        "qend": "query_end_aln",
        "bitscore": "bitscore",
        "score": "score",
        "nident": "n_identity",
        "positive": "n_positives",
        "gapopen": "gaps_open",
        "gaps": "gaps",
        "ppos": "positives",
        "frames": "frames",
        "qframe": "query_frame",
        "sframe": "template_frame",
        "btop": "btop",
        "staxids": "template_taxids",
        "sscinames": "template_sciname",
        "scomnames": "template_comname",
        "sblastnames": "template_blastname",
        "sskingdoms": "template_superkingdom",
        "stitle": "template_title",
        "salltitles": "template_titles",
        "sstrand": "template_strand",
        "qcovs": "query_coverage_template",
        "qcovhsp": "query_coverage_hsp",
        "qcovus": "query_coverage_once",
        "mismatch": "mismatch",
        }

    EXTENSION = None

    def __init__(self, path, separator="tab", comment_lines=False,
                 header=["qseqid", "sseqid", "pident", "length", "mismatch",
                         "gapopen", "qstart", "qend", "sstart", "send",
                         "evalue", "bitscore"]):
        self.header = header
        self.software = "blastn"
        if separator == "comma":
            self.separator = ","
            self.file_type = "csv"
        elif separator == "tab":
            self.separator = "\t"
            self.file_type = "tsv"
        else:
            raise ValueError("The separator of the blast results file has to "
                             "be 'comma' or 'tab'.")

        if separator == "comma" and comment_lines:
            raise TypeError("The option of comment_lines is only available "
                            "for tab separated files")
        self.comment_lines = comment_lines

        _Parse_File.__init__(self, path)

    def __repr__(self):

        return "Iterator_TabFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        while entry_line:
            line = self.parse_line()
            if line == "":
                entry = None
                _Parse_File.close(self)
                raise CGELibFileParseError(
                    "The iterator has arrived to the end of the file")
            elif self.comment_lines and line.startswith("#"):
                line_split = line.rstrip().split(" ")
                if line_split[1] == "Query:":
                    query_entry = line_split[-1]
                elif line_split[1] == "Subject:":
                    subject_entry = line_split[-1]
                elif line_split[-1] == "found":
                    if line_split[1] == "0":
                        pass
                        #print(query_entry, line_split)
                        #entry = {"qseqid": query_entry,
                        #         "templateID": subject_entry}
                        #hit = Iterator_BlastSepFile.format_entry(
                        #                        header=self.header, data=entry)
                        #return hit
                    else:
                        hits_found = int(line_split[1])
                elif line_split[1] == "Fields:":
                    line_header = line.replace("# Fields: ", "")
                    header = line_header.split(",")
            else:
                line_split = line.rstrip().replace(" ",
                                                   "").split(self.separator)
                if len(line_split) != len(self.header):
                    raise IndexError("Length of line '%s' (%s) is not equal to"
                                     " header '%s' (%s). Check if you have "
                                     "chosen the right separator." % (
                                        line_split, len(line_split),
                                        self.header, len(self.header)))
                hit = Iterator_BlastSepFile.format_entry(
                                header=self.header,data=line_split)
                entry_line = False
        return hit

    @staticmethod
    def format_entry(header, data):
        hit = {}
        if isinstance(data, dict):
            hit.update(data)
            hit["empty"] = True
        elif isinstance(data, list):
            if len(data) != len(header):
                raise IndexError("Length of line (%s)is not equal to"
                                 " header (%s). Check if you have chosen "
                                 "the right separator." % (len(data),
                                                           len(header)
                                                           ))
            for n_feat in range(len(data)):
                hit[header[n_feat]] = data[n_feat]
            hit["empty"] = False
        else:
            raise TypeError("Data has to be list or dictionary")
        return hit



    @staticmethod
    def assign_BlastnHit(self, data, empty=False):
        hit = BlastnHit(empty=empty, file_type=self.file_type)
        if isinstance(data, dict):
            for key, value in data.items():
                key = Translate.translate_keys(key,
                                                    Iterator_BlastSepFile.Translator_Hit)
                hit[key] = value
        elif isinstance(data, list):
            if len(data) != len(self.header):
                raise IndexError("Length of line (%s)is not equal to"
                                 " header (%s). Check if you have chosen "
                                 "the right separator." % (len(data),
                                                           len(self.header)
                                                           ))
            for n_feat in range(len(data)):
                value = data[n_feat]
                key = Translate.translate_keys(self.header[n_feat],
                                                    Iterator_BlastSepFile.Translator_Hit)
                hit[key] = value
        else:
            raise TypeError("Data has to be list or dictionary")

        return hit
