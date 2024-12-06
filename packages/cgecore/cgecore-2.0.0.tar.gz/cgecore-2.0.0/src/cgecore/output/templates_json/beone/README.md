# BeOne template

BeOne example output from ResFinder: [example.json](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/beone/example.json)

## Classes

- **software_result**
- **database**
- **seq_region**
- **seq_variation**
- **phenotype**

### software_result

```json

"software_result": {
    "type": "software_result",
    "key": "string*",
    "software_name": "string*",
    "software_version": "string*",
    "software_branch": "string",
    "software_commit": "string",
    "software_log": "string",
    "run_id": "string",
    "run_date": "date",
    "databases": "dict database:class",
    "seq_regions": "dict seq_region:class",
    "seq_variations": "dict seq_variation:class",
    "phenotypes": "dict phenotype:class",
    "provided_species": "string",
    "software_executions": "dict software_exec:class",
    "aln_hits": "dict aln_hit:class",
    "result_summary": "string"
  }

```

**key**: For CGE tools the key will be <software_name>-<software_version>  
*Example*: ResFinder-4.1.0

**software_name**: Name of the application creating the output.  
*Example*: "software_name": "ResFinder"

**software_version**: [Semantic Versioning](https://semver.org/). Given a version number MAJOR.MINOR.PATCH. If no version number can be provided,
the first seven digits of the Git commit checksum is expected here.  
*Example*: 4.1.0
*Example*: d48a0fe

**software_branch**: Name of the git branch.  
*Example*: develop

**software_commit**: Git commit checksum.  
*Example*: d48a0fe7afa763a50777c89a3289d1fd3b13cee5

**software_log**: Ouput written to stdout and/or stderr by the software.

**run_id**: The id should uniquely define how the software was run. Two
identical run_ids should indicate two identical runs. This could be a checksum.

**run_date**: Date and time for when the software was started. UTC timezone.

**databases**: See "database" description.

**seq_regions**: See "gene" description.

**seq_variations**: See "seq_variation".

**phenotypes**: See "phenotypes".

**provided_species**: Full species name, as provided to the software by external software or user.
*Example*: Salmonella enterica

**aln_hits**: See "aln_hits".

**software_executions**: See "software_executions".

**result_summary**: A single string meant to summarise the main result as shortly as possible. There is no fixed format for the string. It should be documented by the application writing the result.
*Example (ResFinder)*: AMP_STR_SUL

### database

```json

"database": {
    "type": "database",
    "key": "string*",
    "database_name": "string*",
    "database_version": "string",
    "database_branch": "string",
    "database_commit": "string",
    "checksum_sha256": "char64"
  }

```

**key**: For CGE tools the key will be <database_name>-<database_version>.  
*Example*: PointFinder-d48a0fe

**database_name**: Name of a database used when running the software.  
*Example*: PointFinder

**database_version**: [Semantic Versioning](https://semver.org/). Given a version number MAJOR.MINOR.PATCH. If no version number can be provided,
the first seven digits of the Git commit checksum is expected here.  
*Example*: 4.1.0
*Example*: d48a0fe

**database_branch**: Name of the git branch.  
*Example*: develop

**database_commit**: Git commit checksum.  
*Example*: d48a0fe7afa763a50777c89a3289d1fd3b13cee5

**checksum_sha256**: SHA256 checksum of entire database.  
*Example*: 08304e062528ae12ecb07abe139e26512fb5991e36df93e30e0d92d885479709

### seq_region

```json

"seq_region": {
    "type": "seq_region",
    "key": "string*",
    "name": "string*",
    "gene": "bool_or_unknown",
    "identity": "percentage",
    "alignment_length": "integer",
    "ref_seq_lenght": "integer",
    "coverage": "percentage",
    "depth": "float",
    "ref_id": "string*",
    "ref_acc": "string",
    "ref_start_pos": "integer",
    "ref_end_pos": "integer",
    "query_id": "string",
    "query_start_pos": "integer",
    "query_end_pos": "integer",
    "phenotypes": "array phenotype.key",
    "ref_database": "array database.key*",
    "note": "string",
    "query_string": "string",
    "alignment_string": "string",
    "ref_string": "string" 
  }

```

**key**: Unique identifier for seq_region hit. Several hits to the same seq_region can occur. Unlike the ref_id, this key must be unique between these hits.  
*Example*: aph(6)-Id;;1;;M28829;;d5sm

**name**: Gene name / Region name.  
*Example*: aph(6)-Id

**gene**: True if the seq_region is a gene, if not, False or unknown.

**identity**: Percent identical bps between query data (input) and reference
seq_region (database).

**alignment_length**: Number of bps in the alignment between query and
reference.

**ref_seq_lenght**: Length in bps of the reference seq_region.

**coverage**: Percentage of the reference seq_region covered by the query data.

**depth**: Average number of times the reference seq_region has been covered by the
query data.

**ref_id**: Unique identifier for seq_region in database, but doesn't have to be
unique in the results. See also "key".  
*Example*: aph(6)-Id_1_M28829

**ref_acc**: If the reference seq_region is extracted from a public database, the
accession number identifying the sequence is stored here.  
*Example*: M28829

**ref_start_pos**: Position in reference seq_region where the alignment starts.

**ref_end_pos**: Position in reference seq_region where the alignment ends.

**query_id**: Unique identifier for the input sequence. For example a contig or
read header.  
*Example*: NODE_47_length_14097_cov_7.40173_ID_3656

**query_start_pos**: Position in query seq_region where the alignment starts.

**query_end_pos**: Position in query seq_region where the alignment starts.

**phenotypes**: List of phenotypes associated to the seq_region.

**ref_database**: List of keys uniquely identifying the databases where the
reference seq_region can be found. Will often just be a list of one item.
*Example*: [PointFinder-d48a0fe]

**note**: Free text field for additional information.

**query_string**: The query nucleotide sequence

**alignment_string**: representation of the alignment. | symbolises a match
while a space indicates mismatch.

**ref_string**: The nucleotide sequence of the reference region.  

### seq_variation

```json

"seq_variation": {
    "type": "seq_variation",
    "key": "string*",
    "ref_id": "string*",
    "seq_var": "seq_var_string",
    "codon_change": "codon_change_string",
    "ref_codon": "nucleotides",
    "var_codon": "nucleotides",
    "ref_aa": "aminoacid_1_char",
    "var_aa": "aminoacid_1_char",
    "ref_start_pos": "integer",
    "ref_end_pos": "integer",
    "substitution": "bool",
    "insertion": "bool",
    "deletion": "bool",
    "ref_database": "array database.key*",
    "seq_regions": "array seq_region.key",
    "phenotypes": "array phenotype.key"
  }

```

**key**: Unique identifier for sequence variation. Format is:
<seq_region>;;<ref_start_pos>;;<var_codon>(;;<random_string>), where pos is the
position of the first nucleotide in the codon. The codon can be a single
nucleotide if found in a non-coding region. If the first part is not unique then
a small random string of small letters will be attached.
*Example*: 23S;;357;;t

**ref_id**: String to identify the mutation in the reference database. Format
is: <seq_region>;;<ref_start_pos>;;<var_codon>. Similar to key but not
guarenteed to be unique.
*Example*: folP;;28;;tta

**seq_var**: String describing the nucleotide variation according [HGVS Sequence Variant Nomenclature](http://varnomen.hgvs.org/)  
*Example*: p.I38L

**codon_change**: String describing codon change. Is not used in non-coding variations. The format is <ref codon>><alt_codon>  
*Example*: ata>tta

**ref_codon**: Reference codon.  Is not used in non-coding variations.  
*Example*: ata

**var_codon**: Codon found in the input data. Is not used in non-coding variations.  
*Example*: tta

**ref_aa**: Reference amino acid. 1-character-coding.  
*Example*: i

**var_aa**: Amino acid found in input data. 1-character-coding.  
*Example*: l

**ref_start_pos**: Position of variation start. If in coding region this is the amino acid position, if in a non-coding region this is the nucleotide acid position. For single amino acid substitution, this will be identical to ref_end_pos.  
*Example*: 38

**ref_end_pos**: Position of variation end. If in coding region this is the amino acid position, if in a non-coding region this is the nucleotide acid position. For single amino acid substitution, this will be identical to ref_end_pos.  
*Example*: 38

**substitution**: True if the variation is a substitution.

**insertion**: True if the variation is an insertion.

**deletion**: True if the variation is a deletion.

**ref_database**: List of keys uniquely identifying the databases where the
varation is annotated. Will often just be a list of one item.
*Example*:[PointFinder-6323b5c]

**seq_regions**: List of seq_regions associated to the sequence variation.

**phenotypes**: List of phenotypes associated to the sequence variation.

### phenotype

```json

"phenotype": {
    "type": "phenotype",
    "key": "string*",
    "category": "vocabulary*",
    "amr_classes": "array vocabulary",
    "amr_resistance": "vocabulary",
    "amr_resistant": "bool_or_unknown",
    "amr_species_relevant": "bool",
    "vir_virulent": "bool_or_unknown",
    "vir_function": "string",
    "seq_regions": "array seq_region.key",
    "seq_variations": "array seq_variation.key",
    "ref_database": "array database.key"
  }

```

**key**: Unique identifier for phenotype.

**category**: phenotype category vocabulary.  
*Example*: amr

**amr_classes**: List of amr classes the phenotype belongs to.

**amr_resistance**: Name of antibiotic to which this phenotype causes resistance.  
*Example*: netilmicin

**amr_resistant**: Indicates if the phenotype in question describes amr resistance.

**amr_species_relevant**: Indicate if the current phenotype is deemed relevant by the tool for the provided species. If no species is provided this should always be true.

**vir_virulent**: Indicates if the phenotype in question describes a virulence factor.

**vir_function**: Describes the protein function of the virulence factor.

**seq_regions**: List of seq_regions causing the phenotype, found in the output in question. Not a comprehensive list of seq_regions causing the phenotype in question.

**seq_variations**: List of sequence variations causing the phenotype, found in the output in question. Not a comprehensive list of sequence variations causing the phenotype in question.

**ref_database**: List of keys uniquely identifying the databases where the
phenotype is annotated. Will often just be a list of one item.
*Example*:[PointFinder-6323b5c]

### software_executions

```json

"software_exec": {
    "type": "software_exec",
    "key": "string*",
    "software_name": "string",
    "command": "string",
    "parameters": "dictionary",
    "stdout": "string",
    "stderr": "string"
}

```

**key**: Unique identifier for software execution.

**software_name**: name of the software executable.
*Example*: kma

**command**: string with the command of the execution of the program
*Example*: "kma -i /path/to/inputfile -o /path/to/output"

**parameters**: dictionary with keys as the parameter and values as the value of the parameter

**stdout**: STDOUT of the execution of the program

**stderr**: STDERR of the execution of the program

### aln_hits

```json

"aln_hit": {
    "type": "aln_hit",
    "key": "string*",
    "queryID": "string",
    "templateID": "string",
    "query_identity": "float",
    "template_identity": "float",
    "template_length": "integer",
    "template_start_aln": "integer",
    "template_end_aln": "integer",
    "query_aln": "string",
    "template_aln": "string",
    "aln_scheme": "string",
    "evalue": "float",
    "aln_length": "integer",
    "query_coverage": "float",
    "template_coverage": "float",
    "query_start_aln": "integer",
    "query_end_aln": "integer",
    "bitscore": "integer",
    "raw_score": "float",
    "n_identity": "float",
    "mismatch": "integer",
    "n_pos_matches": "integer",
    "gapopen": "integer",
    "gaps": "integer",
    "frame": "tuple",
    "query_frame": "integer",
    "template_frame": "integer",
    "btop": "float",
    "template_taxids": "string",
    "template_scie_name": "string",
    "template_common_name": "string",
    "template_blast_name": "string",
    "template_superkingdom": "string",
    "template_title": "string",
    "all_template_title": "string",
    "template_strand": "string",
    "query_coverage_hsp": "float",
    "db_number": "string",
    "db_length": "integer",
    "hsp_length": "integer",
    "effective_space": "float",
    "kappa": "float",
    "lambda": "float",
    "entropy": "float",
    "query_coverage_once": "float",
    "conclave_score": "float",
    "depth": "float",
    "q_value": "float",
    "p_value": "float",
    "reads_mapped": "integer",
    "fragments_mapped": "integer",
    "mapScoreSum": "float",
    "template_coveredPos": "string",
    "tot_query_coverage": "float",
    "tot_template_coverage": "float",
    "tot_depth": "float",
    "Num": "int",
    "template_consesusSum": "float",
    "bpTotal": "integer",
    "depth_variance": "float",
    "nucHigh_depth_variance": "float",
    "depth_max": "float",
    "snps": "float",
    "insertions": "float",
    "deletions": "float",
    "reads_mapped_align": "integer",
    "fragments_mapped_align": "integer",
    "matrix": "dict matrix_position:class",
    "point_variations": "dict point_variation:class",
    "reads_aligned": "dict fragment_aligned:class",
    "score": "integer",
    "n_alignments": "integer",
    "identities": "integer",
    "positives": "integer",
    "strand": "tuple",
    "frame": "tuple",
    "template_file": "array",
    "file_paths": "array",
    "aln_files": "array",
    "exec_key": "software_exec.key"
  }

```

**key**: Unique identifier of a hit of an alignment

**queryID**: Identifier of sequence (FASTA header) aligned on a template sequence (hit from blast)

**templateID**: Identifier of template sequence (FASTA header).

**query_identity**: Identity of the query sequence. Number of bases in the template sequence that are identical to the consensus sequence divided by the length of the consensus (KMA) or to the query sequence divided by the length of the query (Blast).

**template_identity**: Identity of the template sequence. Number of bases in the consensus sequence (KMA) or query sequence (Blast) that are identical to the template sequence divided by the Template_length.

**template_length**: Amount of nucleotides of the template sequence, without preceding and trailing N’s

**template_start_aln**: Position of the start of the alignment on the template

**template_end_aln**: Position of the end of the alignment on the template

**query_start_aln**: Position of the start of the alignment on the query

**query_end_aln**: Position of the end of the alignment on the query

**query_aln**: Aligned part of consensus (KMA) or query (Blast) sequence

**template_aln**: Aligned part of the template sequence

**aln_scheme**: Scheme of the alignment between query or consensus sequence with template.

**evalue**: Expected value

**aln_length**: Alignment length

**template_coverage**: Number of bases in the template sequence that are identical to the consensus sequence divided by the length of the consensus or to the query sequence divided by the length of the query sequence.

**query_coverage**: The reciprocal values of the Template_Coverage. A Query_Coverage above 100% indicates the presence of more deletions than insertions.

**bitscore**: Bit score (for blast)

**raw_score**: Raw score (for blast)

**n_identity**: Number of identical matches

**mismatch**: Number of mismatches

**n_pos_matches**:  Number of positive-scoring matches

**pos_matches**: Percentage of positive-scoring matches

**gapopen**: Number of gaps openings

**gaps**: Total number of gap

**frame**: Query and subject frames separated by a '/'

**query_frame**: Query frame

**template_frame**: Template frame

**btop**: Blast traceback operations (BTOP)

**template_taxids**: Unique Subject Taxonomy ID(s), separated by a ';'(in numerical order)

**template_scie_name**: Unique Subject Scientific Name(s), separated by a ';'

**template_common_name**: Unique Subject Common Name(s), separated by a ';'

**template_blast_name**: Unique Subject Blast Name(s), separated by a ';' (in alphabetical order)

**template_superkingdom**: Unique Subject Super Kingdom(s), separated by a ';' (in alphabetical order)

**template_title**: Template title

**all_template_title**: All Subject Title(s), separated by a '<>'

**template_strand**: Template strand

**query_coverage_hsp**: Query Coverage Per HSP

**db_number**: Number DB

**db_length**: Length DB

**hsp_length**: Length HSP

**effective_space**: Effective space

**kappa**: Kappa (statistics)

**lambda**: Lambda (statistics)

**entropy**: Entropy (statistics)

**query_coverage_once**: ?

**conclave_score**: Accumulated alignment score, from all reads that were accepted to match this template.

**depth**: The depth of coverage of the template by reads. Commonly referred to as X-coverage, coverage, abundance, etc.

**q_value**: The obtained quantile in a  21 -distribution, when comparing the obtained Score with the Expected, using a McNemar test.

**p_value**: The obtained p-value from the quantile Q_value.

**reads_mapped**: Number of reads mapped the template.

**fragments_mapped**: Number of fragments mapped to the template

**mapScoreSum**: Accumulated mapping score, the same as the ConClave score

**template_coveredPos**: The number of covered positions in the template with a minimum depth of 1.

**template_consesusSum**: Total number of bases identical to the template.

**tot_query_coverage**: Total query coverage (?)

**tot_template_coverage**: Total template coverage (?)

**tot_depth**: Total depth (?)

**Num**: Num (?)

**bpTotal**: Total number of bases aligned to the template.

**depth_variance**: The variance of the depth over the template.

**nucHigh_depth_variance**: The number of positions in the template were the depth is more than 3 standard deviations higher.

**depth_max**: The maximum depth at any position in the template.

**snps**: Total number of SNPs.

**insertions**: Total number of insertions.

**deletions**: Total number of deletions.

**reads_mapped_align**: (?)

**fragments_mapped_align**: (?)

**matrix**: Dictionary with the bases found to align to the template per each position. For more, see "matrix_position".

**point_variations**: Dictionary with the variations found per each position. For more, see "point_variations".

**reads_aligned**: Dictionary with the information of each read aligned to the template. For more, see "reads_aligned".

**score**: (?)

**n_alignments**: Number of alignments (?)

**identities**: (?)

**positives**:  (?)

**strand**: (?)

**frame**: (?)

**template_file**: Name of the file the hit is coming from (output of aligner)

**file_paths**: File paths where the information for the hit has been extracted from.

**aln_files**: Name of the type of alignment file(s) that contained the information for the hit.

**exec_key**: Key of the execution of the aligner that produced this hit.

## matrix_position

```json
"matrix_position":{
    "type": "matrix_position",
    "key": "string*",
    "position": "integer",
    "ref_nucl": "string",
    "A_nucl": "integer",
    "G_nucl": "integer",
    "T_nucl": "integer",
    "C_nucl": "integer",
    "N_nucl": "integer",
    "null_nucl": "integer"
}
```

**key**: Unique identifier of a position of the template sequence for the different amount of nucletides aligned.

**position**: Position at the template

**ref_nucl**: Nucleotide in the template at that position

**A_nucl**: Amount of Adenines aligned to that position

**G_nucl**: Amount of Guanines aligned to that position

**T_nucl**: Amount of Thymines aligned to that position

**C_nucl**: Amount of Cytosines aligned to that position

**N_nucl**: Amount of unknown base aligned to that position

**null_nucl**: Amount of gaps aligned to that position

## point_variation

```json
"point_variation":{
    "type": "point_variation",
    "key": "string*",
    "position": "integer",
    "id": "string",
    "ref_base": "string",
    "alt_base": "string",
    "quality": "float",
    "filter": "string",
    "info": "string",
    "format": "string"
}
```

**key**: Unique identifier of a mutation in a position

**position**: Position of the mutation on the template

**id**: Identifier, semicolon-separated list of unique identifiers where available

**ref_base**: reference base

**alt_base**: alternate base(s), comma separated list of alternate non-reference alleles.

**quality**: Phred-scaled quality score for the assertion made in alt_base

**filter**: Filter status; PASS if this position has passed all filters, i.e., a call is made at this position.

**info**: Additional information

**format**: ??

## fragment_aligned

```json
"fragment_aligned":{
    "type": "fragment_mapped",
    "key": "string*",
    "query_seq": "string",
    "eq_mapped": "integer",
    "aln_score": "float",
    "start_aln": "integer",
    "end_aln": "integer",
    "template_name": "hit.templateID",
    "query_name": "string",
    "cut_start": "integer",
    "cut_end": "integer"
}
```

**key**: Unique identifier of the fragment aligned to the template

**query_seq**: Fragment (query sequence)

**eq_mapped**: Number of equally well mapping templates

**aln_score**: Alignment score

**start_aln**: start coordinates of the alignment toward the template

**end_aln**: end coordinates of the alignment toward the template

**template_name**: Template name

**query_name**: Query name sequence

**cut_start**: Start of the cut in the query sequence with respect the original sequence

**cut_end**: End of the cut in the query sequence with respect the original sequence

## ISSUES

**genes and seq_variation notes**
Should add a free text notes field for seq_variation entries.

**seq_variation key and ref_id**  
Are they always identical. If so, can there be two identical keys?

**Missing value parser**

- seq_var_string
- codon_change_string
- aminoacid_1_char
- vocabulary

**Vocabulary**
*Under construction*
Vocabulary values are only valid if they are found in specific vocabulary templates/definitions. How exactly they should be formatted is still being discussed.  
A vocabulary should be identified either by <key>.vocabulary or <class>.<key>.vocabulary. How to handle different classes using same vocabulary?

**seq_variation.genes**
Should this be a list? Why?

**phenotype**
amr_classes: Is currently being written to the key "classes"  
amr_resistance: Is currently being written to the key "resistance"  
amr_resistant: Not currently used.  

## SUGGESTIONS

**provided_species**
Currently allows any string, maybe it should test for valid species.
