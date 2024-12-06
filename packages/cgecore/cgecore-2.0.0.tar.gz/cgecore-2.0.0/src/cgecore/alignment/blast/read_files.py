# Created by Alfred Ferrer Florensa
"""Contains objects for reading """

import os
import sys
import gzip
import signal
import pandas as pd
from cgecore.utils.file_mixin import _File, ResultFile, CGELibFileParseError
from cgecore.alignment.blast.alignment_files import Iterator_XMLFile, Iterator_BlastSepFile
from cgecore.sequence.SeqHit import BlastnHit
from cgecore.sequence.Feature import AlnFeature


class BLASTN_Result(dict):

    FILE_ITERATOR = {
            "XML": Iterator_XMLFile,
            "TSV": Iterator_BlastSepFile,
            "CSV": Iterator_BlastSepFile,
            "TSV_extra": Iterator_BlastSepFile
    }

    ITERATOR_OPTIONS = {
            "XML": None,
            "TSV": {"separator": "tab",
                    "comment_lines": False},
            "CSV": {"separator": "comma",
                    "comment_lines": False},
            "TSV_extra": {"separator": "tab",
                          "comment_lines": True}
    }


    def __init__(self, filename, aln_file, output_path=None, extension=None,
                 headers=None):
        if output_path is None:
            out_prefix = ""
        else:
            out_prefix = output_path + "/"
        if extension is not None:
            file_path = out_prefix + filename + extension
        else:
            file_path = out_prefix + filename

        if not isinstance(aln_file, str):
            raise TypeError("The name of the file has to be a string")

        if not os.path.isfile(file_path):
            raise OSError("The file %s do not exists." % file_path)

        self.files = aln_file
        result_file= BLASTN_Result.init_file(file_path=file_path,
                                             aln_file=aln_file,
                                             header=headers)
        self[result_file] = None


    @staticmethod
    def init_file(file_path, aln_file, header=None):
        if aln_file in BLASTN_Result.FILE_ITERATOR:
            iterator_result = BLASTN_Result.FILE_ITERATOR[aln_file]
            options_read = BLASTN_Result.ITERATOR_OPTIONS[aln_file]
        else:
            raise KeyError("""The alignment file %s is not part of the BLASTN
                              alignment files.""" % aln_file)

        result_file = ResultFile(type=aln_file, file_path=file_path,
                                 read_method=iterator_result)
        if header is not None:
            if aln_file == "XML":
                raise ValueError("No header can be defined when using an XML"
                                 " file")
            else:
                result_file.options_read["header"] = header
        if options_read is not None:
            result_file.options_read["separator"] = options_read["separator"]
            result_file.options_read["comment_lines"] = options_read["comment_lines"]

        return result_file

    def _get_entry(self, file_type):
        for file_result in self:
            if file_result.type == file_type:
                iterator_resultfile = dict.__getitem__(self, file_result)
                try:
                    entry = next(iterator_resultfile)
                except CGELibFileParseError:
                    entry = None
                return entry
        raise KeyError("The file type %s do not exist in the BLASTN_result." % (
                       file_type))

    def start_iterators(self):
        for key, value in self.items():
            self.__setitem__(key, key.read())

    def __getitem__(self, file_type):
        for file_result in self:
            if file_result.type == file_type:
                return file_result
        raise KeyError("The file type %s do not exist in the BLASTN_result." % (
                       file_type))

    def iterate_hits(self):
        iter_true = True
        self.start_iterators()
        while iter_true:
            entry = self._get_entry(self.files)
            if entry is None:
                return 
            file_instance = self[self.files]
            try:
                empty_var = entry.pop("empty")
            except KeyError:
                empty_var = False
            transl_entry = AlnFeature.translate_entry(
                                file_iterator=file_instance.read_method,
                                entry=entry)
            hit = BlastnHit(orig_file=file_instance, empty=empty_var,
                            data=transl_entry)
            yield hit
