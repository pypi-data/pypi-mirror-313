###Testing of BLASTNCommandLineBase
```python3
>>> ### Get the location of the test data ####
>>> import os
>>> loc_py = os.getcwd()
>>> loc_data = loc_py + "/../../../data/tests"
>>> ### Import Module ###
>>> from cgecore.applications.Blast import BlastNCommandline
>>> ### Good run ###
>>> blastnline = BlastNCommandline(subject="%s/datasets/aminoglycoside.fsa"%loc_data, query="%s/assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2amino5.xml"%loc_data, outfmt="5 std qlen", perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline()
>>> print("STD_Output: ", std_output)
STD_Output:
>>> print("ERR_Output: ", err_output)
ERR_Output:
>>> print(blastnline())
('', '')
>>> print(blastnline)# doctest:+ELLIPSIS
blastn -query .../../../../data/tests/assembled_data/test2.fsa -out .../../../../data/tests/alignment_files/blasttest2amino5.xml -subject .../../../../data/tests/datasets/aminoglycoside.fsa -max_target_seqs 50000 -outfmt 5 -dust no -perc_identity 0.9
>>> ### More tests ###
>>> blastnline = BlastNCommandline(subject="%s/datasets/beta-lactam.fsa"%loc_data, query="%s/assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2betalactam5.xml"%loc_data, outfmt=5, perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline()
>>> blastnline = BlastNCommandline(subject="%s/datasets/colistin.fsa"%loc_data, query="%s/assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2colistin5.xml"%loc_data, outfmt=5, perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline()
>>> blastnline = BlastNCommandline(subject="%s/datasets/fosfomycin.fsa"%loc_data, query="%s/assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2fosfomycin5.xml"%loc_data, outfmt=5, perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline()
>>> ### Try SwitchArgument ###
>>> blastnline.ungapped = True
>>> std_output, err_output = blastnline()
>>> ### Try wrong path ###
>>> blastnline_wrong = BlastNCommandline(subject="%s/datasets/aminoglycoside.fsa"%loc_data, query="%s/../assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2amino5.xml"%loc_data, outfmt=5, perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline_wrong()# doctest:+ELLIPSIS
Traceback (most recent call last):
...
cgelib.applications.command.ApplicationError: Non-zero return code 1 from 'blastn -query .../../../../data/tests/../assembled_data/test2.fsa -out .../../../../data/tests/alignment_files/blasttest2amino5.xml -subject .../../../../data/tests/datasets/aminoglycoside.fsa -max_target_seqs 50000 -outfmt 5 -dust no -perc_identity 0.9', with the error message:
                   'Command line argument error: Argument "query". File is not accessible:  `.../../../../data/tests/../assembled_data/test2.fsa\''

>>> ### Try wrong incompatible ###
>>> blastnline_wrong.db = "./sup"
>>> std_output, err_output = blastnline_wrong()
Traceback (most recent call last):
...
ValueError: Parameter 'subject' is set, but the incompatible parameter 'db' has been also set.
>>> del blastnline_wrong.db
>>> ### Try wrong value ###
>>> blastnline_wrong.off_diagonal_range = -12
Traceback (most recent call last):
...
ValueError: Invalid parameter value -12 for parameter off_diagonal_range
>>> ### Try missing required argument ###
>>> blastnline_miss = BlastNCommandline(query="%s/../assembled_data/test2.fsa"%loc_data, output="%s/alignment_files/blasttest2amino5.xml"%loc_data, outfmt=5, perc_identity=0.9, max_target_seqs=50000, dust="no")
>>> std_output, err_output = blastnline_miss()
Traceback (most recent call last):
...
ValueError: Parameter db is not set. Neither alternative parameters as subject, subject_loc.
