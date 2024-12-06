# Created by Alfred Ferrer Florensa
"""Contains objects to contain HIT"""

import os
import sys
import json
import pandas as pd
from cgecore.output.result import Result


class CGEFeatureValueError(ValueError):
    """ Error related to a ValueError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEFeatureValueError, self).__init__(message, *args)


class CGEFeatureFormatError(TypeError):
    """ Error related to a TypeError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEFeatureFormatError, self).__init__(message, *args)


class CGEFeatureKeyError(KeyError):
    """ Error related to a KeyError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEFeatureKeyError, self).__init__(message, *args)


class AlnFeature:

    @staticmethod
    def translate_entry(file_iterator, entry):
        dictionary = file_iterator.STD_header
        file_name = file_iterator.__name__.split("_")[1]
        new_entry = {}
        for k in entry:
            if k in dictionary:
                new_entry[dictionary[k]] = entry[k]
            else:
                provisional_key = "{}_{}_undescribed".format(k, file_name)
                new_entry[provisional_key] = entry[k]
        return new_entry

    @staticmethod
    def FeatureDF_to_dict(feature_DF, aln_hit_key, resultfile):
        feature = {}
        for index, row in feature_DF.iterrows():
            feature_entry = {}
            if resultfile == "Matrix":
                feature_entry["type"] = "matrix_position"
                feature_entry["position"] = index
                feature_entry["key"] = "{}_Pos{}".format(aln_hit_key, index)
            elif resultfile == "Fragments":
                feature_entry["type"] = "fragment_aligned"
                feature_entry["key"] = "{}_Frag{}".format(aln_hit_key, index)
            elif resultfile == "VCF":
                feature_entry["type"] = "point_variation"
                feature_entry["position"] = index
                feature_entry["key"] = "{}_Variation{}".format(aln_hit_key,
                                                               index)
            feature_entry.update(row.to_dict())
            feature.update({feature_entry["key"]: feature_entry})
        return feature

    @staticmethod
    def KMAMatrix_to_std(mat_DF, aln_hit_key):
        for index, row in mat_DF.iterrows():
            matrix_entry = {}
            matrix_entry["type"] = "matrix_position"
            matrix_entry["position"] = index
            matrix_entry["key"] = "{}_Pos{}".format(aln_hit_key, index)
            matrix_entry["ref_nucleotide"] = row["Nucleotide"]
            matrix_entry["A_nucleotide"] = row["A"]
            matrix_entry["G_nucleotide"] = row["G"]
            matrix_entry["T_nucleotide"] = row["T"]
            matrix_entry["C_nucleotide"] = row["C"]
            matrix_entry["N_nucleotide"] = row["N"]
            matrix_entry["null_nucleotide"] = row["-"]
            yield matrix_entry

    @staticmethod
    def KMAFrag_to_std(frag_DF):
        for index, row in frag_DF.iterrows():
            matrix_entry = {}
            matrix_entry["type"] = "fragment_aligned"
            matrix_entry["key"] = "{}_Frag{}".format(aln_hit_key, index)
            matrix_entry["query_seq"] = row["query_seq"]
            matrix_entry["equal_mapped_templ"] = row["eq_mapped"]
            matrix_entry["alignment_score"] = row["aln_score"]
            matrix_entry["start_aln"] = row["start_aln"]
            matrix_entry["end_aln"] = row["end_aln"]
            matrix_entry["template_name"] = row["template"]
            matrix_entry["query_name"] = row["query_name"]
            if "cut_start" in row and "cut_end" in row:
                matrix_entry["cut_start"] = row["cut_1"]
                matrix_entry["cut_end"] = row["cut_2"]
            yield matrix_entry

    @staticmethod
    def KMAVCF_to_std(vcf_DF, aln_hit_key, hit_file):
        "CHROM  POS ID REF ALT QUAL FILTER  INFO  FORMAT         fosfomycin"
        for index, row in vcf_DF.iterrows():
            matrix_entry = {}
            matrix_entry["type"] = "point_variation"
            matrix_entry["position"] = index
            matrix_entry["key"] = "{}_Variation{}".format(aln_hit_key, index)
            matrix_entry["id"] = row["ID"]
            matrix_entry["reference_base"] = row["REF"]
            matrix_entry["alternative_base"] = row["ALT"]
            matrix_entry["quality"] = row["QUAL"]
            matrix_entry["filter"] = row["FILTER"]
            matrix_entry["information"] = row["INFO"]
            matrix_entry["format"] = row[str(hit_file)]
            yield matrix_entry
