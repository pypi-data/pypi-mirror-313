# Application sub module documentation

Submodule dedicated to run applications/executables used in the software of the CGE tools.

## KMA

The python file *KMA.py* contains the classes:

* KMACommandline
* KMAIndexCommandline
* KMAShmCommandline
* KMASeq2FastaCommandline
* KMADistCommandline
* KMADBCommandline

For running KMA with cgelib, installing KMA is required. Follow the instructions at:
https://bitbucket.org/genomicepidemiology/kma.git

If you are using KMA for your research, please cite:

  1. Philip T.L.C. Clausen, Frank M. Aarestrup & Ole Lund, "Rapid and precise alignment of raw reads against redundant databases with KMA", BMC Bioinformatics, 2018;19:307.

### KMACommandline

```python
>>>from cgelib.applications.KMA import KMACommandline

>>> kma_application = KMACommandline(input="test.fq", output="path/to/folder", template_db='path/to/template_db/', min_len=0.5)

>>> stdout, stderr=kma_application()
```
The class KMACommandline calls KMA from python. The different options for KMACommandline are:

```
| KMACommandline | KMA           | Description                                                                         |
|----------------|---------------|-------------------------------------------------------------------------------------|
| input          | -i            | Input file name(s)                                                                  |
| input_ipe      | -ip           | Input paired end file name(s)                                                       |
| input_int      | -int          | Input interleaved file name(s)                                                      |
| output         | -o            | Output file                                                                         |
| template_db    | -t_db         | Template db                                                                         |
| k_size         | -k            | Kmersize                                                                            |
| min_len        | -ml           | Minimum alignment length                                                            |
| p_value        | -p            | p-value                                                                             |
| con_clave      | -ConClave     | Conclave version                                                                    |
| mem_mode       | -mem_mode     | Use kmers to choose best template and save memory                                   |
| proxi          | -proxi        | Use proximity scoring under template mapping                                        |
| ex_mode        | -ex_mode      | Search kmers exhaustively                                                           |
| extra_files    | -ef           | Output extra files (mapstat)                                                        |
| vcf            | -vcf          | Make vcf file, 2 to appy FT                                                         |
| sam            | -sam          | Output sam to stdout, 4 to output mapped reads                                      |
| non_consensus  | -nc           | No consensus file                                                                   |
| no_aln         | -na           | No aln file                                                                         |
| no_frag        | -mf           | No frag file                                                                        |
| deCon          | -deCon        | Remove contamination                                                                |
| dense          | -dense        | Do not allow insertions in assembly                                                 |
| sasm           | -sasm         | Skip alignment and assembly                                                         |
| ref_sa         | -ref_sa       | Consensus sequence will have 'n' instead of gaps                                    |
| matrix         | -matrix       | Outputs assembly matrix                                                             |
| best_maps      | -a            | Print all best mappings                                                             |
| min_phred      | -mp           | Minimum phred score                                                                 |
| cut_5p         | -5p           | Cut a constant number of nucleotides from the 5 primers                             |
| cut_3p         | -3p           | Cut a constant number of nucloetides from the 3 primers                             |
| sparse         | -Sparse       | Only count Kmers                                                                    |
| Mt1            | -Mt1          | Map only to 'num' template                                                          |
| ID             | -ID           | Minimum ID                                                                          |
| ss             | -ss           | Sparse sorting (q,c,d)                                                              |
| pm             | -pm           | Pairing method (p,u,f)                                                              |
| fpm            | -fpm          | Fine pairing method (p,u,f)                                                         |
| apm            | -apm          | Sets both pm and fpm                                                                |
| shm            | -shm          | Use shared DB made by kma_shm                                                       |
| mmap           | -mmap         | Memory map *.comp.by                                                                |
| tmp            | -tmp          | Set directory for temporary files                                                   |
| 1t1            | -1t1          | Force end to end mapping                                                            |
| hmm            | -hmm          | Use HMM to assign template to query sequence                                        |
| count_k        | ck            | Count kmers instead of pseudo alignment                                             |
| circular_aln   | -ca           | Make circular alignments                                                            |
| bootstrap      | -boot         | Bootstrap sequence                                                                  |
| bc             | -bc           | Base calls should be significantly overrerpresented                                 |
| bc90           | -bc90         | Base calls should be both significantly overrerpresented and have 90% agreement     |
| bcNano         | -bcNano       | Call bases at suspicious deletio0ns, made for nanopore                              |
| bcd            | -bcd          | Minimum depth at base                                                               |
| bcg            | -bcg          | Maintain isnignificant gaps                                                         |
| and            | -and          | Both mrs and p_value thresholds has to reached to in order to report a template hit |
| MinMapQ        | -mq           | Minimum mapping quality                                                             |
| MinAlnQ        | -mrs          | Minimum alignment score, normalized to alignment length                             |
| mct            | -mct          | Max overlap between templates                                                       |
| reward         | -reward       | Score for match                                                                     |
| penalty        | -penalty      | Penalty for mismatch                                                                |
| gap_open       | -gapopen      | Penalty for gap opening                                                             |
| gap_extend     | -gapextend    | Penalty for gap extension                                                           |
| reward_pairing | -per          | Reward for pairing end                                                              |
| local_open     | -localopen    | Penalty for opening a local chain                                                   |
| n_penalty      | -Npenalty     | Penalty matching N                                                                  |
| transition     | -transition   | Penalty for transition                                                              |
| transversion   | -transversion | Penalty for transversion                                                            |
| cge            | -cge          | Set cge penalties and reward                                                        |
| threads        | -t            | Number of threads                                                                   |
| status         | -status       | extra status                                                                        |
| verbose        | -verbose      | extra verbose                                                                       |
| citation       | -c            | citations                                                                           |
```

### KMAIndexCommandline

```
| KMAIndexCommandline | KMA Index | Description                               |
|---------------------|-----------|-------------------------------------------|
| input               | -i        | Input/query file name                     |
| output              | -o        | Output file                               |
| batch               | -batch    | Batch input file                          |
| deCon               | -deCon    | File with contamination                   |
| batchD              | -batchD   | Batch decon file                          |
| template_db         | -t_db     | Add to existing DB                        |
| k_size              | -k        | Kmersize                                  |
| k_temp              | -k_t      | Kmersize for template identification      |
| k_index             | -k_i      | Kmersize for indexing                     |
| min_len             | -ML       | Minimum length for templates              |
| cs                  | -CS       | Start Chain size                          |
| mega_db             | -ME       | Mega DB                                   |
| no_index            | -NI       | Do not dump *.index.b                     |
| sparse              | -Sparse   | Make Sparse DB                            |
| homology_temp       | -ht       | Homology template                         |
| homology_query      | -hq       | Homology query                            |
| and                 | -and      | Both homology threshold has to be reached |
| no_bias             | -nbp      | No bias print                             |
```

### KMAShmCommandline

```
| KMAShmCommandline | KMA Shm  | Description              |
|-------------------|----------|--------------------------|
| template_db       | -t_db    | Template DB              |
| destroy           | -destroy | Destroy shared memory    |
| shmLvl            | -shmLvl  | Level of shared memory   |
| shm_h             | -shm-h   | Explain of shared memory |
```

### KMASeq2FastaCommandline

```
| KMASeq2FastaCommandline | KMA seq2fasta | Description                       |
|-------------------------|---------------|-----------------------------------|
| template_db             | -t_db         | Template DB                       |
| seqs                    | -seqs         | Comma separated list of templates |
```

### KMADistCommandline

```
| KMADistCommandline | KMA dist | Description                                                                      |
|--------------------|----------|----------------------------------------------------------------------------------|
| template_db        | -t_db    | Template DB                                                                      |
| output             | -o       | Output file                                                                      |
| output_f           | -f       | Output flags                                                                     |
| help_flags         | -fh      | Help on option '-f'                                                              |
| distance_method    | -d       | Distance method. Options:1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096 |
| help_distance      | -dh      | Help on option '-d'                                                              |
| matrix             | -m       | Allocate matrix on the disk                                                      |
| tmp                | -tmp     | Set directory for temporary file                                                 |
| threads            | -t       | Number of threads                                                                |
```

### KMADBCommandline

```
| KMADBCommandline | KMA db | Description |
|------------------|--------|-------------|
| template_db      | -t_db  | Template DB |

```

## Blast

The python file *Blast.py* contains:

* BlastNCommandline

For running BlastN with cgelib, installing Blast is required. Follow the instructions at:
https://www.ncbi.nlm.nih.gov/books/NBK569861/

If you are using Blast for your research, please cite:

  1. Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL. (2009). BLAST+: architecture and applications. BMC Bioinformatics 10(1):421.

### BlastNCommandline

```python
>>>from cgelib.applications.Blast import BlastNCommandline

>>> blastnline = BlastNCommandline(subject="path/to/template.fsa", query="path/to/output.fsa", output="path/to/output", outfmt="6 std qlen", perc_identity=0.9, max_target_seqs=50000, dust="no")

>>> std_output, err_output = blastnline()
```
The class BlastNCommandline calls BlastN from python. The different options for BlastNCommandline are:

```
| BlastNCommandline      | blastn                  | Description                                                                                   |
|------------------------|-------------------------|-----------------------------------------------------------------------------------------------|
| db                     | -db                     | BLAST database name                                                                           |
| query                  | -query                  | Query file name                                                                               |
| query_location         | -query_loc              | Location on the query sequence                                                                |
| output                 | -out                    | Output file name                                                                              |
| evalue                 | -evalue                 | Expect value (E) for saving hits                                                              |
| subject                | -subject                | File with subject sequence(s) to search                                                       |
| subject_location       | -subject_loc            | Locaiton on the subject sequence                                                              |
| show_GIs               | -show_gis               | Show NCBI GIs in report                                                                       |
| num_descriptions       | -num_descriptions       | Show one-line descriptions for this number of database sequences                              |
| num_alignments         | -num_alignments         | Show alignments for this number of database sequences                                         |
| max_target_seqs        | -max_target_seqs        | Number of aligned sequences to keep                                                           |
| max_hsps               | -max_hsps               | Maximum number of HSPs (alignments) to keep for any single query-subject pair.                |
| html                   | -html                   | Porduce HTML output                                                                           |
| seqidlist              | -seqidlist              | Restrict search of database to list of SeqIDs                                                 |
| gilist                 | -gilist                 | Restrict search of database to GI's listed in this file                                       |
| negative_gilist        | -negative_gilist        | Restrict search of database to everything except the GI's listed in this file                 |
| entrez_query           | -entrez_query           | Restrict search with the given Entrez query.                                                  |
| culling_limit          | -culling_limit          | Delete a hit that is enveloped by at least this many higher-scoring hits                      |
| best_hit_overhang      | -best_hit_overhang      | Best hit algorithm overhang value                                                             |
| best_hit_score_edge    | -best_hit_score_edge    | Best hit algorithm score edge value                                                           |
| dbsize                 | -dbsize                 | Effective size of the database                                                                |
| searchsp               | -searchsp               | Effective length of the search space                                                          |
| import_search_strategy | -import_search_strategy | Search strategy file to read                                                                  |
| export_search_strategy | -export_search_strategy | Eecord search strategy to this file                                                           |
| parse_deflines         | -parse_deflines         | Parse query and subject bar delimited sequence identifiers                                    |
| num_threads            | -num_threads            | Numberof threads CPUs to use in blast search                                                  |
| remote                 | -remote                 | Execute search on NCBI servers                                                                |
| outfmt                 | -outfmt                 | Number of threads (CPUs) to use in blast serach                                               |
| task                   | -task                   | Task to execute                                                                               |
| word_size              | -word_size              | Word size for wordfinder algorithm (lenght of best perfect match)                             |
| gapopen                | -gapopen                | Cost to open a gap                                                                            |
| gapextend              | -gapextend              | Word size for wordfinder algorithm (length of best perfect match)                             |
| reward                 | -reward                 | Reward for a nucleotide match                                                                 |
| penalty                | -penalty                | Penalty for a nucleotide mismatch                                                             |
| strand                 | -strand                 | Query strand to search against database/subject                                               |
| dust                   | -dust                   | Filter query sequence with dust                                                               |
| filtering_db           | -filtering_db           | Mask query using the sequences in this database                                               |
| window_masker_taxid    | -window_masker_taxid    | Enable windowmasker filtering using a taxonomic DB                                            |
| sum_stats              | -sum_stats              | Use sum statistics                                                                            |
| window_masker_db       | -window_masker_db       | Enable windowmasker filtering using this file                                                 |
| soft_masking           | -soft_masking           | Apply filtering locations as soft masks                                                       |
| lcase_masking          | -lcase_masking          | Use lower case filtering in query and subject sequence                                        |
| db_soft_mask           | -db_soft_mask           | Filtering algorithm ID to apply to the BLAST database as soft mask                            |
| db_hard_mask           | -db_hard_mask           | Filtering algorithm ID to apply to the BLAST databaseas hard mask                             |
| perc_identity          | -perc_identity          | Percent query identity cutoff                                                                 |
| qcov_hsp_perc          | -qcov_hsp_perc          | Percent query coverage per hsp                                                                |
| template_type          | -template_type          | Discontiguous MegaBLAST template type                                                         |
| template_length        | -template_length        | Discontiguous BegaBlast template length                                                       |
| use_index              | -use_index              | Use MegaBlast Database index                                                                  |
| index_name             | -index_name             | MegaBLAST database index name                                                                 |
| xdrop_ungap            | -xdrop_ungap            | Heuristic value for ungapped extensions                                                       |
| xdrop_gap              | -xdrop_gap              | Heuristic value for preliminary gapped extensions                                             |
| xdrop_gap_final        | -xdrop_gap_final        | Heuristic value for final gapped alignment                                                    |
| no_greedy              | -no_greedy              | Use non_greedy dynamic programming extension                                                  |
| min_raw_gapped_score   | -min_raw_gapped_score   | Minimum raw gapped score to keep an alignment in the preliminary gapped and trace-back stages |
| ungapped               | -ungapped               | Perform ungapped alignment                                                                    |
| window_size            | -window_size            | Multiple hits window size, use 0 to specify 1-hit algorithm                                   |
| off_diagonal_range     | -off_diagonal_range     | Number off-diagonals to search for the 2nd hit use 0 to turn off                              |
| line_length            | -line_length            | Line length for formatting alignments                                                         |
```
