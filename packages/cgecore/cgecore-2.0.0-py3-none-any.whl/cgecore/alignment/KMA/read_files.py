    # Created by Alfred Ferrer Florensa
"""Contains objects for reading """

from cgecore.alignment.KMA.alignment_files import Iterator_ResFile, Iterator_FragmentFile, Iterator_ConsensusFile, Iterator_AlignmentFile, Iterator_MatrixFile, Iterator_VCFFile, Iterator_MapstatFile, Iterator_SPAFile
from cgecore.sequence.SeqHit import KMAHit
from cgecore.utils.file_mixin import CGELibFileError, ResultFile, CGELibFileParseError
from cgecore.utils.format_mixin import FormatVariable
from cgecore.sequence.Feature import AlnFeature




class KMA_Result(dict):

    FILE_ITERATOR = {
            "Result": Iterator_ResFile,
            "Fragments": Iterator_FragmentFile,
            "Consensus": Iterator_ConsensusFile,
            "Alignment": Iterator_AlignmentFile,
            "Matrix": Iterator_MatrixFile,
            "Mapstat": Iterator_MapstatFile,
            "Frag_Raw": None,
            "VCF": Iterator_VCFFile,
            "Sparse": Iterator_SPAFile
            }

    def __init__(self, filename, aln_files, output_path=None):

        if output_path is None:
            file_path = filename
        else:
            file_path = "%s/%s" % (output_path, filename)

        files = FormatVariable.is_a_list(aln_files)

        KMA_Result.check_Sparse(files)
        self.files = KMA_Result.force_file_last(files=files)

        for file in self.files:
            result_file = KMA_Result.init_file(file_path=file_path,
                                               aln_file=file)
            self[result_file] = None

    def _get_entry(self, file_type):
        for file_result in self:
            if file_result.type == file_type:
                iterator_resultfile = dict.__getitem__(self, file_result)
                try:
                    entry = next(iterator_resultfile)
                except CGELibFileParseError:
                    entry = None
                return entry
        raise KeyError("The file type %s do not exist in the KMA_result." % (
                       file_type))

    def __getitem__(self, file_type):
        for file_result in self:
            if file_result.type == file_type:
                return file_result
        raise KeyError("The file type %s do not exist in the KMA_result." % (
                       file_type))

    @staticmethod
    def check_Sparse(aln_files):
        if "Sparse" in aln_files and aln_files.__len__() > 1:
            raise CGELibFileError("File 'Sparse' is a unique result file. It "
                                  "cannot be read with other files")
    @staticmethod
    def force_file_last(files, file="VCF"):
        if "VCF" in files:
            files.sort(key='string2'.__eq__)
        return files

    @staticmethod
    def init_file(file_path, aln_file):
        if aln_file in KMA_Result.FILE_ITERATOR:
            iterator_result = KMA_Result.FILE_ITERATOR[aln_file]
        else:
            raise KeyError("The alignment file %s is not part of the KMA"
                           "alignment files." % aln_file)
        result_file = ResultFile(type=aln_file, file_path=file_path,
                                 extension=iterator_result.EXTENSION,
                                 read_method=iterator_result)
        return result_file

    def start_iterators(self):
        for key, value in self.items():
            self.__setitem__(key, key.read())

    def iterate_hits(self):
        iter_true = True
        vcf_entry = None
        # Activate iterators
        self.start_iterators()
        while iter_true:
            list_hits = []
            for kma_file in self.files:
                if kma_file == "VCF" and len(self.files) > 1:
                    if vcf_entry is None:
                        entry = self._get_entry(kma_file)
                        if entry is None:
                            return
                    else:
                        entry = vcf_entry
                    if entry["templateID"] == hit["templateID"]:
                        transl_entry = AlnFeature.translate_entry(
                                    file_iterator=self[kma_file].read_method,
                                    entry=entry)
                        file_instance = self[kma_file]
                        hit = KMAHit(orig_file=file_instance,
                                     data=transl_entry)
                        list_hits.append(hit)
                    else:
                        entry = vcf_entry
                else:
                    entry = self._get_entry(kma_file)
                    if entry is None:
                        return
                    else:
                        transl_entry = AlnFeature.translate_entry(
                                        file_iterator=self[kma_file].read_method,
                                        entry=entry)
                        file_instance = self[kma_file]
                        hit = KMAHit(orig_file=file_instance, data=transl_entry)
                        list_hits.append(hit)
            merged_hit = KMAHit.merge_hits(list_hits)
            yield merged_hit
