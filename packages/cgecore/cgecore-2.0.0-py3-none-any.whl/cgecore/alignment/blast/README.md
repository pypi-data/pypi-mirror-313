# Blast Subsection of the alignment documentation

This submodule contains objects to read the files produced by running blastn.

## read_files

The *read_files.py* file contains the class **BlastN_Result**, which reads a file produced by BlastN

### BlastN_Result

The class **BlastN_Result** can be used for reading an output file of BlastN. The files that can be read by this class are:
  **XML**: File produced when using the option *-outfmt 5* with blastn
  **TSV**: File produced when using the option *-outfmt 6* with blastn
  **TSV_extra**: File produced when using the option *-outfmt 7* with blastn
  **CSV**: File produced when using the option *-outfmt 10* with blastn

More information about the files can be found in the [blast command line description](https://www.ncbi.nlm.nih.gov/books/NBK279684/).

```python
from alignment.blast.read_files import BLASTN_Result

blast_result = BLASTN_Result(output_path="path/to/folder", filename="blasttest2amino5.xml", aln_file="XML")
for blasthit in blast_result.iterate_hits():
  print(blasthit)

```
To iterate over the hits in the file, use the function **iterate_hits**. It returns an iterator of [BlastHits](/sequence/).

## alignment_files

The *alignment_files.py* file contains the iterators that are called by the class **BlastN_Result**.

    **Iterator_XMLFile**: Iterator for *.xml* files
    **Iterator_BlastSepFile**: Iterator for *.tsv* and *.csv* files
