# Sequence sub module documentation

Submodule containing the parent object AlnHit, and KMAHit and BlastnHit. These two last ones are the objects returned when iterating over the alignments with the classes [KMAAligner, BlastNAligner](/alignment/aligner.py), [KMAAlignemtn, BlastNAlignment](/alignment/read_alignment.py), and [KMA_Result](/alignment/KMA/read_files.py) and [BlastN_Result](/alignment/blastn/read_files.py).

The object KMAHit can hold information from different files as long as they are from the same KMA execution. The different files can be of any result file of KMA (Matrix, Result, MapStat, etc.). To create a unique hit from two files containing information of that hit is with the function **merge_hits** The object BlastHit can only contain information from one file.


```python
from cgelib.sequence.SeqHit import BlastnHit, KMAHit

kmahit = KMAHit()
kmahit["evalue"] = 0.3
kmahit["templateID"] = "Templatekma1"
kma3hit = KMAHit()
kma3hit["coverage"] = 80.
kma3hit["query_coverage"] = 80.
kma3hit["templateID"] = "Templatekma1"
new_hit = KMAHit.merge_hits([kmahit, kma3hit])

```
