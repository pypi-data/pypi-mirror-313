# Created by Alfred Ferrer Florensa
"""Contains objects for reading """

#from cgelib.alignment.blast.read_files import BLASTN_Result
from cgecore.alignment.KMA.read_files import KMA_Result
from cgecore.alignment.blast.read_files import BLASTN_Result
from cgecore.utils.savers_mixin import SaveJson
from cgecore.output.result import Result
from cgecore.sequence.SeqHit import AlnHit, CGEHitValueError


class _Alignment:

    def __init__(self, filenames, result_file, aligner=None, output_path=None,
                 command=None, stdout=None, stderr=None):
        self.output_path = output_path
        self.filenames = filenames
        self.file = result_file
        self.aligner = aligner
        self.init_result = Result.init_software_result(name="cgecore",
                                                       gitdir=None,
                                                       type="python_module")


    def get_alignment_results(self):

        self._load_alignment_results()

        return self.init_result

    def _load_alignment_results(self):
        try:
            iterator_results = self.parse_hits()
        except AttributeError:
            iterator_results = []

        for hit in iterator_results:
            hit._get_unique_hit_key(hit_collection=self.init_result["aln_hits"])
            result_hit = AlnHit.dfs_to_dict(hit)
            self.init_result.add_class(cl="aln_hits", **result_hit)

    def save_alignment(self, json_path):

        SaveJson.dump_json(std_result_file=json_path,
                            std_result=self.init_result)


class KMAAlignment(_Alignment):

    def __init__(self, filenames, result_file, output_path=None):

        _Alignment.__init__(self, output_path=output_path, filenames=filenames,
                            result_file=result_file, aligner="kma")

    def parse_hits(self):
        for file in self.filenames:
            KMA_aln = KMA_Result(output_path=self.output_path, filename=file,
                                 aln_files=self.file)
            iter_aln = KMA_aln.iterate_hits()
            file_open = True
            while file_open:
                hit = None
                try:
                    hit = next(iter_aln)
                except StopIteration:
                    file_open = False
                if hit is not None:
                    yield hit


class BlastNAlignment(_Alignment):

    def __init__(self, output_path, filenames, result_file, extension=None,
                 headers=None):

        self.extension = extension
        self.headers = headers
        if not isinstance(result_file, str):
            raise CGEHitValueError("Only one result file type from an "
                                   "alignment can be read")

        _Alignment.__init__(self, output_path=output_path, filenames=filenames,
                            result_file=result_file, aligner="blastn")

    def parse_hits(self):
        for file in self.filenames:
            BLASTN_aln = BLASTN_Result(output_path=self.output_path,
                                       filename=file, aln_file=self.file,
                                       extension=self.extension,
                                       headers=self.headers)
            iter_aln = BLASTN_aln.iterate_hits()
            file_open = True
            while file_open:
                hit = None
                try:
                    hit = next(iter_aln)
                except StopIteration:
                    file_open = False
                if hit is not None:
                    yield hit
