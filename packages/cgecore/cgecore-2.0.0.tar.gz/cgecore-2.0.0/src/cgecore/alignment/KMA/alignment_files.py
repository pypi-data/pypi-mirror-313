# Created by Alfred Ferrer Florensa
"""Contains objects for reading alignment files"""

import gzip
import pandas as pd
from cgecore.utils.file_mixin import _Parse_File


class Iterator_ResFile(_Parse_File):
    """Create iterator for a .res file"""
    STD_header={
         "Template": "templateID",
         "Score": "conclave_score",
         "Expected": "evalue",
         "Template_length": "template_length",
         "Template_Identity": "template_identity",
         "Template_Coverage": "template_coverage",
         "Query_Identity": "query_identity",
         "Query_Coverage": "query_coverage",
         "Depth": "depth",
         "q_value": "q_value",
         "p_value": "p_value"
     }

    EXTENSION = ".res"

    def __init__(self, path):
        self.header = None

        _Parse_File.__init__(self, path)

    def __repr__(self):

        return "Iterator_ResFile(%s)" % self.path

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
            elif line.startswith("#"):
                self.header = line.replace("#",
                                           "").rstrip().replace(" ",
                                                                "").split("\t")
            else:
                line_split = line.rstrip().replace(" ", "").split("\t")
                if len(line_split) != len(self.header):
                    raise IndexError("Length of line is not equal to"
                                     " header")

                hit = Iterator_ResFile.format_entry(self.header, line_split)
                entry_line = False
        return hit

    @staticmethod
    def format_entry(header, data):
        hit = {}
        if isinstance(data, dict):
            hit.update(data)
        elif isinstance(data, list):
            if len(data) != len(header):
                raise IndexError("Length of line (%s)is not equal to"
                                 " header (%s). Check if you have chosen "
                                 "the right separator." % (len(data),
                                                           len(header)
                                                           ))
            for n_feat in range(len(data)):
                value = data[n_feat]
                key = header[n_feat]
                hit[key] = value
        else:
            raise TypeError("Data has to be list or dictionary")
        return hit


class Iterator_MapstatFile(_Parse_File):

    STD_header = {
        "refSequence": "templateID",
        "readCount": "reads_mapped",
        "fragmentCount": "fragments_mapped",
        "mapScoreSum": "mapScoreSum",
        "refCoveredPositions": "template_coveredPos",
        "refConsensusSum": "template_consesusSum",
        "bpTotal": "bpTotal",
        "depthVariance": "depth_variance",
        "nucHighDepthVariance": "nucHigh_depth_variance",
        "depthMax": "depth_max",
        "snpSum": "snps",
        "insertSum": "insertions",
        "deletionSum": "deletions",
        "fragmentCountAln": "fragments_mapped_align",
        "readCountAln": "reads_mapped_align"
        }

    EXTENSION = ".mapstat"

    def __init__(self, path):
        self.header = None
        _Parse_File.__init__(self, path)

    def get_info(self):
        info = {}
        if not self.file.closed:
            file_open = open(self.path, 'r')
        else:
            file_open = self.file
        for line in file_open:
            if line.startswith("##"):
                split_line = line.replace("## ", "").rstrip().split("\t")
                if len(split_line) != 2:
                    raise TypeError("The information line of Mapstat does"
                                    " not follow the normal format (%)" %
                                    (line))
                info[split_line[0]] = split_line[1]
            else:
                break
        return info

    def __repr__(self):

        return "Iterator_MapstatFile(%s)" % self.path

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
            elif line.startswith("## "):
                pass
            elif line.startswith("#"):
                self.header = line.replace("#",
                                           "").rstrip().replace(" ",
                                                                "").split("\t")
            else:
                line_split = line.rstrip().replace(" ", "").split("\t")
                if len(line_split) != len(self.header):
                    raise IndexError("Length of line is not equal to"
                                     " header")
                hit = Iterator_MapstatFile.format_entry(self, line_split)
                entry_line = False
        return hit

    @staticmethod
    def format_entry(self, data):

        hit = {}
        if isinstance(data, dict):
            hit.update(data)
        elif isinstance(data, list):
            if len(data) != len(self.header):
                raise IndexError("Length of line (%s)is not equal to"
                                 " header (%s). Check if you have chosen "
                                 "the right separator." % (len(data),
                                                           len(self.header)
                                                           ))
            for n_feat in range(len(data)):
                value = data[n_feat]
                key = self.header[n_feat]
                hit[key] = value
        else:
            raise TypeError("Data has to be list or dictionary")
        return hit


class Iterator_MatrixFile(_Parse_File):
    """Create iterator for a .matrix file"""

    STD_header={
        "templateID": "templateID",
        "matrix": "matrix"}

    EXTENSION = ".mat.gz"

    def __init__(self, path, is_gzip=True):
        self.header = ["ref_nucl", "A_nucl", "C_nucl", "G_nucl", "T_nucl",
                       "N_nucl", "null_nucl"]

        _Parse_File.__init__(self, path, is_gzip)

        self.gene = None
        self.template_df = []

    def __repr__(self):

        return "Iterator_MatrixFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        while entry_line:
            line = self.parse_line()
            if line.startswith("#"):
                if self.gene is not None:
                    gene = self.gene
                    entry = pd.DataFrame(self.template_df, columns=self.header)
                    entry_line = False
                self.gene = line.replace("#", "").rstrip()
                self.template_df = []
            elif line == "\n":
                continue
            elif line == "":
                if self.gene is not None:
                    gene = self.gene
                    entry = pd.DataFrame(self.template_df, columns=self.header)
                    entry_line = False
                else:
                    entry = None
                _Parse_File.close(self)
            else:
                line_split = line.rstrip().split("\t")
                if len(line_split) != len(self.header):
                    raise IndexError("Length of line is not equal to"
                                     " header")
                self.template_df.append(line_split)
        hit = Iterator_MatrixFile.format_entry(gene, entry)
        return hit

    @staticmethod
    def format_entry(gene, data):
        hit = {}
        hit["templateID"] = gene
        hit["matrix"] = data
        return hit


class Iterator_AlignmentFile(_Parse_File):
    """Create iterator for a .aln file"""

    STD_header={
            "templateID": "templateID",
            "query_seq": "query_aln",
            "template_seq": "template_aln",
            "alignment_seq": "aln_scheme"
        }
    EXTENSION = ".aln"

    def __init__(self, path, is_gzip=False):

        _Parse_File.__init__(self, path, is_gzip)
        self.gene = None
        self.alignment = None

    def __repr__(self):

        return "Iterator_AlignmentFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        alignment = None
        while entry_line:
            line = self.parse_line()
            if line.startswith("# "):
                if self.gene is not None:
                    gene = self.gene
                    alignment = self.alignment
                    entry_line = False
                self.gene = line.replace("# ", "").rstrip()
                self.alignment = {"template_seq": [], "alignment_seq": [],
                                  "query_seq": []}
            elif line.startswith("template:"):
                temp_seq = str(line.split("\t")[-1].rstrip())
                self.alignment["template_seq"].append(temp_seq)
            elif line.startswith("query:"):
                temp_seq = str(line.split("\t")[-1].rstrip())
                self.alignment["query_seq"].append(temp_seq)
            elif line == "\n":
                continue
            elif line == "":
                # This might be useless
                if self.gene is not None:
                    entry = self.alignment
                    entry_line = False
                    break
                else:
                    entry = None
            else:
                aln_seq = str(line.split("\t")[-1].rstrip())
                self.alignment["alignment_seq"].append(aln_seq)
        if alignment is None:
            alignment = self.alignment
            gene = self.gene
            _Parse_File.close(self)
        hit = Iterator_AlignmentFile.format_entry(self, alignment, gene)
        return hit

    @staticmethod
    def format_entry(self, alignment, template):
        hit = {}
        hit["templateID"] = template
        hit["query_seq"] = "".join(alignment["query_seq"])
        hit["template_seq"] = "".join(alignment["template_seq"])
        hit["alignment_seq"] = "".join(alignment["alignment_seq"])
        return hit


class Iterator_ConsensusFile(_Parse_File):
    """Create iterator for a .fsa file"""

    STD_header={
     "templateID": "templateID",
     "sequence": "query_aln"
     }

    EXTENSION = ".fsa"

    def __init__(self, path):
        self.gene = None
        self.sequence = None

        _Parse_File.__init__(self, path)

    def __repr__(self):

        return "Iterator_ConsensusFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        entry = None
        while entry_line:
            line = self.parse_line()
            if line.startswith(">"):
                if self.gene is not None:
                    gene = self.gene
                    entry = "".join(self.sequence)
                    entry_line = False
                self.gene = line.replace(">", "").rstrip()
                self.sequence = []
            elif line == "\n":
                continue
            elif line == "":
                if self.gene is not None:
                    gene = self.gene
                    entry = "".join(self.sequence)
                    self.sequence = []
                    entry_line = False
                else:
                    entry = None    #BUG?
                _Parse_File.close(self)
            else:
                self.sequence.append(line.rstrip())
        if entry is None:
            entry = "".join(self.sequence)
            gene = self.gene
        hit = Iterator_ConsensusFile.format_entry(self, entry, gene)
        return hit

    @staticmethod
    def format_entry(self, sequence, template):
        hit = {}
        hit["templateID"] = template
        hit["query_aln"] = sequence
        return hit


class Iterator_VCFFile(_Parse_File):

    STD_header={
         "templateID": "templateID",
         "vcf_data": "point_variations"
         }
    EXTENSION = ".vcf.gz"

    def __init__(self, path, is_gzip=True):

        self.gene = None
        self.header = None
        self.template_df = []


        _Parse_File.__init__(self, path, is_gzip)

    def __repr__(self):

        return "Iterator_VCFFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        while entry_line:
            line = self.parse_line()
            if line.startswith("##"):
                pass
            elif line.startswith("#"):
                self.define_header(header_line=line)
            elif line == "":
                if self.gene is not None:
                    gene = self.gene
                    entry = pd.DataFrame(self.template_df, columns=self.header)
                    entry_line = False
                else:
                    entry = None
                _Parse_File.close(self)
            else:
                line_split = line.rstrip().split("\t")
                if self.gene == line_split[0]:
                    if len(line_split) != len(self.header):
                        raise IndexError("Length of line is not equal to"
                                         " header")
                    self.template_df.append(line_split)
                else:
                    if self.gene is not None:
                        gene = self.gene
                        entry = pd.DataFrame(self.template_df, columns=self.header)
                        entry_line = False
                    self.gene = line_split[0]
                    self.template_df = []
        hit = Iterator_VCFFile.format_entry(entry, gene)
        return hit

    def define_header(self, header_line):
        header_split = header_line.replace("#", "").rstrip().split("\t")
        last_col = header_split[-1]
        if len(header_split) != 10:
            raise IndexError("The iterator needs a vcf file with ten columns")
        else:
            header = ["templateID", "position", "id", "ref_base", "alt_base",
                      "quality", "filter", "info", "format", last_col]
        self.header = header


    def get_info(self):
        info = {}
        with gzip.open(self.path, 'rt') as file_open:
            for line in file_open:
                if line.startswith("##"):
                    line_split = line.replace("##", "").rstrip().split("=")
                    if len(line_split) == 2:
                        info[line_split[0]] = line_split[1]
                    else:
                        if line_split[0] not in info:
                            info[line_split[0]] = {}
                        new_value = []
                        for i in range(len(line_split[1:])-1):
                            new_element = line_split[1:][i].replace('<',
                                                                    '').split(
                                                                    ",")
                            new_value.extend(new_element)
                        new_value.append(line_split[-1].replace('>', ''))
                        dict_value = dict(zip(new_value[::2], new_value[1::2]))
                        info[line_split[0]].update({dict_value["ID"]:
                                                    dict_value})
                else:
                    break
        return info

    @staticmethod
    def format_entry(entry, gene):
        hit = {}
        hit["templateID"] = gene
        hit["vcf_data"] = entry
        return hit


class Iterator_SPAFile(_Parse_File):
    """Create iterator for .spa file"""

    STD_header={
        "#Template": "templateID",
        "Num": "Num",
        "Score": "score",
        "Expected": "evalue",
        "Template_length": "template_length",
        "Query_Coverge": "query_coverage",
        "Template_Coverage": "template_coverage",
        "Depth": "depth",
        "tot_query_Coverage": "tot_query_coverage",
        "tot_template_Coverage": "tot_template_coverage",
        "tot_depth": "tot_depth",
        "q_value": "q_value",
        "p_value": "p_value"
    }

    EXTENSION = ".spa"

    def __init__(self, path):
        self.header = None

        _Parse_File.__init__(self, path)

    def __repr__(self):

        return "Iterator_SPAFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        while entry_line:
            line = self.parse_line()
            if line == "":
                _Parse_File.close(self)
            elif line.startswith("#"):
                self.header=Iterator_SPAFile.define_header(header_str=line)
            else:
                line_split = line.rstrip().replace(" ", "").split("\t")
                if len(line_split) != len(self.header):
                    raise IndexError("Length of line is not equal to"
                                     " header")
                hit = Iterator_SPAFile.format_entry(self.header, line_split)
                entry_line = False
        return hit

    @staticmethod
    def define_header(header_str):
        header = header_str.replace("#", "").rstrip().replace(" ", "").split("\t")
        if header != Iterator_SPAFile.STD_header:
            raise ValueError("""Header of the %s file is not equal to the header
                                expected. Please inform curator.""")
        return header

    @staticmethod
    def format_entry(header, data):
        hit = {}
        if isinstance(data, dict):
            hit.update(data)
        elif isinstance(data, list):
            if len(data) != len(header):
                raise IndexError("Length of line (%s)is not equal to"
                                 " header (%s). Check if you have chosen "
                                 "the right separator." % (len(data),
                                                           len(header)
                                                           ))
            for n_feat in range(len(data)):
                value = data[n_feat]
                key = header[n_feat]
                hit[key] = value
        else:
            raise TypeError("Data has to be list or dictionary")


class Iterator_FragmentFile(_Parse_File):
    """Create iterator for .frag file"""
    STD_header={
            "templateID": "templateID",
            "fragments": "reads_aligned"
             }
    EXTENSION = ".frag.gz"
    def __init__(self, path, gzip=True):
        self.header = None
        self.gene = None
        self.template_df = []

        _Parse_File.__init__(self, path, gzip)

    def __repr__(self):

        return "Iterator_FragmentFile(%s)" % self.path

    def __str__(self):

        return self.path

    def __iter__(self):

        return self

    def __next__(self):
        entry_line = True
        while entry_line:
            line = self.parse_line()
            if line == "":
                if self.gene is not None:
                    gene = self.gene
                    entry = pd.DataFrame(self.template_df, columns=self.header)
                    entry_line = False
                else:
                    entry = None
                _Parse_File.close(self)
            else:
                line_split = line.rstrip().split("\t")
                if self.header is None:
                    self.define_header(line_split=line_split)
                else:
                    if len(line_split) != len(self.header):
                        raise IndexError("Length of line is not equal to"
                                         " header")
                if self.gene is None:
                    self.gene = line_split[5]
                    self.template_df = []

                if self.gene == line_split[5]:
                    #row_series = pd.Series(data=line_split, index=self.header)
                    self.template_df.append(line_split)
                else:
                    gene = self.gene
                    entry = pd.DataFrame(self.template_df, columns=self.header)
                    entry_line = False
                    self.gene = line_split[5]
                    self.template_df = []
                    self.template_df.append(line_split)


        hit = Iterator_FragmentFile.format_entry(entry, gene)
        return hit

    def define_header(self, line_split):
        if len(line_split) == 7:
            self.header = ["query_seq", "eq_mapped", "aln_score", "start_aln",
                           "end_aln", "template_name", "query_name"]
        elif len(line_split) == 9:
            self.header = ["query_seq", "eq_mapped", "aln_score", "start_aln",
                           "end_aln", "template_name", "query_name", "cut1",
                           "cut2"]
        else:
            raise KeyError("Fragment file is does has not 7 or 9 columns")

    @staticmethod
    def format_entry(data, gene):
        hit = {}
        hit["templateID"] = gene
        hit["fragments"] = data
        return hit
