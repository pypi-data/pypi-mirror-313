
# in the end you should just take the two outputs and summarise it as one 
# you need and object which shows the final gene - if there is a gap maybe insert - ?
# the query string should be merged 

import pandas as pd
import numpy as np
# identifier: contig (test_isolate_01); gene; position 
# everything up to first underscore needs to match because blaB-2 or blaB-3 can still be the same gene due to noise and variacne 
# 
# loop over each dictionary for instance the dic from beta-lactam


# different contigs must be possible!!! check
# for gene split between two different contigs you must calc the coverage and then compare with threshold. check 
# report whiche gene was found in which contig and in which position 
# for only one gene 

class MergeGenes:
    def __init__(self) -> None:
        self.contig_names = []
        self.sbjct_headers = []
        self.coverage = []
        self.identity = []
        self.start_merge=  None
        self.end_merge = None
        self.merged_sequence = ""
        
    def calc_identity(self, start_points:list, end_points:list):
        """This function calculates the normalized identity of the merged sequence. It takes the sequences from the different contigs and weights them based on their proportion in the merged sequences. 
            After that this is multiplied by the sequence's identity value. Finally all of these are summed up.

        Args:
            start_points (list): Contains the start points of each sequence in the query sequence
            end_points (list): Contains the end points of each sequence in the query sequence

        Returns:
            int: Normalized identity for the merged sequence.
        """
        # does not work like this because if you have an overlap and sequence 2 has id of 80 but where the identity is low the overlap happens then you should have 100 percent identity anyway because you will take gene 1 for that part
        assert len(self.coverage) >= 1
        assert len(self.identity) >= 1, "You must have identity values here to run this method."
        gap_count = self.merged_sequence.count("-")
        normed_identity = 0
        len_seq = len(self.merged_sequence)
        add_to_denuminator = 0
        length_sequences = []
        identity_genes = []
        for index, start in enumerate(start_points):
            end_i = end_points[index]
            if index != 0:
                end_i_past = end_points[index-1]
                
            else:
                end_i_past = 0
            if end_i_past > start: # overlap and fulls first sequence of two sequences will always be taken for merge
                diff = end_i_past - start
                start = start + diff
            elif end_i_past < start - 1: #This case happens when there is a gap. minus one because +1 position after end_i_past would be perfect alignment
                diff = start - end_i_past - 1 
                add_to_denuminator += diff # it sees that there is a gap and adds the difference to this variable
                diff_seq = end_i - start + 1
                self.identity[index] = (self.identity[index] / 100 - diff/diff_seq ) * 100
            else: 
                pass
            len_i = end_i - start  + 1
            length_sequences.append(len_i) 
            identity_genes.append(self.identity[index] /100)
        identity_genes = np.array(identity_genes)
        length_sequences = np.array(length_sequences)
        length_whole_seqeunce = end_points[-1] - start_points[0]+ 1
        vector = length_sequences / length_whole_seqeunce *identity_genes
        normed_identity = np.sum(vector) # calc proportion of single sequences on whole sequence and multiply by corresponding identity
        return normed_identity

        
            
    
    def collect_gene_objects(self, common_gene_df:pd.DataFrame, seq_no:int):
        seq_no -=1
        contig_gene = common_gene_df.iloc[common_gene_df.index.get_loc("contig_name"), seq_no]
        contig_name = contig_gene.split(" ")[0]
        self.contig_names.append(contig_name)
        self.sbjct_headers.append(common_gene_df.iloc[common_gene_df.index.get_loc("sbjct_header"), seq_no])
        self.coverage.append(common_gene_df.iloc[common_gene_df.index.get_loc("coverage"), seq_no])
        self.identity.append(common_gene_df.iloc[common_gene_df.index.get_loc("perc_ident"), seq_no])
        
    def merge_sequence(self, common_gene_df:pd.DataFrame):
        """
        common_gene_df (pd.DataFrame): This object is the value of any resistance category as pandas dataframe. So the headers are the gene/contig labels and the rows are the results for each gene from blast. If you have three genes there you will have three columns in the pandas dataframe
        """
        assert isinstance(common_gene_df, pd.DataFrame), "input must be a pandas dataframe"
        start_points = common_gene_df.loc["query_start"].to_list()
        end_points = common_gene_df.loc["query_end"].to_list()

        merged_seq = ""
        self.start_merge = start_points[0]
        self.end_merge = end_points[-1]
        seq_no = 0 #seq_no is index of current sequence to put it correctly in the merged sequence
        for start in start_points:
            index_end = start_points.index(start) # index in list with start points
            if index_end -1 >= 0:
                end = end_points[index_end - 1]
                if end >= start: # overlap between seq 2 and seq1
                    trim = end  - start +1
                    merged_seq += common_gene_df.iloc[common_gene_df.index.get_loc("query_string"), seq_no][trim:] 
                    
                elif end < start -1: 
                    add_dash = start - 1  - end
                    merged_seq += add_dash * "-" + common_gene_df.iloc[common_gene_df.index.get_loc("query_string"), seq_no]
            else: # for the first sequence input
                merged_seq += common_gene_df.iloc[common_gene_df.index.get_loc("query_string"), seq_no]
            seq_no += 1
            self.collect_gene_objects(common_gene_df, seq_no)
        self.merged_sequence = merged_seq
        return merged_seq, start_points, end_points
                    


class FindCommonRegion:
    def __init__(self, result_AF):
        """
        result_AF (dict): Is the result object which contains the resistance categories with the corresponding dictionaries for the genes and the BLAST results
        return: Creates a similar object like result_AF where the resistance categories are the major keys and with the corresponding values which are dictionaries of merged or non merged sequences or a string like: No hit found.
        """
        self.result_AF = result_AF
        self.merged_seq_region = {}
        

    
    def make_merge_dic(self, common_gene_df: pd.DataFrame):
        """
        return: creates the result object with the merged sequences.
        """
        merged_dic = {}
        Merger = MergeGenes()
        merged_seq, start_points, end_points=  Merger.merge_sequence(common_gene_df)
        merged_dic["query_string"] = merged_seq   
        merged_dic["query_start"] = Merger.start_merge
        merged_dic["query_end"] = Merger.end_merge
        merged_dic["identity"] = None # this allows to select certain genes with dbhit
        contig_info = {}
        for index, name in enumerate(Merger.sbjct_headers):
            inner_dict = {}
            inner_dict["query_start"] = start_points[index] 
            inner_dict["query_end"] = end_points[index] 
            inner_dict["coverage"] = Merger.coverage[index]
            inner_dict["perc_ident"] = Merger.identity[index]
            inner_dict["gene"] = Merger.sbjct_headers[index]
            
            
            contig_info[name] = inner_dict
        normed_identity = Merger.calc_identity(start_points, end_points)
        merged_dic["gene_origin"] = contig_info
        merged_dic["identity"] = normed_identity
        return merged_dic
        
        
    def analyse_res_catg(self, res_catg:pd.DataFrame):
        gene_headers = res_catg.columns.to_list()
        gene_headers_split = [] # the headers until the first underscore after the first space in the string will be taken.
        merged_inner_dic = {}
        for header in gene_headers:
            split_string = header.split() # split by space
            gene_name = split_string[1].split('-')[0]
            gene_headers_split.append(gene_name)

        for header in gene_headers_split:
            filtered_columns = [col for col in gene_headers if header in col]
            
            if len(filtered_columns) > 1:
                common_gene_df = res_catg[filtered_columns]
    
                sorted_genes = common_gene_df.sort_values(by = "query_start", axis = 1) # crucical for the algoritm because the columns are anaylsed in a loop
                merged_inner_dic[header] = self.make_merge_dic(sorted_genes)
            else: # if no match is found just add everything to the merged_seq_region 
                values = res_catg[filtered_columns[0]].to_dict()
                merged_inner_dic[header] = values
        
        return merged_inner_dic
            
    def merged_query_string(self):
        """
        initializes the loop over the result object from point or aquired finder and goes over each category (key) inside the object.
        Fills the class object merged_seq_region with the merged and unmerged sequences
        """
        for key, value in self.result_AF.items(): # loops over each resistance categoru
            if type(value) == dict: # If there are no genes found the corresponding category is skipped
                if len(value)>=1:
                    res_catg = pd.DataFrame(data = self.result_AF[key])
                    inner_dic = self.analyse_res_catg(res_catg)
                    self.merged_seq_region[key] = inner_dic
                else:
                    self.merged_seq_region[key] = {}
            else:
                pass
            
#test_A1 = {"beta-lactam": {
 #                          "abcdefg sdf-3_jkle2kdsfjksldfka": {"query_string": "AAB", "sbjct_string": "AAB", "query_end": 7, "query_start": 5, "contig_name": "abcdefg", "sbjct_header": "sdf-3_jkle2kdsfjksldfka", "perc_ident":100.0, "coverage": 100.0},
  #                         "fffffff fff-3_jkle2kdsfjksldfka": {"query_string": "CCC", "sbjct_string": "CCC", "query_end": 3, "query_start": 1, "contig_name": "abcdefg", "sbjct_header": "sdf-3_jkle2kdsfjksldfka", "perc_ident": 50.0, "coverage": 100.0},
   #                        "abcdefg sdf-1_jkle2kdsfjksldfka": {"query_string": "EEE", "sbjct_string": "AAA", "query_end": 8, "query_start": 6, "contig_name": "abcdefg", "sbjct_header": "sdf-1_jkle2kdsfjksldfka", "perc_ident": 75.0, "coverage": 100.0},
    #                       "abcdefg sdf-2_jkle2kdsfjksldfka": {"query_string": "AAA", "sbjct_string": "AAA", "query_end": 3, "query_start": 1, "contig_name": "abcdefg", "sbjct_header": "sdf-2_jkle2kdsfjksldfka", "perc_ident": 90.0, "coverage": 100.0},}}
#A = FindCommonRegion(test_A1)
#A.merged_query_string()
#print(A.merged_seq_region)