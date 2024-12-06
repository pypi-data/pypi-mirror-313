from argparse import ArgumentParser




class CGEArgumnents:
    def __init__(self, program_description = "", allow_abbrev = True, **kwargs):
        self.parser = ArgumentParser(description = program_description,
                                     allow_abbrev = allow_abbrev,
                                     **kwargs)

    def fasta_input(self, shortcut = "-a", flag = "--inputfasta", **kwargs):
        self.parser.add_argument(shortcut, flag,
                                 help="Input fasta file.",
                                 default=None,
                                 **kwargs)


    def fastq_input(self, shortcut = "-q", flag = "--inputfastq"):
        self.parser.add_argument(shortcut, flag,
                                 help=("Input fastq file(s). Assumed to be single-end "
                                       "fastq if only one file is provided, and assumed"
                                       " to be paired-end data if two files are "
                                       "provided."),
                                 nargs = "+",
                                 default=[],
                                 type = str)


    def nanopore(self, flag = "--nanopore", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 dest="nanopore",
                                 help="If nanopore data is used",
                                 default=default)

    def output_path(self, shortcut = "-o", flag = "--output_path", required = True):
        self.parser.add_argument(shortcut, flag,
                                 help=("Output directory. If it doesn't exist, it will "
                                       "be created."),
                                 required=required,
                                 default=None)



    def blast_path(self, flag = "--blastPath", default = None):
        self.parser.add_argument(flag,
                                 help="Path to blastn",
                                 default=default)


    def kma_path(self, flag = "--kma_path", default = None):
        self.parser.add_argument(flag,
                                 help="Path to KMA",
                                 default=default)

    def species(self, shortcut = "-s", flag = "--species", default = "other",
                multiple = False):

        if multiple == False:
            self.parser.add_argument(shortcut, flag,
                                    help="Species in the sample",
                                    default=default)
        else:
            self.parser.add_argument(shortcut, flag,
                                    help="Species in the sample",
                                    default=default,
                                    nargs="+")

    def ignore_missing_species(self, flag = "--ignore_missing_species", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 help=("If set, species is provided and --point flag "
                                       "is set, will not throw an error if no database "
                                       "is found for the provided species. If species "
                                       "is not found. Point mutations will silently "
                                       "be ignored."),
                                 default=default)


    def add_alignments_to_json(self, flag = "--output_aln", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 help="will add the alignments in the json output.",
                                 default=default)

    def add_database_res_arg(self,flag = "--db_res", default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the databases for ResFinder."),
                                 default=default)

    def add_database_res_kma_arg(self,flag = "--db_res_kma", default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the ResFinder databases indexed with "
                                       "KMA. Defaults to the value of the --db_res "
                                       "flag."),
                                 default=default)

    def add_database_disinf_arg(self, flag = "--db_disinf", default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the databases for DisinFinder."),
                                 default=default)

    def add_database_disinf_kma_arg(self,flag= "--db_disinf_kma", default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the DisinFinder databases indexed with "
                                       "KMA. Defaults to the value of the --db_res "
                                       "flag."),
                                 default=default)


    def add_database_point_arg(self,flag = "--db_point", default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the databases for PointFinder."),
                                 default=default)

    def add_database_point_kma_arg(self,flag ="--db_point_kma",  default = None):
        self.parser.add_argument(flag,
                                 help=("Path to the PointFinder databases indexed with "
                                       "KMA. Defaults to the value of the "
                                       "--db_point flag."),
                                 default=default)


    def add_overlap_arg(self,flag = "--acq_overlap", default = None):
        self.parser.add_argument(flag,
                                 help="Genes are allowed to overlap this number of\
                                         nucleotides. Default: {}.", # rest needed to be deleted
                                 type=int,
                                 default=default)

    def add_min_cov_arg(self,flag = "--min_cov", default = None):
        self.parser.add_argument(flag,
                                 help=("Minimum (breadth-of) coverage of ResFinder "
                                       "within the range 0-1."),
                                 type=float,
                                 default=default)


    def add_threshold_arg(self, shortcut = "-t", flag = "--threshold", default = None):
        self.parser.add_argument(shortcut, flag,
                                 help=("Threshold for identity of ResFinder within the "
                                       "range 0-1."),
                                 type=float,
                                 default=default)

    def add_disinfectant_arg(self, shortcut = "-d", flag = "--disinfectant", default = False):
        self.parser.add_argument(shortcut, flag,
                                 action="store_true",
                                 help="Run resfinder for disinfectant resistance genes",
                                 default=default)

    def add_chromosomal_arg(self,shortcut = "-c", flag = "--chromosomal", default = None):
        self.parser.add_argument(shortcut, flag,
                                 action="store_true",
                                 help="Run resfinder for chromosomal resistance genes",
                                 default=default)

    def add_specific_gene_arg(self,flag = "--specific_gene", default = None):
        self.parser.add_argument(flag,
                                 nargs='+',
                                 help="Specify genes existing in the database to \
                                         search for - if none is specified all genes are \
                                         included in the search.",
                                 default=default)

    def add_unknown_mut_arg(self,shortcut = "-u", flag = "--unknown_mut", default = False):
        self.parser.add_argument(shortcut, flag,
                                 action="store_true",
                                 help=("Show all mutations found even if in unknown to "
                                       "the resistance database"),
                                 default=default)


    def add_min_cov_point_arg(self,flag = "--min_cov_point", default = None):
        self.parser.add_argument(flag,
                                 help=("Minimum (breadth-of) coverage of Pointfinder "
                                       "within the range 0-1. If None is selected, the "
                                       "minimum coverage of ResFinder will be used."),
                                 type=float,
                                 default=default)

    def add_threshold_point_arg(self,flag = "--threshold_point", default = None):
        self.parser.add_argument(flag,
                                 help=("Threshold for identity of Pointfinder within "
                                       "the range 0-1. If None is selected, the minimum"
                                       " coverage of ResFinder will be used."),
                                 type=float,
                                 default=default)

    def add_ignore_indels_arg(self,flag = "--ignore_indels", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 help=("Ignore frameshift-causing indels in "
                                       "Pointfinder."),
                                 default=default)

    def add_ignore_stop_codons_arg(self,flag = "--ignore_stop_codons", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 help="Ignore premature stop codons in Pointfinder.",
                                 default=default)

    def add_version_arg(self,version, shortcut = "-v",flag = "--version", ):
        self.parser.add_argument(shortcut, flag,
                                 action="version",
                                 version=version,
                                 help="Show program's version number and exit")

    def add_pickle_arg(self,flag = "--pickle", default = False):
        self.parser.add_argument(flag,
                                 action="store_true",
                                 help=("Create a pickle dump of the Isolate object. "
                                       "Currently needed in the CGE webserver. "
                                       "Dependency and this option is being removed."),
                                 default=default)

    def add_kma_arguments(self, flag = "--kma_arguments", default = None):
        self.parser.add_argument(flag,
                                 default=default,
                                 type = str)

    def add_db_path_arg(self,flag = "--db_path", default = None, required = True):
        self.parser.add_argument(flag,
                                 help=("Path to the database(s). Can be a directory or a filepath."),
                                 default=default,
                                 required = required,
                                 nargs = "+")

    def add_tax(self, flag = "--tax", default = None):
        self.parser.add_argument(flag,
                                 default = default,
                                 type = str)

    def add_output_json(self, flag = "--output_json", default = None):
        self.parser.add_argument(flag,
                                 default = default,
                                 type = str)
