Application class test
=================

### Testing of KMACommandLineBase

```python

>>> ### Get locations ###
>>> import os
>>> loc_py = os.getcwd()
>>> loc_data = loc_py + "/../../../data/tests"
>>> ### Start testing ###
>>> from cgecore.applications.KMA import KMACommandline
>>> kmaline = KMACommandline(k_size=10, min_len=0.5, sparse=True)
>>> kmaline
KMACommandline(cmd='kma', k_size=10, min_len=0.5, sparse=True)

You can instead manipulate the parameters via their properties, e.g.
>>> kmaline.k_size
10
>>> kmaline.k_size = 20
>>> kmaline
KMACommandline(cmd='kma', k_size=20, min_len=0.5, sparse=True)

You can clear a parameter you have already added by 'deleting' the
corresponding property:
>>> del kmaline.k_size
>>> kmaline.k_size
'DB defined (default)'
>>> kmaline.output = "./loc"
>>> kmaline.template_db = "./template_db/"
>>> str(kmaline)# doctest:+ELLIPSIS
Traceback (most recent call last):
...
ValueError: Parameter input is not set. Neither alternative parameters as input_int, input_ipe.
>>> kmaline.input = "./home.txt"
>>> kmaline.input
'./home.txt'
>>> kmaline
KMACommandline(cmd='kma', input='./home.txt', output='./loc', template_db='./template_db/', min_len=0.5, sparse=True)
>>> str(kmaline)
'kma -i ./home.txt -o ./loc -t_db ./template_db/ -ml 0.5 -Sparse'
>>> kmaline.input_ipe = "/home2.txt"
>>> str(kmaline)# doctest:+ELLIPSIS
Traceback (most recent call last):
...
ValueError: Parameter 'input_ipe' is set, but the incompatible parameter 'input' has been also set.

>>> del kmaline.input
>>> kmaline.input_ipe = ["/home2.txt","/home1.txt"]
>>> str(kmaline)
'kma -ipe /home2.txt /home1.txt  -o ./loc -t_db ./template_db/ -ml 0.5 -Sparse'
>>> kmaline.path_exec = "/home/alfred/bio_tools/kma/"
>>> str(kmaline)
'/home/alfred/bio_tools/kma/kma -ipe /home2.txt /home1.txt  -o ./loc -t_db ./template_db/ -ml 0.5 -Sparse'
>>> kmaline.path_exec = ""
>>> del kmaline.input_ipe
>>> del kmaline.min_len
>>> del kmaline.sparse
>>> kmaline.input = ["%s/raw_reads/test2_R1.fq"%loc_data,"%s/raw_reads/test2_R2.fq"%loc_data]
>>> kmaline.template_db = "%s/datasets/beta-lactam"%loc_data
>>> kmaline.output = "%s/alignment_files/beta-lactam"%loc_data
>>> print(kmaline)# doctest:+ELLIPSIS
kma -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/beta-lactam -t_db .../../../../data/tests/datasets/beta-lactam
>>> kmaline.matrix = True
>>> kmaline.best_maps = True
>>> kmaline.extra_files = True
>>> kmaline.vcf = 2
>>> print(kmaline)# doctest:+ELLIPSIS
kma -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/beta-lactam -t_db .../../../../data/tests/datasets/beta-lactam -ef -vcf 2 -matrix -a
>>> kmaline.vcf = True
>>> print(kmaline)
... #doctest: +ELLIPSIS
kma -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/beta-lactam -t_db .../../../../data/tests/datasets/beta-lactam -ef -vcf -matrix -a
>>> std_output, err_output = kmaline()
>>> print(std_output)
<BLANKLINE>
>>> print(err_output)# doctest:+ELLIPSIS
# Reading inputfile: 	.../../../../data/tests/raw_reads/test2_R1.fq
# Phred scale:	33
# Reading inputfile: 	.../../../../data/tests/raw_reads/test2_R2.fq
# Phred scale:	33
#
# Query converted
#
# Running KMA.
#
# Total time used for DB loading: 0.00 s.
#
# Finding k-mer ankers
# Query ankered
#
# KMA mapping done
#
# Sort, output and select KMA alignments.
# Total time for sorting and outputting KMA alignment	0.00 s.
#
# Doing local assemblies of found templates, and output results
# Total time used for local assembly: 0.00 s.
#
# Closing files
>>> stdout, stderr = kmaline()
>>> print(stdout)
>>> print(stderr)
# Reading inputfile: 	/home/alfred/Projects/cgelib/src/cgelib/applications/../../../data/tests/raw_reads/test2_R1.fq
# Phred scale:	33
# Reading inputfile: 	/home/alfred/Projects/cgelib/src/cgelib/applications/../../../data/tests/raw_reads/test2_R2.fq
# Phred scale:	33
#
# Query converted
#
# Running KMA.
#
# Total time used for DB loading: 0.01 s.
#
# Finding k-mer ankers
# Query ankered
#
# KMA mapping done
#
# Sort, output and select KMA alignments.
# Total time for sorting and outputting KMA alignment	0.00 s.
#
# Doing local assemblies of found templates, and output results
# Total time used for local assembly: 0.00 s.
#
# Closing files
# Reading inputfile: 	/home/alfred/Projects/cgelib/src/cgelib/applications/../../../data/tests/raw_reads/test2_R1.fq
# Phred scale:	33
# Reading inputfile: 	/home/alfred/Projects/cgelib/src/cgelib/applications/../../../data/tests/raw_reads/test2_R2.fq
# Phred scale:	33
#
# Query converted
#
# Running KMA.
#
# Total time used for DB loading: 0.01 s.
#
# Finding k-mer ankers
# Query ankered
#
# KMA mapping done
#
# Sort, output and select KMA alignments.
# Total time for sorting and outputting KMA alignment	0.00 s.
#
# Doing local assemblies of found templates, and output results
# Total time used for local assembly: 0.00 s.
#
# Closing files

>>> kmaline.template_db = "%s/datasets/colistin"%loc_data
>>> kmaline.output = "%s/alignment_files/colistin"%loc_data
>>> kmaline()# doctest:+ELLIPSIS
('', '# Running KMA.\n# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R1.fq\n# Phred scale:\t33\n# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R2.fq\n# Phred scale:\t33\n#\n# Query converted\n#\n#\n# Total time used for DB loading: 0.00 s.\n#\n# Finding k-mer ankers\n# Query ankered\n#\n# KMA mapping done\n#\n# Sort, output and select KMA alignments.\n# Total time for sorting and outputting KMA alignment\t0.00 s.\n#\n# Doing local assemblies of found templates, and output results\n# Total time used for local assembly: 0.00 s.\n#\n# Closing files\n')
>>> kmaline.template_db = "%s/datasets/aminoglycoside"%loc_data
>>> kmaline.output = "%s/alignment_files/aminoglycoside"%loc_data
>>> kmaline()# doctest:+ELLIPSIS
('', '# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R1.fq\n# Phred scale:\t33\n# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R2.fq\n# Phred scale:\t33\n#\n# Query converted\n#\n# Running KMA.\n#\n# Total time used for DB loading: 0.00 s.\n#\n# Finding k-mer ankers\n# Query ankered\n#\n# KMA mapping done\n#\n# Sort, output and select KMA alignments.\n# Total time for sorting and outputting KMA alignment\t0.00 s.\n#\n# Doing local assemblies of found templates, and output results\n# Total time used for local assembly: 0.01 s.\n#\n# Closing files\n')
>>> kmaline.template_db = "%s/datasets/fosfomycin"%loc_data
>>> kmaline.output = "%s/alignment_files/fosfomycin"%loc_data
>>> kmaline()# doctest:+ELLIPSIS
('', '# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R1.fq\n# Phred scale:\t33\n# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R2.fq\n# Phred scale:\t33\n#\n# Query converted\n#\n# Running KMA.\n#\n# Total time used for DB loading: 0.00 s.\n#\n# Finding k-mer ankers\n# Query ankered\n#\n# KMA mapping done\n#\n# Sort, output and select KMA alignments.\n# Total time for sorting and outputting KMA alignment\t0.00 s.\n#\n# Doing local assemblies of found templates, and output results\n# Total time used for local assembly: 0.00 s.\n#\n# Closing files\n')
>>> kmaline = KMACommandline(sparse=True)
>>> kmaline.input = ["%s/raw_reads/test2_R1.fq"%loc_data,"%s/raw_reads/test2_R2.fq"%loc_data]
>>> kmaline.template_db = "%s/datasets/aminoglycosideCT"%loc_data
>>> kmaline.output = "%s/alignment_files/aminoglycoside"%loc_data
>>> kmaline.sparse
True
>>> print(kmaline)# doctest:+ELLIPSIS
kma -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/aminoglycoside -t_db .../../../../data/tests/datasets/aminoglycosideCT -Sparse
>>> kmaline()
('', '# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R1.fq\n# Phred scale:\t33\n# Reading inputfile: \t.../../../../data/tests/raw_reads/test2_R2.fq\n# Phred scale:\t33\n#\n# Query converted\n#\n#\n# Total time used for DB loading: 0.00 s.\n#\n# Finding k-mers\n# k-mers in query identified\n#\n# Finding best matches and output results.\n# Total number of matches: 182 of 231 kmers\n# Total for finding and outputting best matches: 0.00 s.\n#\n# Closing files\n')
>>> kmaline.sup = 10
Traceback (most recent call last):
...
ValueError: Option name sup was not found.
>>> kmaline.custom_args = "-sup 10 --MEH"
>>> str(kmaline)# doctest:+ELLIPSIS
'kma  -sup 10 --MEH -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/aminoglycoside -t_db .../../../../data/tests/datasets/aminoglycosideCT -Sparse'
>>> std_output, err_output = kmaline()# doctest:+ELLIPSIS
Traceback (most recent call last):
...
cgelib.applications.command.ApplicationError: Non-zero return code 1 from 'kma  -sup 10 --MEH -i .../../../../data/tests/raw_reads/test2_R1.fq .../../../../data/tests/raw_reads/test2_R2.fq  -o .../../../../data/tests/alignment_files/aminoglycoside -t_db .../../../../data/tests/datasets/aminoglycosideCT -Sparse', with the error message:
                   Invalid option:	-sup
>>> print(std_output)
<BLANKLINE>
>>> print(err_output)# doctest:+ELLIPSIS
# Reading inputfile: 	.../../../../data/tests/raw_reads/test2_R1.fq
# Phred scale:	33
# Reading inputfile: 	.../../../../data/tests/raw_reads/test2_R2.fq
# Phred scale:	33
#
# Query converted
#
# Running KMA.
#
# Total time used for DB loading: 0.00 s.
#
# Finding k-mer ankers
# Query ankered
#
# KMA mapping done
#
# Sort, output and select KMA alignments.
# Total time for sorting and outputting KMA alignment	0.00 s.
#
# Doing local assemblies of found templates, and output results
# Total time used for local assembly: 0.00 s.
#
# Closing files

```
