###Testing of CommandLineBase
```python3
>>> import os
>>> from cgecore.alignment.aligner import KMAAligner, BlastNAligner
>>> loc = os.getcwd()
>>> loc_aln = "%s/../../../data/tests/alignment_files/" % loc
>>> loc_output = "%s/../../../data/tests/output/" % loc
>>> loc_rawreads = "%s/../../../data/tests/raw_reads/" % loc
>>> loc_assembled = "%s/../../../data/tests/assembled_data/" % loc
>>> loc_dataset = "%s/../../../data/tests/datasets/" % loc
>>> k = KMAAligner(result_file=["Result", "Matrix", "Fragments", "VCF"])
>>> k.set_aligner_params(input=loc_rawreads+"/test1.fq", output=loc_output, matrix=True, vcf=True, extra_files=True)
>>> k(values_iter=[loc_dataset+"aminoglycoside", loc_dataset+"beta-lactam", loc_dataset+"fosfomycin"])
>>> k.fit_alignment()
>>> iter = k.parse_hits()
>>> print(next(iter))
>>> print(next(iter))
>>> print(next(iter))
>>> k.read_alignment_result()
>>> k.save_results("./sup2.json")
>>> b = BlastNAligner(result_file="XML")
>>> b.set_aligner_params(query=loc_assembled + "/test1.fsa", output=loc_output, outfmt=5)
>>> b(values_iter=[loc_dataset+"aminoglycoside.fsa", loc_dataset+"beta-lactam.fsa", loc_dataset+"fosfomycin.fsa"])
>>> b.fit_alignment()
>>> b.read_alignment_result()
>>> b.save_results("./supblast5.json")
>>> t = BlastNAligner(result_file="TSV")
>>> t.set_aligner_params(query=loc_assembled + "/test1.fsa", output=loc_output, outfmt=6)
>>> t(values_iter=[loc_dataset+"aminoglycoside.fsa", loc_dataset+"beta-lactam.fsa", loc_dataset+"fosfomycin.fsa"])
>>> t.fit_alignment()
>>> t.read_alignment_result()
>>> t.save_results("./supblast6.json")
>>> t2 = BlastNAligner(result_file="TSV_extra")
>>> t2.set_aligner_params(query=loc_assembled + "/test1.fsa", output=loc_output, outfmt=["7","qseqid","qgi", "qacc", "sseqid", "sallseqid", "sgi", "sallgi", "sacc", "sallacc", "qstart", "qend", "sstart", "send", "qseq", "sseq", "evalue", "bitscore", "score", "length", "pident", "nident", "mismatch", "positive", "gapopen", "gaps", "ppos", "frames", "qframe", "sframe", "btop", "staxids", "sscinames", "scomnames", "sblastnames", "sskingdoms", "stitle", "salltitles", "sstrand", "qcovs", "qcovhsp", "qcovus"])
>>> t2(values_iter=[loc_dataset+"aminoglycoside.fsa", loc_dataset+"beta-lactam.fsa", loc_dataset+"fosfomycin.fsa"])
>>> t2.fit_alignment()
>>> results = t2.read_alignment_result()
>>> t2.save_results("./supblast72.json")
