###Testing of CommandLineBase
```python3
>>> from read_files import KMA_Result
>>> import os
>>> loc = os.getcwd()
>>> loc_aln = "%s/../../../../data/tests/alignment_files/" % loc
>>> b = KMA_Result(output_path=loc_aln, filename="aminoglycoside", aln_files=["Result"])
>>> print(b)
>>> n = b.iterate_hits()
>>> print(next(n))
>>> print(next(n))
>>> a = KMA_Result(output_path=loc_aln, filename="aminoglycoside", aln_files=["Result", "Matrix"])
>>> print(a["Result"])
>>> print(a)
>>> n = a.iterate_hits()
>>> print(next(n))
>>> print(next(n))
>>> print(len(a))
>>> b = KMA_Result(output_path=loc_aln, filename="aminoglycoside", aln_files=["Result", "VCF", "Mapstat"])
>>> print(b)
>>> n = b.iterate_hits()
>>> print(next(n))
>>> print(next(n))
>>> print(next(n))
>>> print(next(n))
```
