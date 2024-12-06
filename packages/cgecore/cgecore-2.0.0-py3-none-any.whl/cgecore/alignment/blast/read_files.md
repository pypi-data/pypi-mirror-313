###Testing of CommandLineBase
```python3
>>> from read_files import BLASTN_Result
>>> import os
>>> loc = os.getcwd()
>>> loc_aln = "%s/../../../../data/tests/alignment_files/" % loc
>>> a = BLASTN_Result(output_path=loc_aln, filename="blasttest2amino6.tab", aln_file="TSV")
>>> print(a["TSV"])
>>> print(a)
>>> print(len(a))
>>> m = a.iterate_hits()
>>> print(next(m))
>>> print(next(m))
>>> print(next(m))
>>> print(next(m))
>>> print(next(m))
>>> b = BLASTN_Result(output_path=loc_aln, filename="blasttest2amino5.xml", aln_file="XML")
>>> print(b)
>>> n = b.iterate_hits()
>>> print(next(n))
>>> print(next(n))
>>> print(next(n))
>>> print(next(n))
```
