
import os
import sys
import warnings
from .pointfinder import PointFinder
import subprocess
from cgecore.utils.loaders_mixin import LoadersMixin
import glob

class Config:

    def __init__(self, args, program_name = "resfinder"):
        """
        :param parser: The parser object from CGEArguments
        :param program_name: The name of the program you are running
        :param program_root: The root of the program you are running. The root directory is before src/
        """
        
        self.program_root = self.get_resfinder_parent_dir(program_name)
        # all possible args contains all args from the class CGEArguments
        all_possible_args = {"inputfasta": self.check_input_files, # called as general option
                            "inputfastq": self.check_input_files, # called as general option
                            "nanopore": None, # happens in check_fastq
                            "output_path": self.check_output_path, # called as general option
                            "out_json": self.check_json, # called as general option
                            "blastPath": self.set_blastPath, # happens in check_fasta
                            "kmaPath": self.set_kmaPath, # happens in check_fastq
                            "species": None, # belongs to check_get_species but needs to be called spearately
                            "ignore_missing_species": None, # not part of final Config object
                            "output_aln": self.set_output_aln, # called as general opts
                            "db_res": self.check_db_res,
                            "db_res_kma": None, # happens in check_db_res
                            "db_disinf": self.check_db_disinf, # called if disinfinder is True or software name is is not resfinder
                            "db_disinf_kma": None, # happens in check_db_disinf
                            "db_point": None, # call this separately with check_point_settings when class instance has been called
                            "db_point_kma": None, # in original class never called. Maybe needs to be removed ?!
                            "acq_overlap": self.set_acq_overlap, 
                            "min_cov": self.check_min_cov_res, 
                            "threshold": self.check_threshold_res,
                            "disinfectant": self.set_disinf, # called as general opts      
                            "specific_gene": self.set_specific_gene, 
                            "unknown_mut": self.set_unknown_mut,             
                            "ignore_indels": self.set_ignore_indels,
                            "ignore_stop_codons": self.set_ignore_stop_codons,
                            "version": None,
                            "pickle": self.set_pickle, # called as general opts
                            "db_path": self.check_db_path_custom,
                            }
        
        self.ENV_VAR_FILENAME = os.path.join(os.path.dirname(__file__), "markdown_documents/environment_variables.md")
        self.SPECIES_ABBR_FILENAME = os.path.join(os.path.dirname(__file__), "markdown_documents/species_abbreviations.md")
        self.AMR_ABBR_FILENAME = os.path.join(os.path.dirname(__file__), "markdown_documents/amr_abbreviations.md")
        # in program_args are only the program specific arguments, this is important to distinguish from all_possible_args to know which kind of test dependencies you have. 
        # For instance if you run blast that you need to check for the databse for resfinder etc.        
        self.program_name = program_name
        self.args = args
        keys_all = set(all_possible_args.keys())
        self.keys_program = set(vars(self.args).keys())
        
        # perform inner merge of keys to allow to inherit this class in a program specific config class where certain things are build on top of this class
        # this allows to not always have to update the cgecore package when a new tool is created
        common_keys = keys_all.intersection(self.keys_program)
        result_dict = {key: all_possible_args[key] for key in common_keys}


        # sets the attributes of the Config class
        for key, method in result_dict.items():
            if method is not None and callable(method):
                method()
                
        # resfinder specific run
        if self.program_name == "resfinder":
            self.set_phenotype_opts()
            self.set_amr_abbreviations()
            self.check_point_settings()

        #sets dynamically the attribute for the program root in the class, so that conf.resfinder_root or conf.plasmidfinder_root is possible
        setattr(self, f"{self.program_name}_root", self.program_root)
        
    @staticmethod
    def check_indexed(path:str):
        if len(glob.glob(path + "*.comp.b")) > 0:
            pass
        else:
            Warning(f"Database file {path + '*.comp.b'} not found.")
            return False            
        if len(glob.glob(path + "*.length.b")) > 0:
            pass
        else:
            Warning(f"Database file {path + '*.length.b'} not found.")
            return False
        if len(glob.glob(path + "*.name")) >0:
            pass
        else:
            Warning(f"Database file {path + '*.name'} not found.")
            return False
        if len(glob.glob(path + "*.seq.b")) > 0:
            pass
        else:
            Warning(f"Database file {path + '*.seq.b'} not found. No Analysis will be conducted")
            return False
        return True
    
    def check_db_path_custom(self):
        db_path = getattr(self.args, "db_path")
        if self.args.inputfasta is None:
            if hasattr(self.args, "species"):
                if type(self.args.species) == list:
                    pass
                else:
                    self.args.species = [self.args.species]
                for species in self.args.species:
                    pot_db_path = os.path.join(db_path, species)
                    if os.path.dirname(pot_db_path) == species:
                        pot_db_path = db_path 
                    else:
                        pass
                    if pot_db_path.endswith("/"):
                        pass
                    else:
                        pot_db_path = pot_db_path + "/"
                    if self.check_indexed(pot_db_path) == True:
                        db_path = pot_db_path
                    else:
                        raise LookupError("The database path is not indexed")
            else: # when species is included in db_path
                if os.path.isdir(db_path):
                    if db_path.endswith("/"):
                        pass
                    else:
                        db_path = db_path + "/"
                else:
                    db_path = os.path.dirname(db_path)
                if self.check_indexed(db_path):
                    db_path = db_path
                else:
                    raise LookupError("The database path is not indexed")
        elif self.args.inputfastq == []:
            if hasattr(self.args, "species"):
                if type(self.args.species) == list:
                    pass
                else:
                    self.args.species = [self.args.species]
                for species in self.args.species:
                    pot_db_path = os.path.join(db_path, species)
                    if os.path.dirname(pot_db_path) == species:
                        pot_db_path = db_path
                    else:
                        pass
                    if pot_db_path.endswith("/"):
                        pass
                    else:
                        pot_db_path = pot_db_path + "/"
                    if os.path.isfile(os.path.join(pot_db_path, species + ".fsa")):
                        db_path = pot_db_path
                    elif os.path.isfile(os.path.join(pot_db_path, species + ".fna")):
                        db_path = pot_db_path
                    else:
                        raise FileNotFoundError("The database .fna path does not exist.")
            else: # when species is included in db_path
                if os.path.isdir(db_path):
                    if db_path.endswith("/"):
                        pass
                    else:
                        db_path = db_path + "/"
                else:
                    db_path = os.path.dirname(db_path)
                db_path = glob.glob(db_path + "*.fna")[0]
                if os.path.isfile(db_path):
                    db_path = db_path
                else:
                    raise FileNotFoundError("The database .fna path does not exist.")
        else:
            raise SystemError("No files to be analysed were provided.")
        self.db_path = db_path
        
    @staticmethod
    def get_resfinder_parent_dir(program_name):
        
        path = __file__
        while True:
            path = os.path.dirname(path)
            if os.path.isdir(os.path.join(path, program_name)):
                break
            elif path == "/":
                sys.exit(f"ERROR: Could not locate the root directory of "
                         "{program_name}.")
        return path
        
    def set_environment_variables(self):
        assert os.path.isfile(self.ENV_VAR_FILENAME)
        self.set_default_and_env_vals(self.args, self.ENV_VAR_FILENAME)
        
    def set_amr_abbreviations(self ):
        self.AMR_ABBR_FILENAME = os.path.abspath(self.AMR_ABBR_FILENAME)
        self.amr_abbreviations = LoadersMixin.load_md_table_after_keyword(
            self.AMR_ABBR_FILENAME, "## Abbreviations")
    
    @staticmethod
    def get_abs_path_and_check(path, allow_exit=True):
        abs_path = os.path.abspath(path)
        if(not os.path.isfile(abs_path) and not os.path.isdir(abs_path)):
            if(allow_exit):
                sys.exit("ERROR: Path not found: {}".format(path))
            else:
                raise FileNotFoundError
        return abs_path

    def check_root_of_path(self, path):
        if os.path.isdir(path):
            assert os.path.exists(os.path.dirname(path)), "The root of the path to your directory does not exist"
        elif os.path.isfile(path):
            pass
        
    @staticmethod
    def check_input_range_float(number, arg_name):
        if number != None:            
            if number < 0.0 or number > 1.0:
                sys.exit(f"ERROR: {arg_name} above 1 or below 0 is not "
                        "allowed. Please select a value within the "
                        "range 0-1 with the flag -l. Given value: {}."
                        .format(number))
                
    def check_min_cov(self, value):
        if type(value) == float or type(value) == int: 
            value = float(value)
            self.check_input_range_float(value, "min_cov")
        else:
            sys.exit("ERROR: The min_cov is not a float or an integer.")
        return value
    
    def check_min_cov_res(self, ):
        if self.args.min_cov is None:
            self.args.min_cov = 0.6
        else:
            pass
        self.min_cov = self.check_min_cov(self.args.min_cov)
        self.dis_gene_cov = self.args.min_cov
        self.rf_gene_cov = self.args.min_cov
        self.pf_gene_cov = 0.01
        self.min_cov_point = self.args.min_cov
        

    def check_threshold(self, threshold, name_of_arg):
        if type(threshold) == float or type(threshold) == int: 
            threshold = float(threshold)
            self.check_input_range_float(threshold, name_of_arg)
        else:
            sys.exit("ERROR: The threshold is not a float or an integer.")
        return threshold
    
    def check_threshold_res(self):
        # NOTE: It is weird that disinfinder and resfinder have the same value in the end while pointfinder has its own flag
        if self.args.threshold is None:
            self.args.threshold = 0.8
        else:
            pass
        self.args.threshold = self.check_threshold(self.args.threshold, "threshold_resfinder")
        self.dis_gene_id = self.args.threshold
        self.rf_gene_id = self.args.threshold
        self.pf_gene_id = self.args.threshold
        
    
    def set_unknown_mut(self):
        self.unknown_mut = self.args.unknown_mut
        
    def set_output_aln(self):
        self.output_aln = bool(self.args.output_aln)
    
    def set_pickle(self):
        self.pickle = self.args.pickle
    
    def set_ignore_indels(self):
        self.ignore_indels = self.args.ignore_indels
    
    def set_ignore_stop_codons(self):
        self.ignore_stop_codons = self.args.ignore_stop_codons
   
    def set_acq_overlap(self):
        if self.args.acq_overlap is None:
            self.args.acq_overlap = 30
        self.rf_overlap = int(self.args.acq_overlap)
        self.pf_overlap = int(self.args.acq_overlap)

       
    def set_specific_gene(self):
        self.specific_gene = self.args.specific_gene
        
                
    def set_blastPath(self):
        if self.args.blastPath == None:
            self.args.blastPath = "blastn"
        else:
            self.args.blastPath = self.args.blastPath
            
    def set_kmaPath(self):
        if self.args.kmaPath == None:
            self.args.kmaPath = "kma"
        else: 
            pass
    
    def set_disinf(self):
        self.disinf = bool(self.args.disinfectant)
        
    def check_json(self):
        if self.args.out_json:
            if not self.args.out_json.endswith(".json"):
                sys.exit("Please specify the path to the JSON file including "
                         "its filename ending with .json.\n")
            self.out_json = os.path.abspath(self.args.out_json)
            os.makedirs(os.path.dirname(self.out_json), exist_ok=True)
        else:
            self.out_json = None
            
    def check_output_path(self):
        if self.args.output_path is not None:
            self.outputPath = os.path.abspath(self.args.output_path)
            os.makedirs(self.outputPath, exist_ok=True)
        else:
            warnings.warn("Output Path is NoneType. This warning appears if you have set the argument to be not required and the user inputs no value here. Be aware that some other arguments may depend on this.")
    
    @staticmethod
    def get_species(in_species, species_def_filepath):
        out_species = in_species
        if(in_species is not None and in_species.lower() == "other"):
            out_species = "other"
        elif(in_species is not None):
            out_species = in_species.lower()

        species_transl = LoadersMixin.load_md_table_after_keyword(
            species_def_filepath, "## Species Abbreviations Table",
            header_key="Abbreviation")

        fixed_species = species_transl.get(out_species, None)
        if(fixed_species):
            out_species = fixed_species[0]

        return out_species
        
    def check_get_species(self):        
        self.species = self.get_species(self.args.species, self.SPECIES_ABBR_FILENAME)
        

    def check_fasta(self):
        self.inputfastq = None

        self.inputfasta = self.get_abs_path_and_check(path = self.args.inputfasta, allow_exit=True)
        if "db_point" in self.keys_program:
            self.outPath_point_blast = ("{}/pointfinder_blast"
                            .format(self.args.output_path))
            os.makedirs(self.outPath_point_blast, exist_ok=True)
            self.method = PointFinder.TYPE_BLAST # maybe remove because of import
            
        if "db_disinf" in self.keys_program:
            self.outPath_disinf_blast = ("{}/disinfinder_blast"
                            .format(self.args.output_path))
            os.makedirs(self.outPath_disinf_blast, exist_ok=True)
        if "db_res" in self.keys_program:
            self.outPath_res_blast = ("{}/resfinder_blast"
                            .format(self.args.output_path))
            os.makedirs(self.outPath_res_blast, exist_ok=True)
        else: # if non of the above is TRUE then create the direcotry for the program -> You can then use this functionality for other programs
            self.outPath_blast = "{}/" + f"{self.program_name}" + "_blast".format(self.args.output_path)
            os.makedirs(self.outPath_blast, exist_ok=True)
        
        self.sample_name = os.path.basename(self.inputfasta)
        if "blastPath" in self.args:
            self.set_blastPath()
            self.blast = self.get_prg_path(self.args.blastPath)
        self.kma = None
        
    
    def check_fastq(self):
        self.inputfasta = None
        self.inputfastq_1 = self.get_abs_path_and_check(
            self.args.inputfastq[0])
        if(len(self.args.inputfastq) == 2):
            self.inputfastq_2 = self.get_abs_path_and_check(
                self.args.inputfastq[1])
            
        elif(len(self.args.inputfastq) > 2):
            sys.exit("ERROR: More than 2 files were provided to inputfastq: "
                     "{}.".format(self.args.inputfastq))
        else:
            self.inputfastq_2 = None
        
        if "db_point" in self.keys_program:
            self.outPath_point_kma = "{}/pointfinder_kma".format(self.args.output_path)
            os.makedirs(self.outPath_point_kma, exist_ok=True)
            self.method = PointFinder.TYPE_KMA
            
        if "db_disinf" in self.keys_program:
            self.outPath_disinf_kma = "{}/disinfinder_kma".format(self.args.output_path)
            os.makedirs(self.outPath_disinf_kma, exist_ok=True)    
        
        if "db_res" in self.keys_program:
            self.outPath_res_kma = "{}/resfinder_kma".format(self.args.output_path)
            os.makedirs(self.outPath_res_kma, exist_ok=True)
        
        else: # if non of the above is TRUE then create the direcotry for the program -> You can then use this functionality for other programs
            self.outPath_kma = "{}/" + f"{self.program_name}" + "_kma".format(self.args.output_path)
            os.makedirs(self.outPath_kma, exist_ok=True)
            
        self.sample_name = os.path.basename(self.args.inputfastq[0])
        if "kmaPath" in self.args:
            self.set_kmaPath()
            self.kma = self.get_prg_path(self.args.kmaPath)
        if "nanopore" in self.keys_program:
            self.nanopore = self.args.nanopore  
        
    def check_input_files(self,):
        inputfasta = self.args.inputfasta
        if "inputfastq" in self.keys_program:
            inputfastq = self.args.inputfastq
        else: # in case that no inputfastq is provided in program arguments
            if inputfasta != None:
                inputfastq = None
                self.check_fasta()
                return
            else:
                sys.exit("ERROR: Please provide either a FASTA file or FASTQ "
                         "files.")  
        if  len(inputfastq) == 0 and inputfasta == None:
            sys.exit("ERROR: Please provide either a FASTA file or FASTQ "
                     "files.")
        if inputfasta != None and len(inputfastq) > 0:
            sys.exit("ERROR: Please provide either a FASTA file or FASTQ "
                     "files, not both.")
        if inputfasta != None:
            self.check_fasta()
        else:
            self.check_fastq()
    
    @staticmethod
    def check_db(file, basename):
        path = os.path.join(file, basename)
        isfile = os.path.isfile(path)
        if not isfile:
            sys.exit(f"Input Error: The database {basename} file could not be found"
                     " in the database directory.")
        return path

    def check_path_db(self,db_path ,program_name, *conditions):
        if db_path is None:
            db_path = "{}{}".format(self.program_root,
                                    f"/databases/{program_name}_db")
        else:
            pass
        try:
            db_path = self.get_abs_path_and_check(
                db_path, allow_exit=False)
        except FileNotFoundError:
            if all(conditions):
                sys.exit("Could not locate " + program_name + " database path: {}"
                        .format(db_path)) 
        return db_path      
    
    
    def check_path_db_kma(self,db_path, db_path_kma, *conditions):
        if db_path_kma is None:
            db_path_kma = db_path
        try:
            db_path_kma = os.path.abspath(db_path_kma)
            db_path_kma = self.get_abs_path_and_check(
                path = db_path_kma, allow_exit=False)
        except FileNotFoundError:
            if all(conditions):
                sys.exit("Could not locate DisinFinder database index path: {}"
                         .format(db_path_kma))
            else:
                pass
        return db_path_kma
    
    
    def check_db_res(self):
        self.db_path_res = self.check_path_db(self.args.db_res, "resfinder")
        if len(self.args.inputfastq) == 0:
            inputfastq = None
        else:
            inputfastq = self.args.inputfastq[0]
        self.db_path_res_kma = self.check_path_db_kma(self.db_path_res,
                                                        self.args.db_res_kma,
                                                       inputfastq)
        for basename in ["config", "notes.txt", "phenotype_panels.txt"]:
            path = self.check_db(self.db_path_res, basename)
            if basename != "phenotype_panels.txt":
                basename = basename.split(".")[0]
                setattr(self, f"db_{basename}_file", path)
            else:
                self.db_panels_file = path
        
        
    def check_db_disinf(self):
        self.set_disinf()
        if self.args.disinfectant or self.program_name == "resfinder":
            self.db_path_disinf = self.check_path_db(self.args.db_disinf, "disinfinder")
            if len(self.args.inputfastq) == 0:
                inputfastq = None
            else:
                inputfastq = self.args.inputfastq[0]
            self.db_path_disinf_kma = self.check_path_db_kma(self.db_path_disinf,
                                                            self.args.db_disinf_kma,
                                                            self.args.disinfectant, inputfastq)
            for basename in ["config", "notes.txt",]:
                self.check_db(self.db_path_disinf, basename)
        else: 
            pass
            
        if(self.disinf or self.program_name != "resfinder"):
            self.disinf_file = ("{}/phenotypes.txt".format(self.db_path_disinf)
                                )
            _ = self.get_abs_path_and_check(self.disinf_file)

            self.disclassdef_file = ("{}/disinfectant_classes.txt"
                                     .format(self.db_path_disinf))
            _ = self.get_abs_path_and_check(self.disclassdef_file)
        else:
            self.disinf_file = None
            self.disclassdef_file = None
            
        
        
    def _parse_species_dir(self, path_pointdb, species_dir,
                           ignore_missing_species):
        # Check if a database for species exists
        point_dbs = PointFinder.get_db_names(path_pointdb)
        if(species_dir not in point_dbs):
            # If no db for species is found check if db for genus is found
            # and use that instead
            tmp_list = self.species.split()
            if(tmp_list[0] in point_dbs):
                species_dir = tmp_list[0]
            elif(ignore_missing_species):
                self.species = None
                self.db_path_point_root = None
                self.db_path_point = None
                species_dir = None
            else:
                sys.exit("ERROR: species '{}' ({}) does not seem to exist"
                         " as a PointFinder database."
                         .format(self.species, species_dir))
        else:
            pass
        return species_dir    
    
        
    def set_path_pointdb(self):
        tmp_list = self.species.split()
        if(len(tmp_list) != 1 and len(tmp_list) != 2):
            sys.exit("ERROR: Species name must contain 1 or 2 names. Given "
                     "value: {}".format(self.species))

        if(len(tmp_list) == 2):
            tmp_species_dir = "_".join(tmp_list)
        else:
            tmp_species_dir = tmp_list[0]
        
        self.args.db_point = self.check_path_db(self.args.db_point, "pointfinder")

        path_pointdb = os.path.abspath(self.args.db_point)

        self.species_dir = self._parse_species_dir(path_pointdb,
                                                   tmp_species_dir,
                                                   self.args.ignore_missing_species)

        if(self.species_dir is not None):
            self.db_path_point_root = path_pointdb

            self.db_path_point = "{}/{}".format(path_pointdb, self.species_dir)
        else:
            self.db_path_point = None
        
        self.db_path_point_kma = self.db_path_point
        
    def check_point_settings(self, ):
        self.check_get_species()
        if(not self.species and not self.args.ignore_missing_species):
            sys.exit("ERROR: Chromosomal point mutations cannot be located if "
                     "no species has been provided. Please provide species "
                     "using the --species option.")
        elif((not self.species and self.args.ignore_missing_species)
                or self.species.lower() == 'other'):
            self.species = None
            
            self.db_path_point = None
            
            return

        self.set_path_pointdb()

        
        if self.db_path_point:
            if os.path.exists("{}/phenotypes.txt"
                                .format(self.db_path_point)):
                self.point_phenotypes_new = ("{}/phenotypes.txt"
                                    .format(self.db_path_point))
                _ = self.get_abs_path_and_check(self.point_phenotypes_new)
                if _:
                    return
            if os.path.exists("{}/resistens-overview.txt"
                                .format(self.db_path_point)):
                self.point_phenotypes_old = ("{}/resistens-overview.txt"
                                    .format(self.db_path_point))
                _ = self.get_abs_path_and_check(self.point_phenotypes_old)
            else:
                sys.exit("Error: The pointfinder database does not have the "
                            "'phenotypes.txt' file (new database) neither the "
                            "'resistens-overview.txt' file (old database)")
        
    def get_prg_path(self,prg_path):
        try:
            prg_path = self.get_abs_path_and_check(prg_path,
                                                     allow_exit=False)
        except FileNotFoundError:
            pass

        try:
            _ = subprocess.check_output([prg_path, "-h"])
        except PermissionError:
            sys.exit("ERROR: Missing permission. Unable to execute app from"
                     " the path: {}".format(prg_path))
        return prg_path


    def set_phenotype_opts(self):
        self.point_file = None
        
        self.check_db_res()

        self.db_panels_file = f"{self.db_path_res}/phenotype_panels.txt"
        _ = self.get_abs_path_and_check(self.db_panels_file)

        self.abclassdef_file = f"{self.db_path_res}/antibiotic_classes.txt"
        _ = self.get_abs_path_and_check(self.abclassdef_file)
        

        self.phenotype_file = ("{}/phenotypes.txt"
                                .format(self.db_path_res))
        _ = self.get_abs_path_and_check(self.phenotype_file)


    
            
            
