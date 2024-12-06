from .config import Config
from .handling_args import CGEArgumnents


def collect_args(argv):
    ArgumentHandler = CGEArgumnents(program_description="test")
    version = "1.0.0"
    ArgumentHandler.fasta_input()
    ArgumentHandler.fastq_input()
    ArgumentHandler.output_path()
    ArgumentHandler.output_json()
    ArgumentHandler.nanopore()
    ArgumentHandler.blast_path()
    ArgumentHandler.kma_path()
    ArgumentHandler.species()
    ArgumentHandler.ignore_missing_species()
    ArgumentHandler.add_alignments_to_json()
    ArgumentHandler.add_database_res_arg()
    ArgumentHandler.add_database_res_kma_arg()
    ArgumentHandler.add_database_disinf_arg()
    ArgumentHandler.add_database_disinf_kma_arg()
    ArgumentHandler.add_database_point_arg()
    ArgumentHandler.add_database_point_kma_arg()
    ArgumentHandler.add_overlap_arg()
    ArgumentHandler.add_min_cov_arg()
    ArgumentHandler.add_threshold_arg()
    ArgumentHandler.add_disinfectant_arg()
    ArgumentHandler.add_chromosomal_arg()
    ArgumentHandler.add_specific_gene_arg()
    ArgumentHandler.add_unknown_mut_arg()
    ArgumentHandler.add_min_cov_point_arg()
    ArgumentHandler.add_threshold_point_arg()
    ArgumentHandler.add_ignore_indels_arg()
    ArgumentHandler.add_ignore_stop_codons_arg()
    ArgumentHandler.add_version_arg(version = version)
    ArgumentHandler.add_pickle_arg()
    parser = ArgumentHandler.parser
    args = parser.parse_args(argv)
    return args

def collect_point(argv):
    ArgumentHandler = CGEArgumnents(program_description="test",)
    version = "1.0.0"
    ArgumentHandler.fasta_input()
    ArgumentHandler.output_path()
    ArgumentHandler.add_database_point_arg()
    ArgumentHandler.add_database_point_kma_arg()
    ArgumentHandler.species()
    parser = ArgumentHandler.parser
    args = parser.parse_args(argv)
    return args
    
    
def test_config():
    args = collect_args(["--inputfasta",
                         "/home/people/s220672/resfinder/tests/data/test_isolate_01.fa",
                         "-o", ".",
                         "--db_res", "/home/people/s220672/databases/resfinder_db"])
    Config(args, "resfinder", ".")
    args = collect_args(["--inputfastq", "/home/people/s220672/resfinder/tests/data/test_isolate_05_1.fq",
                         "-o", ".",
                         "--db_res", "/home/people/s220672/databases/resfinder_db"])
    Config(args, "resfinder", ".")
    args = collect_args(["--inputfastq","/home/people/s220672/resfinder/tests/data/test_isolate_05_1.fq",
                         "/home/people/s220672/resfinder/tests/data/test_isolate_05_2.fq",
                        "-o", ".",
                        "--db_res", "/home/people/s220672/databases/resfinder_db"])
    Config(args, "resfinder", ".")
    args = collect_args(["--inputfasta",
                         "/home/people/s220672/resfinder/tests/data/test_isolate_01.fa",
                         "-o", ".",
                         "--db_res", "/home/people/s220672/databases/resfinder_db",
                         "--point",
                         "--db_point", "/home/people/s220672/databases/pointfinder_db",
                         "--species", "ecoli"])
    conf = Config(args, "resfinder", ".")
    conf.check_point_settings()
    args= collect_args(["--inputfasta",
                         "/home/people/s220672/resfinder/tests/data/test_isolate_01.fa",
                         "-o", ".",
                         "--db_res", "/home/people/s220672/databases/resfinder_db",
                         "--disinfectant",
                         "--db_disinf", "/home/people/s220672/databases/disinfinder_db",])
    conf = Config(args, "resfinder", ".")
    # Check if Config also works with reduced number of arguments (given trhough collect_point)
    args = collect_point(["--inputfasta", "/home/people/s220672/resfinder/tests/data/test_isolate_01.fa",
                          "--db_point", "/home/people/s220672/databases/pointfinder_db",
                          "--species", "ecoli",
                          "-o", "."])
    conf = Config(args, "pointfinder", ".")