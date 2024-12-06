# Created by Alfred Ferrer Florensa
"""Contains objects to contain HIT"""
import os
import json
from cgecore.utils.file_mixin import CGELibFileError
from cgecore.output.result import Result
from cgecore.utils.file_mixin import ResultFile
from cgecore.utils.savers_mixin import StringCreator
from cgecore.sequence.Feature import CGEFeatureValueError, CGEFeatureFormatError, CGEFeatureKeyError, AlnFeature


class CGEHitTypeError(TypeError):
    """ Error related to a ValueError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEHitTypeError, self).__init__(message, *args)


class CGEHitValueError(ValueError):
    """ Error related to a ValueError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEHitValueError, self).__init__(message, *args)


class CGEHitKeyError(KeyError):
    """ Error related to a ValueError of the value of the feature
    """

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGEHitKeyError, self).__init__(message, *args)


class AlnHit(dict):

    beone_json_path = Result.beone_json_path

    def __init__(self, software=None, empty=False, data=None,
                 fmt_file=beone_json_path, orig_file=None):

        """
            Root for all submodule of alignment
            Input:
                software: Software that has created the alignment
                file: File object from which the data has been extracted
                empty: If the query did hit on a template or did not
                data: Dictionary containing information about a single hit from
                      aligner

            Method creates a hit dict as defined in the BeOne template
            https://bitbucket.org/genomicepidemiology/cgelib/src/master/src/
            cgelib/output/templates_json/beone/
            from res.
        """
        self.software = software

        with open(fmt_file, "r") as fh:
            json_defs = json.load(fh)
            self.feature_defs = json_defs["aln_hit"]

        self.resultfiles = []
        self.file_type = []
        self.file_paths = []

        self["type"] = "aln_hit"

        if isinstance(orig_file, ResultFile):
            self.add_resultfile(orig_file)
        elif orig_file is None:
            self["template_file"]=None
        else:
            raise TypeError("The origin file cannot be %s " % (orig_file))

        self["templateID"] = None


        if data is not None:
            self.add_features(data)
        else:
            pass

        if isinstance(empty, bool):
            self.empty = empty
        else:
            raise TypeError("Empty variable has to be a boolean")


    def __str__(self):
        if self.software is None:
            aln_str = ""
        else:
            aln_str = self.software.title()
        if self.empty:
            string_hit = "No Hit by %s on %s" % (self["queryID"],
                                                 self["templateID"])
        else:
            if self["templateID"] is not None:
                string_hit = "%sHit on %s(\n" % (aln_str, self["templateID"])
                for key, value in self.items():
                    string_hit += "\t%s: %s,\n" % (key, value)
                string_hit = string_hit[:-2]
                string_hit += ")"
            elif self["queryID"] is not None:
                string_hit = "No Hit by %s" % self["queryID"]
            else:
                string_hit = "No Hit"
        return string_hit

    def __repr__(self):
        if self.software is None:
            aln_str = ""
        else:
            aln_str = self.software.title()
        if self["templateID"] is not None:
            string_hit = "%sHit on %s (" % (aln_str, self["templateID"])
            for key, value in self.items():
                string_hit += "%r, " % (value)
            string_hit = string_hit[:-1]
            string_hit += ")"
        else:
            string_hit = "No hit"
        return string_hit

    def add_features(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                self[key] = value
        else:
            raise CGEFeatureFormatError("Only an a dictionary"
                                        " of features with their values can be "
                                        "incorporated")

    def __getitem__(self, y):
        if y in self:
            return super(AlnHit, self).__getitem__(y)
        else:
            raise CGEHitKeyError("The feature %s has not been set for this hit."
                                  % (y))


    def __setitem__(self, i, y):

        if i in self and self[i] is not None:
            if y == self[i]:
                pass
            else:
                raise CGEFeatureValueError("Feature %s has been already "
                                           "attributed to the AlnHit with the "
                                           "value %s and is trying to be "
                                           "changed by the value %s." % (
                                            i, self[i], y))
        else:
            super(AlnHit, self).__setitem__(i, y)

    @staticmethod
    def dfs_to_dict(hit):
        for aln_hit in hit.file_type:
            if aln_hit == "Matrix":
                feature_df = hit.pop("matrix")
                feature_dict = AlnFeature.FeatureDF_to_dict(
                                feature_DF=feature_df, aln_hit_key=hit["key"],
                                resultfile=aln_hit)
                hit.update({"matrix_position":feature_dict})
            elif aln_hit == "Fragments":
                feature_df = hit.pop("reads_aligned")
                feature_dict = AlnFeature.FeatureDF_to_dict(
                                feature_DF=feature_df, aln_hit_key=hit["key"],
                                resultfile=aln_hit)
                hit.update({"fragment_aligned":feature_dict})
            elif aln_hit == "VCF":
                feature_df = hit.pop("point_variations")
                feature_dict = AlnFeature.FeatureDF_to_dict(
                                feature_DF=feature_df, aln_hit_key=hit["key"],
                                resultfile=aln_hit)
                hit.update({"point_variations":feature_dict})
        return hit

    @staticmethod
    def get_run_key(software_execs, hit):
        try:
            template_file = hit["template_file"]
        except KeyError:
            template_file = None
        if template_file is None:
            key_exec = None
        else:
            key_exec = None
            for k in software_execs:
                if k.endswith(template_file):
                    if key_exec is None:
                        key_exec = k
                    else:
                        raise ValueError("The run_key has not been able to set"
                                         " because several run keys coincide")
        return key_exec



    @staticmethod
    def get_rnd_unique_hit_key(hit_key, hit_collection,
                                minimum_hit_key, delimiter):
        """
            Input:
                hit_key: None-unique key
                hit_collection: Result object created by the cgelib package.
                minimum_key: Key prefix
                delimiter: String used as delimiter inside the returned key.
            Output:
                hit_key: Unique key (string)

            If hit_key is found in hit_collection. Creates a unique key by
            appending a random string ton minimum_hit_key.
        """
        while(hit_key in hit_collection):
            rnd_str = StringCreator.random_string(str_len=4)
            hit_key = ("{key}{deli}{rnd}"
                        .format(key=minimum_hit_key, deli=delimiter,
                                rnd=rnd_str))
        return hit_key


    def _get_unique_hit_key(self, hit_collection, delimiter=";;"):
        """
            Input:
                hit_collection: Result object created by the cgelib package.
                delimiter: String used as delimiter inside the returned key.
            Output:
                key: Unique key for hit

            Creates a unique key for Hit instance. Key format depends on
            database.
        """
        if self.empty:
            if self["template_file"] is not None:
                hit_key = "NoHit{deli}{query}{deli}on{deli}{template}".format(
                        deli=delimiter, query=self["queryID"],
                        template=self["template_file"])
            else:
                hit_key = "NoHit{deli}{query}".format(deli=delimiter,
                                                query=self["queryID"])
        else:
            if self["template_file"] is not None:
                hit_key = "{template}{deli}{templatefile}".format(
                        template=self["templateID"], deli=delimiter,
                        templatefile=self["template_file"])
            else:
                hit_key = "{template}".format(
                        template=self["templateID"])
        minimum_key = hit_key
        if hit_key in hit_collection:
            hit_key = AlnHit.get_rnd_unique_hit_key(
                        hit_key, hit_collection, minimum_key, delimiter)
        self["key"] = hit_key



class BlastnHit(AlnHit):
    """Object that is a hit on a database from BLAST"""

    def __init__(self, software="blast", data=None, empty=False,
                 orig_file=None):


        super().__init__(software=software, empty=empty, data=data,
                         orig_file=orig_file)

    def add_resultfile(self, resultfile):

        if isinstance(resultfile, list):
            raise CGEFeatureFormatError("Hit from blast cannot provide from"
                                        " different files")
        if(len(self.resultfiles) > 0 or len(self.file_paths) > 0 or
            len(self.file_type) > 0):
            raise CGEFeatureFormatError("This hit has already data from "
                                        "another file")
        else:
            self.resultfiles.append(resultfile)
            self.file_paths.append(resultfile.file_path)
            self.file_type.append(resultfile.type)

        try:
            self["template_file"] = resultfile.name
        except CGEFeatureValueError:
            raise CGELibFileError("When mixing hits from different resultfiles"
                                  ", these should come from the same alignment"
                                  ". The result files that are trying to be "
                                  "mixed (%s and %s) come from different "
                                  "alignments when adding the file %s." % (
                                  self["template_file"], result_file.name,
                                  result_file.type))


class KMAHit(AlnHit):
    """Object that is a hit on a database from KMA"""

    def __init__(self, software="kma", data=None, empty=False,
                 orig_file=None):


        super().__init__(software=software, empty=empty, data=data,
                         orig_file=orig_file)


    def add_hit(self, hit):
        hit_merged = KMAHit.merge_hits([self, hit])
        self.clear()
        self.file_type = hit_merged.file_type
        self.update(hit_merged)

    def add_resultfile(self, resultfile):

        if not isinstance(resultfile, list):
            resultfile_lst = [resultfile]
        else:
            resultfile_lst = resultfile

        for result_file in resultfile_lst:
            if result_file in self.resultfiles:
                raise CGELibFileError("The hits trying to be merged should "
                                      "come from different result files. The "
                                      "file %s has been already used for "
                                      "building this hit." % (result_file))
            self.resultfiles.append(result_file)
            self.file_paths.append(result_file.file_path)
            self.file_type.append(result_file.type)


            try:
                self["template_file"] = result_file.name
            except CGEFeatureValueError:
                raise CGELibFileError("When mixing hits from different resultfiles"
                                  ", these should come from the same alignment"
                                  ". The result files that are trying to be "
                                  "mixed (%s and %s) come from different "
                                  "alignments when adding the file %s." % (
                                  self["template_file"], result_file.name,
                                  result_file.type))


    @staticmethod
    def merge_hits(list_hits):
        merged_kmahit = list_hits.pop()
        while len(list_hits) > 0:
            hit = list_hits.pop()
            merged_kmahit.add_resultfile(hit.resultfiles)
            # Add data if templateID is same
            if("templateID" not in hit):
                raise CGEHitValueError(("The hit trying to be merged to the \
                                        existing hit is not defined by the \
                                        templateID"))
            elif(merged_kmahit["templateID"] is not None
                and str(merged_kmahit["templateID"]).rstrip() != str(hit["templateID"]).rstrip()):
                raise CGEHitValueError(("The two hits trying to merge do not \
                                         come from the same template (%r and \
                                         %r)" % (
                                         merged_kmahit["templateID"],
                                         hit["templateID"])))
            else:
                merged_kmahit.add_features(hit)
        return merged_kmahit
