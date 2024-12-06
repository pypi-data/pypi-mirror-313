# Created by Alfred Ferrer Florensa
"""Contains objects for reading """

import os
import glob
import json
from cgecore.utils.savers_mixin import SaveJson
from cgecore.applications.KMA import KMACommandline
from cgecore.applications.Blast import BlastNCommandline
from cgecore.alignment.read_alignment import KMAAlignment, BlastNAlignment
from cgecore.output.result import Result
from cgecore.sequence.SeqHit import AlnHit
from cgecore.applications.command import CommandResume
from cgecore.alignment.blast.alignment_files import Iterator_BlastSepFile



class CGELibAttributeError(AttributeError):
    """"""

    def __init__(self, message, *args):
        self.message = message
        # allow users initialize misc. arguments as any other builtin Error
        super(CGELibAttributeError, self).__init__(message, *args)



class _Aligner:

    def __init__(self, aligner=None, commandline_exec=None, result_file=None):

        self.aligner = aligner

        self.commandline_exec = commandline_exec
        self.result_file = result_file
        self.alignment = None
        self.alignment_parameters = None
        self.result_dict = Result.init_software_result(name="cgecore",
                                                       gitdir=None,
                                                       type="python_module")
        self.alignment_files = []

    def load_exec_command(self, command, stdout, stderr, key=None):

        command_info = CommandResume(exec_name=self.aligner, command=command,
                                     stdout=stdout, stderr=stderr)

        CommandResume.std_executable(cmdresume=command_info,
                                     json_report=self.result_dict, key=key)

        self.result_dict.add_class(cl="software_executions", **command_info)

    def create_commands(self, parameters, output_param, variable_iter=None, values_iter=None):
        commandlines = {}
        if self.commandline_exec is None:
            raise ValueError("No commandline executable has been defined")
        if variable_iter is None:
            commandlines[variable_iter] = self.commandline_exec(**parameters)
        else:
            if variable_iter in parameters:
                raise KeyError("The parameter to iterate over the results (%s)"
                               " has already been set with 'set_aligner_params"
                               "' creating the commandline (%s)" % (
                                        variable_iter, parameters))
                #variable_list = parameters[variable_iter]
            else:
                variable_list = values_iter
                #raise KeyError("The parameter to iterate over the results (%s)"
                #               " is not found in the parameters introduced for"
                #               " creating the commandline (%s)" % (variable_iter,
                #                                                   parameters))
            if not isinstance(variable_list, list):
                raise ValueError("The variable chosen (%s) to iterate over is "
                                 " not a list (%s)" % (variable_iter, variable_list)
                                 )
            else:
                init_out_path = parameters[output_param]
                for variable_value in variable_list:
                    parameters[variable_iter] = variable_value
                    output_path = _Aligner.create_outputname(
                                    aligner=self.aligner,
                                    out_path=init_out_path,
                                    parameters=parameters,
                                    variable=variable_iter)
                    key_path = os.path.basename(output_path).split(os.extsep, 1)[0]
                    parameters[output_param] = output_path
                    self.alignment_files.append(output_path)
                    commandlines[key_path] = self.commandline_exec(**parameters)
        return commandlines

    @staticmethod
    def create_outputname(aligner, out_path, parameters, variable):
        value = parameters[variable]
        if glob.glob(value+".*"):
            for file in glob.glob(value+".*"):
                value = os.path.basename(file).split(os.extsep, 1)[0]
                break
        elif os.path.isfile(value):
            value = os.path.splitext(os.path.basename(value))[0]
        else:
            value = value
        if os.path.isdir(out_path):
            path_str = "%s/%s-alignment_" % (out_path, aligner)
        else:
            path_str = "%s_%s-alignment_" % (out_path, aligner)
        if aligner == "kma":
            new_out = "%s%s-%s" % (path_str, variable, value)
        else:
            extension = BlastNAligner._create_extension(parameters)
            new_out = "%s%s-%s%s" % (path_str, variable, value, extension)
        return os.path.abspath(new_out)

    def report_aligner(self):
        if not self.result_dict["software_exec"]:
            raise AttributeError("""The Report of the aligner is empty.
                                    Probably as the aligner has not been runned
                                    """)
        return self.result_dict["software_exec"]

    @staticmethod
    def define_alignment_params(**kwargs):
        alignment_parameters = {}
        alignment_parameters.update((key,
                                     value) for key, value in kwargs.items())
        return alignment_parameters

    def set_aligner_params(self, **kwargs):

        self.alignment_parameters = _Aligner.define_alignment_params(**kwargs)


    def __call__(self, commands):

        for key, run_command in commands.items():
            stdout, stderr = run_command()
            self.load_exec_command(command=str(run_command), stdout=stdout,
                                   stderr=stderr, key=key)


    def parse_hits(self):

        if self.alignment is None:
            raise CGELibAttributeError("Alignment has not been created yet. "
                                       "Run the Aligner to produce the "
                                       "alignment")

        iterator_alignment = self.alignment.parse_hits()
        for hit in iterator_alignment:
            yield hit

    def _load_alignment_results(self):
        try:
            iterator_results = self.parse_hits()
        except AttributeError:
            iterator_results = []

        for hit in iterator_results:
            hit._get_unique_hit_key(hit_collection=self.result_dict["aln_hits"])
            result_hit = AlnHit.dfs_to_dict(hit)
            hit["exec_key"] = AlnHit.get_run_key(
                        software_execs=self.result_dict["software_executions"],
                        hit=hit
                        )
            self.result_dict.add_class(cl="aln_hits", **result_hit)

    def read_alignment_result(self):

        self._load_alignment_results()

        return self.result_dict

    def save_results(self, json_path, std_result=None):
        if std_result is None:
            SaveJson.dump_json(std_result_file=json_path,
                                std_result=self.result_dict)
        else:
            SaveJson.dump_json(std_result_file=json_path,
                                std_result=std_result)

    @classmethod
    def load_results(cls, json_path):

        if not os.path.isfile(json_path):
            raise OSError("The json file %s does not exists" % json_path)
        with open(json_path, "r") as read_file:
            data = json.load(read_file)

        if cls.__name__ == "KMAAligner":
            new_aligner_class = KMAAligner()
        elif cls.__name__ == "BlastNAligner":
            new_aligner_class = BlastNAligner()
        else:
            new_aligner_class = _Aligner()
        for key, value in data["software_executions"].items():
            new_aligner_class.result_dict.add_class(cl="software_executions",
                                                **value)
        print(data["aln_hits"])
        new_aligner_class.alignment = data["aln_hits"]

        return new_aligner_class




class BlastNAligner(_Aligner):

    outfmt_to_resultfile = {
        5: "XML", 6: "TSV", 7: "TSV_extra", 10: "CSV"
    }

    std_header = ["qseqid", "sseqid", "pident", "length", "mismatch",
                    "gapopen", "qstart", "qend", "sstart", "send",
                    "evalue", "bitscore"]

    def __init__(self, result_file=None):

        _Aligner.__init__(self, aligner="blastn",
                          commandline_exec=BlastNCommandline,
                          result_file=result_file)

    @staticmethod
    def get_output_format(alignment_parameters):
        if "outfmt" in alignment_parameters:
            if isinstance(alignment_parameters["outfmt"], list):
                try:
                    file_format = int(alignment_parameters["outfmt"][0])
                    header = alignment_parameters["outfmt"][1:]
                except ValueError:
                    raise ValueError("The list of 'outfmt' has to have the number"
                                     " of the alignment view option first "
                                     "(%s)" % (
                                     alignment_parameters["outfmt"][0]))
            else:
                file_format = int(alignment_parameters["outfmt"])
                header = None
        else:
            raise ValueError("The package CGELIB cannot read the "
                             "results of running Blast with the parameter "
                             "'-outfmt' set to 0 (standard).")
        return file_format, header

    @staticmethod
    def get_header_format(alignment_parameters):
        file_format, header_format = BlastNAligner.get_output_format(
                                    alignment_parameters=alignment_parameters)
        if file_format == 5:
            header = None
        else:
            if header_format is None:
                header = BlastNAligner.std_header
            else:
                header = []
                for i in header_format:
                    if i == "std":
                        header.extend(BlastNAligner.std_header)
                    else:
                        if i not in Iterator_BlastSepFile.STD_header.keys():
                            raise ValueError("The format specifier %s is not"
                                             " part of the blastn options" % (
                                             i))
                        else:
                            if i not in header:
                                header.append(i)
        return header

    def get_resultfiles(self):

        file_format, _ = BlastNAligner.get_output_format(
                                alignment_parameters=self.alignment_parameters)

        if self.result_file is None:
            if(file_format in
               BlastNAligner.outfmt_to_resultfile):
                self.result_file = BlastNAligner.outfmt_to_resultfile[
                                        self.alignment_parameters["outfmt"]]
            else:
                raise ValueError("""The package CGELIB cannot read the
                                results of running Blast with the parameter
                                '-outfmt' set to %s
                                """ % self.alignment_parameters["outfmt"])
        elif isinstance(file_format, list):
            raise TypeError("The result file for Blast cannot be a list.")
        else:
            bool_found = 0
            for k, v in BlastNAligner.outfmt_to_resultfile.items():
                if v == BlastNAligner.outfmt_to_resultfile[file_format]:
                    if k == file_format:
                        bool_found = 1
                        self.result_file = v
                        break
                elif v == file_format:
                    if k == file_format:
                        bool_found = 1
                        break
                    else:
                        raise ValueError("""The result file selected has been
                                         %s, while the 'outfmt' option %s (
                                         result file %s) has been runned"""
                                         % (self.result_file,
                                            file_format,
                                            BlastNAligner.outfmt_to_resultfile[
                                                self.alignment_parameters["outfmt"]]
                                            ))
            if bool_found == 0:
                raise ValueError("""The result file %s selected is not part of
                                    the options available (TSV, XML, TSV_extra,
                                    CSV)""" % self.result_file)

    def fit_alignment(self):

        self.get_resultfiles()

        header = BlastNAligner.get_header_format(
                    alignment_parameters=self.alignment_parameters)

        alignment = BlastNAlignment(output_path=None,
                                    filenames=self.alignment_files,
                                    result_file=self.result_file,
                                    headers=header)
        self.alignment = alignment

    @staticmethod
    def _create_extension(parameters):
        format_outfmt, _ = BlastNAligner.get_output_format(
                                    alignment_parameters=parameters)
        if format_outfmt == 5:
            extension = ".xml"
        elif format_outfmt == 10:
            extension = ".csv"
        else:
            extension = ".tsv"
        return extension



    def __call__(self, values_iter, variable_iter="subject"):

        commands = self.create_commands(parameters=self.alignment_parameters,
                                        output_param="output",
                                        variable_iter=variable_iter,
                                        values_iter=values_iter)
        super(BlastNAligner, self).__call__(commands)

        return self.result_dict["software_executions"]



class KMAAligner(_Aligner):

    def __init__(self, result_file=None):

        _Aligner.__init__(self, aligner="kma",
                          commandline_exec=KMACommandline,
                          result_file=result_file)

    def get_resultfiles(self):

        if self.result_file is None:
            if "sparse" in self.alignment_parameters:
                self.result_file = ["Sparse"]
            else:
                self.result_file = ["Result", "Fragments", "Consensus",
                                    "Alignment", "Matrix", "Mapstat",
                                    "Frag_Raw", "VCF"]

        if("non_consensus" in self.alignment_parameters
           and "Consensus" in self.result_file):
            self.result_file.remove("Consensus")
        if("no_aln" in self.alignment_parameters
           and "Alignment" in self.result_file):
            self.result_file.remove("Alignment")
        if("no_frag" in self.alignment_parameters
           and "Fragments" in self.result_file):
            self.result_file.remove("Fragments")
        if("extra_files" in self.alignment_parameters
           and "Mapstat" in self.result_file):
            self.result_file.remove("Mapstat")
        if("vcf" in self.alignment_parameters
           and "VCF" in self.result_file):
            self.result_file.remove("VCF")
        if("matrix" in self.alignment_parameters
            and "Matrix" in self.result_file):
            self.result_file.remove("Matrix")
        if("best_maps" in self.alignment_parameters
           and "Frag_Raw" in self.result_file):
            self.result_file.remove("Frag_Raw")

    def fit_alignment(self):

        self.get_resultfiles()

        alignment = KMAAlignment(output_path=None,
                                 filenames=self.alignment_files,
                                 result_file=self.result_file)
        self.alignment = alignment


    def __call__(self, values_iter, variable_iter="template_db"):


        commands = self.create_commands(parameters=self.alignment_parameters,
                                        output_param="output",
                                        variable_iter=variable_iter,
                                        values_iter=values_iter)

        super(KMAAligner, self).__call__(commands)

        return self.result_dict["software_executions"]
