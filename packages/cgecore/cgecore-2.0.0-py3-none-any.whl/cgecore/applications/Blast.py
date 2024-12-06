from cgecore.applications.command import _ContentArgument, CommandLineBase
from cgecore.applications.command import _SwitchArgument


class _BlastBaseCommandline(CommandLineBase):
    """Base Commandline object for Blast wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the blast tools (blastn, etc).
    """

    def __init__(self, cmd=None, path_exec="", **kwargs):
        assert cmd is not None
        extra_parameters = [
            # Core:
            _SwitchArgument(
                ["-h", "help"],
                "Print USAGE, DESCRIPTION description; "
                "ignore other arguments.",
                no_run=True,
            ),
            _SwitchArgument(
                ["-help", "help_extended"],
                "Print EXTENDED USAGE, DESCRIPTION and ARGUMENTS description; "
                "ignore other arguments.",
                no_run=True,
            ),
            _SwitchArgument(
                ["-version", "version"],
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
        except AttributeError:
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


class _BlastSearchBaseCommandline(_BlastBaseCommandline):
    """Base Commandline object for Blast wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the blast tools (blastn, etc).
    """

    def __init__(self, cmd=None, path_exec="", **kwargs):
        assert cmd is not None
        extra_parameters = [
            # Core:
            _ContentArgument(
                ["-db", "db"],
                "BLAST database name",
                filename=True,
                is_required=True,
                default=None,
                alter_options=["subject", "subject_loc"],
                incompatible=["subject", "subject_loc"],
            ),
            _ContentArgument(
                ["-query", "query"],
                "Query file name",
                filename=True,
                is_required=True,
                alter_options=["query_loc"],
                default="-",
            ),
            _ContentArgument(
                ["-query_loc", "query_location"],
                "Location on the query sequence",
                filename=True,
                is_required=True,
                alter_options=["query"],
                default="STDIN",
            ),
            _ContentArgument(
                ["-out", "output"],
                "Output file name",
                filename=True,
                is_required=True,
                default="STDOUT",
            ),
            _ContentArgument(
                ["-evalue", "evalue"],
                "Expect value (E) for saving hits",
                filename=True,
                is_required=False,
                default=10.0,
            ),
            _ContentArgument(
                ["-subject", "subject"],
                "File with subject sequence(s) to search.",
                filename=True,
                incompatible=["db", "gilist", "seqidlist", "negative_gilist",
                              "db_soft_mask", "db_hard_mask"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-subject_loc", "subject_location"],
                "Location on the subject sequence (Format: start-stop).",
                filename=True,
                incompatible=["db", "gilist", "seqidlist", "negative_gilist",
                              "db_soft_mask", "db_hard_mask"],
                is_required=False,
                default=None,
            ),
            _SwitchArgument(
                ["-show_gis", "show_GIs"],
                "Show NCBI GIs in report.",
            ),
            _ContentArgument(
                ["-num_descriptions", "num_descriptions"],
                "Show one-line descriptions for this number of database "
                "sequences.",
                filename=False,
                checker_function=lambda x: x >= 0,
                is_required=False,
                default=500,
            ),
            _ContentArgument(
                ["-num_alignments", "num_alignments"],
                "Show alignments for this number of database sequences.",
                filename=False,
                checker_function=lambda x: x >= 0,
                is_required=False,
                default=250,
            ),
            _ContentArgument(
                ["-max_target_seqs", "max_target_seqs"],
                "Number of aligned sequences to keep. Use with report formats "
                "that do not have separate definition line and alignment "
                "sections such as tabular (all outfmt > 4). Not compatible "
                "with num_descriptions or num_alignments. Ties are broken by "
                "order of sequences in the database.",
                filename=False,
                is_required=False,
                checker_function=lambda x: x >= 1,
                incompatible=["num_descriptions", "num_alignments"],
                default=500,
            ),
            _ContentArgument(
                ["-max_hsps", "max_hsps"],
                "Maximum number of HSPs (alignments) to keep for any single "
                "query-subject pair. The HSPs shown will be the best as judged"
                " by expect value. This number should be an integer that is "
                "one or greater. If this option is not set, BLAST shows all "
                "HSPs meeting the expect value criteria. Setting it to one "
                "will show only the best HSP for every query-subject pair",
                filename=False,
                checker_function=lambda x: x >= 1,
                is_required=False,
                default=None,
            ),
            _SwitchArgument(
                ["-html", "html"],
                "Produce HTML output",
            ),
            _ContentArgument(
                ["-seqidlist", "seqidlist"],
                "Restrict search of database to list of SeqId's.",
                filename=False,
                incompatible=["negative_gilist", "gilist", "remote",
                              "subject", "subject_loc"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-gilist", "gilist"],
                "Restrict search of database to GI’s listed in this file. "
                "Local searches only.",
                filename=True,
                incompatible=["negative_gilist", "seqidlist", "remote",
                              "subject", "subject_loc"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-negative_gilist", "negative_gilist"],
                "Restrict search of database to everything except the GI’s "
                "listed in this file. Local searches only.",
                filename=True,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-entrez_query", "entrez_query"],
                "Restrict search with the given Entrez query. Remote searches "
                "only.",
                filename=False,
                required_options=["remote"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-culling_limit", "culling_limit"],
                "Delete a hit that is enveloped by at least this many "
                "higher-scoring hits.",
                filename=False,
                is_required=False,
                incompatible=["best_hit_overhang", "best_hit_score_edge"],
                checker_function=lambda x: x >= 0,
                default=None,
            ),
            _ContentArgument(
                ["-best_hit_overhang", "best_hit_overhang"],
                "Best Hit algorithm overhang value (recommended value: 0.1)",
                filename=False,
                incompatible=["culling_limit"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-best_hit_score_edge", "best_hit_score_edge"],
                "Best Hit algorithm score edge value (recommended value: 0.1)",
                filename=False,
                is_required=False,
                incompatible=["culling_limit"],
                default=None,
            ),
            _ContentArgument(
                ["-dbsize", "dbsize"],
                "Effective size of the database",
                filename=False,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-searchsp", "searchsp"],
                "Effective length of the search space",
                filename=False,
                checker_function=lambda x: x >= 0,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-import_search_strategy", "import_search_strategy"],
                "Search strategy file to read.",
                filename=True,
                incompatible=["export_search_strategy"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-export_search_strategy", "export_search_strategy"],
                "Record search strategy to this file.",
                filename=True,
                incompatible=["import_search_strategy"],
                is_required=False,
                default=None,
            ),
            _SwitchArgument(
                ["-parse_deflines", "parse_deflines"],
                "Parse query and subject bar delimited sequence identifiers "
                "(e.g., gi|129295).",
            ),
            _ContentArgument(
                ["-num_threads", "num_threads"],
                "Number of threads (CPUs) to use in blast search.",
                filename=None,
                checker_function=lambda x: x >= 1,
                incompatible=["remote"],
                is_required=False,
                default=1,
            ),
            _SwitchArgument(
                ["-remote", "remote"],
                "Execute search on NCBI servers?",
                incompatible=["gilist", "seqidlist", "negative_gilist",
                              "subject_loc", "num_threads"]
            ),
            _ContentArgument(
                ["-outfmt", "outfmt"],
                "Number of threads (CPUs) to use in blast search.",
                filename=None,
                is_required=False,
                default=0,
                allow_multiple=True,
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
        _BlastBaseCommandline.__init__(self, cmd, path_exec, **kwargs)


class BlastNCommandline(_BlastSearchBaseCommandline):
    """Base Commandline object for Blast wrappers (PRIVATE).
    This is provided for subclassing, it deals with shared options
    common to all the blast tools (blastn, etc).
    """

    def __init__(self, cmd="blastn", path_exec="", **kwargs):
        assert cmd is not None
        self.parameters = [
            _ContentArgument(
                ["-task", "task"],
                "Task to execute",
                filename=None,
                is_required=False,
                checker_function=lambda x: x in ["blastn", "blastn-short",
                                                 "dc-megablast", "megablast",
                                                 "rmblastn"],
                default="Megablast",
            ),
            _ContentArgument(
                ["-word_size", "word_size"],
                "Word size for wordfinder algorithm (length of best perfect "
                "match)",
                filename=None,
                is_required=False,
                checker_function=lambda x: x >= 4,
                default="Depends on task",
            ),
            _ContentArgument(
                ["-gapopen", "gapopen"],
                "Cost to open a gap.",
                filename=None,
                is_required=False,
                default="Depends on task",
            ),
            _ContentArgument(
                ["-gapextend", "gapextend"],
                "Word size for wordfinder algorithm (length of best perfect "
                "match)",
                filename=None,
                is_required=False,
                default="Depends on task",
            ),
            _ContentArgument(
                ["-reward", "reward"],
                "Reward for a nucleotide match.",
                filename=None,
                is_required=False,
                checker_function=lambda x: x >= 0,
                default="Depends on task",
            ),
            _ContentArgument(
                ["-penalty", "penalty"],
                "Penalty for a nucleotide mismatch.",
                filename=None,
                is_required=False,
                checker_function=lambda x: x <= 0,
                default="Depends on task",
            ),
            _ContentArgument(
                ["-strand", "strand"],
                "Query strand(s) to search against database/subject. Choice of"
                "both, minus, or plus.",
                filename=None,
                is_required=False,
                checker_function=lambda x: x in ["both", "minus", "plus"],
                default="both",
            ),
            _ContentArgument(
                ["-dust", "dust"],
                "Filter query sequence with dust.",
                filename=None,
                is_required=False,
                default="20 64 1",
            ),
            _ContentArgument(
                ["-filtering_db", "filtering_db"],
                "Mask query using the sequences in this database.",
                filename=None,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-window_masker_taxid", "window_masker_taxid"],
                "Enable WindowMasker filtering using a Taxonomic ID.",
                filename=None,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-sum_stats", "sum_stats"],
                "Use sum statistics.",
                filename=None,
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-window_masker_db", "window_masker_db"],
                "Enable WindowMasker filtering using this file.",
                filename=None,
                is_required=False,
                default=None,
            ),
            _SwitchArgument(
                ["-soft_masking", "soft_masking"],
                "Apply filtering locations as soft masks (i.e., only for "
                "finding initial matches).",
            ),
            _SwitchArgument(
                ["-lcase_masking", "lcase_masking"],
                "Use lower case filtering in query and subject sequence(s).",
            ),
            _ContentArgument(
                ["-db_soft_mask", "db_soft_mask"],
                "Filtering algorithm ID to apply to the BLAST database as soft"
                "mask (i.e., only for finding initial matches).",
                filename=None,
                incompatible=["db_hard_mask", "subject", "subject_loc"],
                is_required=False,
                default=True,
            ),
            _ContentArgument(
                ["-db_hard_mask", "db_hard_mask"],
                "Filtering algorithm ID to apply to the BLAST database as "
                "hard mask (i.e., sequence is masked for all phases of search)"
                ".",
                filename=None,
                incompatible=["db_hard_mask", "subject", "subject_loc"],
                is_required=False,
                default=None,
            ),
            _ContentArgument(
                ["-perc_identity", "perc_identity"],
                "Percent identity cutoff.",
                filename=None,
                is_required=False,
                default=0,
            ),
            _ContentArgument(
                ["-qcov_hsp_perc", "qcov_hsp_perc"],
                "Percent query coverage per hsp.",
                filename=None,
                is_required=False,
                default=0,
            ),
            _ContentArgument(
                ["-template_type", "template_type"],
                "Discontiguous MegaBLAST template type. Allowed values are "
                "coding, optimal and coding_and_optimal.",
                filename=None,
                is_required=False,
                checker_function=lambda x: x in ["coding",
                                                 "coding_and_optimal",
                                                 "optimal"],
                required_options=["template_length"],
                default=0,
            ),
            _ContentArgument(
                ["-template_length", "template_length"],
                "Discontiguous MegaBLAST template length.",
                filename=None,
                required_options=["template_length"],
                is_required=False,
                default=18,
            ),
            _ContentArgument(
                ["-use_index", "use_index"],
                "Use MegaBLAST database index. Indices may be created with the"
                " makembindex application.",
                filename=None,
                is_required=False,
                default=18,
            ),
            _ContentArgument(
                ["-index_name", "index_name"],
                "MegaBLAST database index name.",
                filename=None,
                is_required=False,
                default=18,
            ),
            _ContentArgument(
                ["-xdrop_ungap", "xdrop_ungap"],
                "Heuristic value (in bits) for ungapped extensions.",
                filename=None,
                is_required=False,
                default=20,
            ),
            _ContentArgument(
                ["-xdrop_gap", "xdrop_gap"],
                "Heuristic value (in bits) for preliminary gapped extensions.",
                filename=None,
                is_required=False,
                default=30,
            ),
            _ContentArgument(
                ["-xdrop_gap_final", "xdrop_gap_final"],
                "Heuristic value (in bits) for final gapped alignment.",
                filename=None,
                is_required=False,
                default=100,
            ),
            _SwitchArgument(
                ["-no_greedy", "no_greedy"],
                "Use non-greedy dynamic programming extension.",
            ),
            _ContentArgument(
                ["-min_raw_gapped_score", "min_raw_gapped_score"],
                "Minimum raw gapped score to keep an alignment in the "
                "preliminary gapped and trace-back stages. Normally set based "
                "upon expect value.",
                filename=None,
                is_required=False,
                default=30,
            ),
            _SwitchArgument(
                ["-ungapped", "ungapped"],
                "Perform ungapped alignment.",
            ),
            _ContentArgument(
                ["-window_size", "window_size"],
                "Multiple hits window size, use 0 to specify 1-hit algorithm.",
                filename=None,
                is_required=False,
                default=40,
                checker_function=lambda x: x >= 0,
            ),
            _ContentArgument(
                ["-off_diagonal_range", "off_diagonal_range"],
                "Number of off-diagonals to search for the 2nd hit, use 0 to "
                "turn off",
                filename=None,
                is_required=False,
                default=40,
                checker_function=lambda x: x >= 0,
            ),
            _ContentArgument(
                ["-line_length", "line_length"],
                "Line length for formatting alignments. Not applicable for "
                "outfmt > 4",
                filename=None,
                is_required=False,
                default=60,
                checker_function=lambda x: x >= 1,
            ),
        ]
        _BlastSearchBaseCommandline.__init__(self, cmd, path_exec, **kwargs)
