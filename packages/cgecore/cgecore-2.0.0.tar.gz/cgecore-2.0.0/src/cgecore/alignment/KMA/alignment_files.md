Alignment results class test
=================



###Testing results
```python3
>>> import os
>>> loc = os.getcwd()
>>> loc_aln = "%s/../../../../data/tests/alignment_files/" % loc
>>> from cgecore.alignment.KMA.alignment_files import Iterator_ResFile, Iterator_MapstatFile, Iterator_MatrixFile, Iterator_AlignmentFile, Iterator_ConsensusFile, Iterator_VCFFile, Iterator_SPAFile, Iterator_FragmentFile
>>> iter_res = Iterator_ResFile(path="%s/aminoglycoside.res"%loc_aln)
>>> print(iter_res.EXTENSION)
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> print(next(iter_res))
>>> iter_map = Iterator_MapstatFile(path="%s/aminoglycoside.mapstat"%loc_aln)
>>> print(next(iter_map))
>>> print(next(iter_map))
>>> c = Iterator_ConsensusFile(path="%s/aminoglycoside.fsa"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_VCFFile(path="%s/aminoglycoside.vcf.gz"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_SPAFile(path="%s/aminoglycoside.spa"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_FragmentFile(path="%s/aminoglycoside.frag.gz"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_MatrixFile(path="%s/aminoglycoside.mat.gz"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_AlignmentFile(path="%s/aminoglycoside.aln"%loc_aln)
>>> print(next(c))
>>> print(next(c))
>>> c = Iterator_FragmentFile(path="%s/fosfomycin.frag.gz"%loc_aln)
>>> print(next(c))
>>> c = Iterator_MatrixFile(path="%s/fosfomycin.mat.gz"%loc_aln)
>>> print(next(c))
