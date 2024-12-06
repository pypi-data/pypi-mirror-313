# KMA Subsection of the alignment documentation

This submodule contains objects to read the files produced by running kma.

## read_files

The *read_files.py* file contains the class **KMA_Result**, which reads files produced by KMA.

###BlastN_Result

The class **KMA_Result** can be used for reading an output file of KMA. As KMA can produced more than one file per run, and each file can contain different information from the same hit/alignment, the class **KMA_Result** can iterate over several files at the same time to return hits/alignments resuming the information from the different files (besides the *.spa* file). The files that can be read by this class are:

  **ResultFile**: File with extension *.res*. Produced by KMA by default.
  **MapStatFile**: File with extension *.mapstat*. Produced when using the option *-ef*.
  **MatrixFile**: File with extension *.mat.gz*. Produced when using the option *-matrix*.
  **AlignmentFile**: File with extension *.aln*. Produced by default.
  **ConsensusFile**: File with extension *.fsa*. Produced by default.
  **VCFFile**: File with extension *.vcf.gz*. Produced when using the option *-vcf*.
  **SPAFile**: File with extension *.spa*. Produced when using the option *-Sparse*.
  **FragmentFile**: File with extension *.frag.gz*. Produced by default.

More information about the content in the different files can be found in the [KMA file](https://bitbucket.org/genomicepidemiology/kma/src/master/KMAspecification.pdf)

```python
from alignment.KMA.read_files import KMA_Result

kma_result = KMA_Result(output_path="path/to/folder", filename="aminoglycoside", aln_files=["Result", "VCF", "Mapstat"])
for kmahit in kma_result.iterate_hits():
  print(kmahit)

```
To iterate over the hits in the file, use the function **iterate_hits**. It returns an iterator of [KMAHits](/sequence/).

## alignment_files

The *alignment_files.py* file contains the iterators that are called by the class **KMA_Result**.

    **Iterator_ResFile**: Iterator for *.res* files
    **Iterator_MapstatFile**: Iterator for *.mapstat* files
    **Iterator_MatrixFile**: Iterator for *.mat.gz* files
    **Iterator_AlignmentFile**: Iterator for *.aln* files
    **Iterator_ConsensusFile**: Iterator for *.fsa* files
    **Iterator_VCFFile**: Iterator for *.vcf.gz* files
    **Iterator_SPAFile**: Iterator for *.spa* files
    **Iterator_FragmentFile**: Iterator for *.frag.gz* files
