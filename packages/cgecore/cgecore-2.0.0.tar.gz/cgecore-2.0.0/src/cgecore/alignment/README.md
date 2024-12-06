# Alignment sub module documentation

Submodule dedicated to the alignment of sequences. It contains the classes for reading the files produced by the two aligners used in this package (BLASTN and KMA), and wrappers to run the aligners.

![Scheme](scheme_submodule.png)

## Aligner

The Aligners (BlastNAligner and KMAAligner) are classes that can perform several runs of the aligner, and read the results of those runs.

### KMAAligner

The KMAAligner object is the Aligner that uses KMA. It is able to run KMA, creating several commands depending on a variable to iterate on. For example, if the user wants to align a file called *test1.fq* to a series of FASTA files called *db1.fa*, *db2.fa* and *db3.fa*, the KMAAligner is able to create three KMA commands and run them. After this, the object is able to iterate over the hits found, or save them in a json file with the format of [BeOne](output/templates_json/beone/).

```python
>>> from cgecore.alignment.aligner import KMAAligner

>>> kma_aligner = KMAAligner(result_file=["Result", "Matrix", "Fragments", "VCF"])

```
  **result_file**: The name of the result files desired. For more information about the result files available for KMA, visit [read_files](/alignment/KMA/).

```python
>>> kma_aligner.set_aligner_params(input=loc_rawreads+"/test1.fq", output=loc_output, matrix=True, vcf=True, extra_files=True)

>>> combined_stdout_stderr=kma_aligner(variable_iter="template_db", values_iter=[loc_dataset+"aminoglycoside", loc_dataset+"beta-lactam", loc_dataset+"fosfomycin"])
```
The Aligner class is thought for running the aligners several times iterating over an specific parameter of the aligner; for example, the files containg the template.

In order to run kma several times, the object KMAAligner has to get set the parameters that will be fixed over the different times the aligner is called. Afterwards, when callin the aligner, the parameter that changes its value through the different times the aligner is called has to be set with **variable_iter** (by default, that option is "template_db"; *variable_iter="template_db*"), and the list with the values is indicated with **values_iter**.

```python
>>> kma_aligner.fit_alignment()
```
In order to work with the hits found during the several alignments, **fit_alignment** has to be called.

```python
>>> iterator_hits = kma_aligner.parse_hits()
>>> for hit in iterator_hits:
      print(hit)
```
The function **parse_hits** is an iterator that iterates over all this hits found when running the object KMAAligner. Notice that if several files have been created, the iterator will jump from file to file searching for the hits. The hit will contain information found on the **result_files** indicated before.
For more information about the hit object, visit [hit](/sequence/).

```python
>>> results = kma_aligner.read_alignment_results()
>>> kma_aligner.save_results(json_path="output.json", std_result=results)
```

The function **read_alignment_results** save all the hits produced when running KMAAligner into a dictionary with the [BeOne](output/templates_json/beone/) format. The function **save_results** save the results in a json also with the [BeOne](output/templates_json/beone/) format.

### BlastNAligner

The BlastN aligner works as the KMAAligner, with the same functions and properties. The main differences are found on the **result_files** available (visit [read_files](/alignment/blastn/)), and the default option for *variable_iter* is *subject*.

```python
>>> from cgecore.alignment.aligner import BlastNAligner
>>> blast = BlastNAligner(result_file=["Result", "Fragments", "VCF"])
>>> combined_stdout_stderr = blast(variable_iter="subject",
                                    values_iter = [DATABASE_PATHS])
>>> blast.fit_alignment()
>>> hits = blast.read_alignment_result()["results"]
```

## Read_Alignment

To read the alignments produced by KMA or Blastn, two objects are available: KMAAlignment and BlastNAlignment. Notice that these objects can read several files at the same time and return an iterator of the hits described on those files.

```python
>>> from read_alignment import KMAAlignment, BlastNAlignment

>>> kma_alignment = KMAAlignment(output_path="path/to/folder", filenames=["aminoglycoside", "beta-lactam", "fosfomycin"], result_file=["Result", "Alignment"])
>>> for kmahit in kma_alignment.parse_hits():
      print(kmahit)

>>> blast_alignment= BlastNAlignment(output_path="path/to/folder", filenames=["blasttest2amino5.xml", "blasttest2betalactam5.xml", "blasttest2colistin5.xml", "blasttest2fosfomycin5.xml"], result_file="XML")
>>> for blasthit in blast_alignment.parse_hits():
      print(blasthit)

```
