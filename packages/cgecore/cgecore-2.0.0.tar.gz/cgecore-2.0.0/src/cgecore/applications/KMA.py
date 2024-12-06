from cgecore.applications.command import _ContentArgument, CommandLineBase
from cgecore.applications.command import _SwitchArgument, _SwitchValueArgument


class _KmaBaseCommandline(CommandLineBase):
    """Base Commandline object for KMA wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the KMA tools (kma, kma_index, kma_update, etc
    AND kma_shm).
    """

    def __init__(self, cmd=None, path_exec="", **kwargs):
        assert cmd is not None
        extra_parameters = [
            # Core:
            _SwitchArgument(
                ["-h", "h"],
                "Print USAGE, DESCRIPTION and ARGUMENTS description; "
                "ignore other arguments.",
                no_run=True,
            ),
            _SwitchArgument(
                ["-v", "v"],
                "Print version number;  "
                "ignore other arguments.",
                no_run=True,
            ),
            _ContentArgument(
                ["", "custom_args"],
                "Add custom arguments that are not included in the "
                "kma_application.py file."
            ),
        ]
        try:
            # Insert extra parameters - at the start just in case there
            # are any arguments which must come last:
            self.parameters = extra_parameters + self.parameters
        except TypeError:
            # Should we raise an error?  The subclass should have set this up!
            self.parameters = extra_parameters
        # Do we need a method to add a method for adding arguments in front?
        CommandLineBase.__init__(self, cmd, path_exec, **kwargs)

    def _validate_incompatibilities(self, incompatibles):
        """Validate parameters for incompatibilities (PRIVATE).
        Used by the _validate method.
        """
        for a in incompatibles:
            if self._get_parameter(a):
                for b in incompatibles[a]:
                    if self._get_parameter(b):
                        raise ValueError("Options %s and %s are incompatible."
                                         % (a, b))


class KMACommandline(_KmaBaseCommandline):
    """Base Commandline object for the wrapper of the KMA aligner.
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            # Input query options:
            _ContentArgument(
                ["-i", "input"],
                "Input file name(s)",
                filename=True,
                is_required=True,
                default="STDIN",
                alter_options=["input_int", "input_ipe"],
                incompatible=["input_int", "input_ipe"],
                allow_multiple=True,
            ),
            _ContentArgument(
                ["-ipe", "input_ipe"],
                "Input paired end file name(s)",
                filename=True,
                is_required=True,
                alter_options=["input", "input_int"],
                incompatible=["input", "input_int"],
                allow_multiple=True,
            ),
            _ContentArgument(
                ["-int", "input_int"],
                "Input interleaved file name(s)",
                filename=True,
                is_required=True,
                alter_options=["input", "input_ipe"],
                incompatible=["input", "input_ipe"],
                allow_multiple=True,
            ),  # Should this be required?
            _ContentArgument(
                ["-o", "output"],
                "Output file",
                filename=True,
                is_required=True,
                default="None",
            ),
            _ContentArgument(
                ["-t_db", "template_db"],
                "Template DB",
                filename=True,
                default="None",
                is_required=True,
            ),
            _ContentArgument(
                ["-k", "k_size"],
                "Kmersize (default by db)",
                filename=False,
                default="DB defined",
                is_required=False,
            ),
            _ContentArgument(
                ["-ml", "min_len"],
                "Minimum alignment length",
                filename=False,
                default=16,
                is_required=False,
            ),
            _ContentArgument(
                ["-p", "p_value"],
                "p-value",
                filename=False,
                default=0.05,
                is_required=False,
            ),
            _ContentArgument(
                ["-ConClave", "con_clave"],
                "ConClave version",
                filename=False,
                default=1,
                is_required=False,
            ),
            _SwitchArgument(
                ["-mem_mode", "mem_mode"],
                "Use kmers to choose best template, and save memory",
            ),
            _SwitchValueArgument(
                ["-proxi", "proxi"],
                "Use proximity scoring under template mapping",
                filename=False,
                default="False/1.0",
                is_required=False,
            ),
            _SwitchArgument(
                ["-ex_mode", "ex_mode"],
                "Searh kmers exhaustively",
            ),
            _SwitchArgument(
                ["-ef", "extra_files"],
                "Output extra files",
            ),
            _SwitchValueArgument(
                ["-vcf", "vcf"],
                "Make vcf file, 2 to apply FT",
                filename=False,
                default="False/0",
                is_required=False,
            ),
            _SwitchValueArgument(
                ["-sam", "sam"],
                "Output sam to stdout, 4 to output mapped reads,"
                "2096 for aligned",
                filename=False,
                default="False/1.0",
                is_required=False,
            ),
            _SwitchArgument(
                ["-nc", "non_consensus"],
                "No consensus file",
            ),
            _SwitchArgument(
                ["-na", "no_aln"],
                "No aln file",
            ),
            _SwitchArgument(
                ["-nf", "no_frag"],
                "No frag file",
            ),
            _SwitchArgument(
                ["-deCon", "deCon"],
                "Remove contamination",
            ),
            _SwitchArgument(
                ["-dense", "dense"],
                "Do not allow insertions in assembly",
            ),
            _SwitchArgument(
                ["-sasm", "sasm"],
                "Skip alignment and assembly",
            ),
            _SwitchValueArgument(
                ["-ref_fsa", "ref_sa"],
                "Consensus sequence will have 'n' instead of gaps",
                filename=False,
                is_required=False,
                default="False/0",
            ),
            _SwitchArgument(
                ["-matrix", "matrix"],
                "Outputs assembly matrix",
            ),
            _SwitchArgument(
                ["-a", "best_maps"],
                "Print all best mappings",
            ),
            _ContentArgument(
                ["-mp", "min_phred"],
                "Minimum phred score",
                filename=False,
                default=20,
                is_required=False,
            ),
            _ContentArgument(
                ["-5p", "cut_5p"],
                "Cut a constant number of nucleotides from the 5 prime",
                filename=False,
                default=0,
                is_required=False,
            ),
            _ContentArgument(
                ["-3p", "cut_3p"],
                "Cut a constant number of nucleotides from the 3 prime",
                filename=False,
                default=0,
                is_required=False,
            ),
            _SwitchArgument(
                ["-Sparse", "sparse"],
                "Only count kmers",
            ),
            _SwitchValueArgument(
                ["-Mt1", "Mt1"],
                "Map only to 'num' template",
                filename=False,
                is_required=False,
                default="False/0",
            ),
            _ContentArgument(
                ["-ID", "ID"],
                "Minimum ID",
                filename=False,
                default="1.0%",
                is_required=False,
            ),
            _ContentArgument(
                ["-ss", "ss"],
                "Sparse sorting (q,c,d)",
                filename=False,
                default="q",
                checker_function=lambda x: x in ["q", "c", "d"],
                is_required=False,
            ),
            _ContentArgument(
                ["-pm", "pm"],
                "Pairing method (p,u,f)",
                filename=False,
                default="u",
                checker_function=lambda x: x in ["p", "u", "f"],
                is_required=False,
            ),
            _ContentArgument(
                ["-fpm", "fpm"],
                "Fine Pairing method (p,u,f)",
                filename=False,
                checker_function=lambda x: x in ["p", "u", "f"],
                default="u",
                is_required=False,
            ),
            _ContentArgument(
                ["-apm", "apm"],
                "Sets both pm and fpm (p,u,f)",
                filename=False,
                default="u",
                checker_function=lambda x: x in ["p", "u", "f"],
                is_required=False,
            ),
            _ContentArgument(
                ["-shm", "shm"],
                "Use shared DB made by kma_shm",
                filename=False,
                default="0 (lvl)",
                is_required=False,
            ),
            _SwitchArgument(
                ["-mmap", "mmap"],
                "Memory map *.comp.by",
            ),
            _ContentArgument(
                ["-tmp", "tmp"],
                "Set directory for temporary files.",
                filename=True,
                is_required=False,
            ),
            _SwitchArgument(
                ["-1t1", "kma_1t1"],
                "Force end to end mapping"
            ),
            _SwitchArgument(
                ["-hmm", "hmm"],
                "Use a HMM to assign template(s) to query sequences"
            ),
            _SwitchArgument(
                ["-ck", "count_k"],
                "Count kmers instead of pseudo alignment"
            ),
            _SwitchArgument(
                ["-ca", "circular_aln"],
                "Make circular alignments"
            ),
            _SwitchArgument(
                ["-boot", "bootstrap"],
                "Bootstrap sequence"
            ),
            _SwitchArgument(
                ["-bc", "bc"],
                "Base calls should be significantly overrepresented",
                default=True,
                incompatible=["bc90"],
            ),
            _SwitchArgument(
                ["-bc90", "bc90"],
                "Base calls should be both significantly overrepresented, and"
                " have 90% agreement.",
                incompatible=["bc"]
            ),
            _SwitchArgument(
                ["-bcNano", "bcNano"],
                "Call bases at suspicious deletions, made for nanopore."
            ),
            _ContentArgument(
                ["-bcd", "bcd"],
                "Minimum depth at base.",
                filename=False,
                default=1,
                is_required=False,
            ),
            _SwitchArgument(
                ["-bcg", "bcg"],
                "Maintain insignificant gaps",
            ),
            _SwitchArgument(
                ["-and", "and"],
                "Both mrs and p_value thresholds has to reached to in order "
                "to	report a template hit.",
            ),
            _ContentArgument(
                ["-mq", "MinMapQ"],
                "Minimum mapping quality",
                filename=False,
                default=0,
                is_required=False,
            ),
            _ContentArgument(
                ["-mrs", "MinAlnQ"],
                "Minimum alignment score, normalized to alignment length",
                filename=False,
                default=0.50,
                is_required=False,
            ),
            _ContentArgument(
                ["-mct", "mct"],
                "Max overlap between templates",
                filename=False,
                default=0.50,
                is_required=False,
            ),
            _ContentArgument(
                ["-reward", "reward"],
                "Score for match",
                filename=False,
                default=1,
                is_required=False,
            ),
            _ContentArgument(
                ["-penalty", "penalty"],
                "Penalty for mismatch",
                filename=False,
                default=-2,
                is_required=False,
            ),
            _ContentArgument(
                ["-gapopen", "gap_open"],
                "Penalty for gap opening",
                filename=False,
                default=-3,
                is_required=False,
            ),
            _ContentArgument(
                ["-gapextend", "gap_extend"],
                "Penalty for gap extension",
                filename=False,
                default=-1,
                is_required=False,
            ),
            _ContentArgument(
                ["-per", "reward_pairing"],
                "Reward for pairing end",
                filename=False,
                default=7,
                is_required=False,
            ),
            _ContentArgument(
                ["-localopen", "local_open"],
                "Penalty for openning a local chain",
                filename=False,
                default=-6,
                is_required=False,
            ),
            _ContentArgument(
                ["-Npenalty", "n_penalty"],
                "Penalty matching N",
                filename=False,
                default=0,
                is_required=False,
            ),
            _ContentArgument(
                ["-transition", "transition"],
                "Penalty for transition",
                filename=False,
                default=-2,
                is_required=False,
            ),
            _ContentArgument(
                ["-transversion", "transversion"],
                "Penalty for transversion",
                filename=False,
                default=-2,
                is_required=False,
            ),
            _SwitchArgument(
                ["-cge", "cge"],
                "Set CGE penalties and rewards",
            ),
            _ContentArgument(
                ["-t", "threads"],
                "Number of threads",
                filename=False,
                default=1,
                is_required=False,
            ),
            _SwitchArgument(
                ["-status", "status"],
                "Extra status",
            ),
            _SwitchArgument(
                ["-verbose", "verbose"],
                "Extra verbose",
            ),
            _SwitchArgument(
                ["-c", "citation"],
                "Citation",
                no_run=True,
            ),
            _SwitchArgument(
                ["-ont", "ont"],
                "Set 3rd gen genefinding preset",
            ),
            _ContentArgument(
                ["-md", "md"],
                "minimum depth",
                filename=False,
                default=0.0,
                is_required=False,
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class KMAIndexCommandline(_KmaBaseCommandline):
    """Base Commandline object for (new) NCBI BLAST+ wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma_index", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-i", "input"],
                "Input/query file name (STDIN: '--')",
                filename=True,
                default="None",
                is_required=False,
                allow_multiple=True,
                alter_options=["batch"],
                incompatible=["batch"],

            ),
            _ContentArgument(
                ["-o", "output"],
                "Output file",
                filename=False,
                default="Input file",
                is_required=False,
            ),
            _ContentArgument(
                ["-batch", "batch"],
                "Batch input file",
                filename=True,
                is_required=False,
                alter_options=["input"],
                incompatible=["input"]
            ),
            _SwitchValueArgument(
                ["-deCon", "deCon"],
                "File with contamination (STDIN: '--')",
                default="None/False",
                filename=True,
                is_required=False,
            ),
            _ContentArgument(
                ["-batchD", "batchD"],
                "Batch decon file",
                filename=True,
                is_required=False,
            ),
            _SwitchValueArgument(
                ["-t_db", "template_db"],
                "Add to existing DB",
                filename=True,
                default="None/False",
                is_required=False,
            ),
            _ContentArgument(
                ["-k", "k_size"],
                "Kmersize",
                filename=False,
                default=16,
                is_required=False,
            ),
            _ContentArgument(
                ["-k_t", "k_temp"],
                "Kmersize for template identification",
                filename=False,
                default=16,
                is_required=False,
            ),
            _ContentArgument(
                ["-k_i", "k_index"],
                "Kmersize for indexing",
                filename=False,
                default=16,
                is_required=False,
            ),
            _ContentArgument(
                ["-ML", "min_len"],
                "Minimum length for templates",
                filename=False,
                default="kmersize (16)",
                is_required=False,
            ),
            _ContentArgument(
                ["-CS", "cs"],
                "Start chain size",
                filename=False,
                default="1 M",
                is_required=False,
            ),
            _SwitchArgument(
                ["-ME", "mega_db"],
                "Mega DB",
            ),
            _SwitchArgument(
                ["-NI", "no_index"],
                "Do not dump *.index.b",
            ),
            _SwitchValueArgument(
                ["-Sparse", "sparse"],
                "Make Sparse DB ('-' for no prefix)",
                filename=False,
                default="None/False",
                is_required=False,
            ),
            _ContentArgument(
                ["-ht", "homology_temp"],
                "Homology template",
                filename=False,
                default=1.0,
                is_required=False,
            ),
            _ContentArgument(
                ["-hq", "homology_query"],
                "Homology query",
                filename=False,
                default=1.0,
                is_required=False,
            ),
            _SwitchArgument(
                ["-and", "and"],
                "Both homolgy thresholds has to be reached",
            ),
            _SwitchArgument(
                ["-nbp", "no_bias"],
                "No bias print",
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class KMAShmCommandline(_KmaBaseCommandline):
    """Base Commandline object for (new) NCBI BLAST+ wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma_shm", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-t_db", "template_db"],
                "Template DB",
                filename=True,
                default=None,
                is_required=True,
            ),
            _SwitchArgument(
                ["-destroy", "destroy"],
                "Destroy shared memory",
            ),
            _ContentArgument(
                ["-shmLvl", "shmLvl"],
                "Level of shared memory",
                filename=False,
                default=1,
                is_required=False,
            ),
            _SwitchArgument(
                ["-shm-h", "shm_h"],
                "Explain of shared memory",
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class KMASeq2FastaCommandline(_KmaBaseCommandline):
    """Base Commandline object for (new) NCBI BLAST+ wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma seq2fasta", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-t_db", "template_db"],
                "Template DB",
                filename=True,
                default=None,
                is_required=True,
            ),
            _SwitchArgument(
                ["-seqs", "seqs"],
                "Comma separated list of templates",
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class KMADistCommandline(_KmaBaseCommandline):
    """Base Commandline object for (new) NCBI BLAST+ wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma dist", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-t_db", "template_db"],
                "Template DB",
                filename=True,
                is_required=True,
            ),
            _ContentArgument(
                ["-o", "output"],
                "Output file",
                filename=True,
                default="DB",
                is_required=False,
            ),
            _ContentArgument(
                ["-f", "output_f"],
                "Output flags",
                filename=False,
                default=1,
                checker_function=lambda x: x in [1, 4],
                is_required=False,
            ),
            _SwitchArgument(
                ["-fh", "help_flags"],
                "Help on option '-f'",
            ),
            _ContentArgument(
                ["-d", "distance_method"],
                "DistanceMethod",
                filename=False,
                checker_function=lambda x: x in [1, 2, 4, 8, 16, 32, 64, 128,
                                                 256, 512, 1024, 2048, 4096],
                default=1,
                is_required=False,
            ),
            _SwitchArgument(
                ["-dh", "help_distance"],
                "Help on option '-d'",
            ),
            _SwitchArgument(
                ["-m", "matrix"],
                "Allocate matrix on the disk",
            ),
            _ContentArgument(
                ["-tmp", "tmp"],
                "Set directory for temporary file",
                filename=True,
                is_required=False,
            ),
            _ContentArgument(
                ["-t", "threads"],
                "Number of threads",
                filename=False,
                default=1,
                is_required=False,
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class KMADBCommandline(_KmaBaseCommandline):
    """Base Commandline object for (new) NCBI BLAST+ wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the BLAST tools (blastn, rpsblast, rpsblast, etc).
    """

    def __init__(self, cmd="kma db", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-t_db", "template_db"],
                "Template DB",
                filename=True,
                is_required=True,
            ),
        ]
        _KmaBaseCommandline.__init__(self, cmd, path_exec, **kwargs)
