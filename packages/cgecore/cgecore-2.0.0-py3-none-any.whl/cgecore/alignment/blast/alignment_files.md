Alignment results class test
=================



###Testing results
```python3
>>> from cgecore.alignment.blast.alignment_files import Iterator_BlastSepFile, Iterator_XMLFile
>>> import os
>>> loc = os.getcwd()
>>> loc_aln = "%s/../../../../data/tests/alignment_files/" % loc
>>> iter_res = Iterator_BlastSepFile("%s/blasttest2amino6.tab"%loc_aln, separator="tab", comment_lines=False)
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_BlastSepFile("%s/blasttest2amino10.tab" % loc_aln, separator="comma")
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_BlastSepFile("%s/blasttest2amino7.tab"%loc_aln, separator="tab", comment_lines=True)
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_XMLFile("%s/blasttest2amino5.xml" %loc_aln)
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_XMLFile("%s/blasttest2amino5.xml"%loc_aln)
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_BlastSepFile("%s/blasttest2amino10.tab" % loc_aln, separator="comma")
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_res = Iterator_BlastSepFile("../../../../data/tests/output/blastn-alignment_subject-aminoglycoside.tsv", separator="tab", comment_lines=True)
>>> print(next(iter_res))
>>> print(next(iter_res))
