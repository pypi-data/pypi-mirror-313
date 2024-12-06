
Information: You always have to input files for the class FindCommonRegion where both are dictionaries and contain the alignment information of the resistance genes from resfinder and pointfinder respectively. The goal is to combine the acquired resistance genes and the chromosomal resistance genes in one file.


## Import 

```
>>> from src.resfinder.seq_region.seq_region_finder import FindCommonRegion

```


### Test overlap two sequences

- Take a look at the the start and end position of the query string. They overlap and the expected result is that the Common region finder will merge them so that the rest of string 2 is added to the merged string.

- Furthermore, take a look at the third key. The contig is different than to the other two. Therefore, this should not be included in the merge and should appear as separate item in the output dictionary.


```
>>> test_A1 = {"beta-lactam": {"bbbbbbb sdf-2_jkle2kdsfjksldfka": {"query_string": "AAA", "sbjct_string": "AAA", "query_end": 3, "query_start": 1}, "aaaaaaa sdf-3_jkle2kdsfjksldfka": {"query_string": "AAB", "sbjct_string": "AAB", "query_end": 4, "query_start": 2},"fffffff fff-3_jkle2kdsfjksldfka": {"query_string": "CCC", "sbjct_string": "CCC", "query_end": 3, "query_start": 1}}}
>>> A = FindCommonRegion(test_A1)
>>> A.merged_query_string()
>>> merged_object = A.merged_seq_region
>>> beta_lactam = merged_object["beta-lactam"]
>>> assert beta_lactam['sdf'].get("query_string") == "AAAB"
>>> assert beta_lactam['fff'].get("query_string") == "CCC"
>>> assert beta_lactam['sdf'].get("query_start") == 1
>>> assert beta_lactam['sdf'].get("query_end") == 4

```

### Test that non overlap but same contig works

- Now, take a look at the start and end position. They do not overlap. In fact, they have an empty region in between. In this case the software should insert one dash! 

```
>>> test_A1 = {"beta-lactam": {"abcdefg sdf-2_jkle2kdsfjksldfka": {"query_string": "AAA", "sbjct_string": "AAA", "query_end": 3, "query_start": 1}, "abcdefg sdf-3_jkle2kdsfjksldfka": {"query_string": "AAB", "sbjct_string": "AAB", "query_end": 7, "query_start": 5},"abcdefg fff-3_jkle2kdsfjksldfka": {"query_string": "CCC", "sbjct_string": "CCC", "query_end": 3, "query_start": 1}}}
>>> A = FindCommonRegion(test_A1)
>>> A.merged_query_string()
>>> merged_object = A.merged_seq_region
>>> beta_lactam = merged_object["beta-lactam"]
>>> assert beta_lactam['sdf'].get("query_string") == "AAA-AAB", f"current string is {beta_lactam['abcdefg sdf'].get('query_string')}"
>>> assert beta_lactam['sdf'].get("query_start") == 1, f"current start is {beta_lactam['abcdefg sdf'].get('query_start')}"
>>> assert beta_lactam['sdf'].get("query_end") == 7, f"current end is {beta_lactam['abcdefg sdf'].get('query_end')}"

```


### Test three fragments on same contig

- this tests the indexing of the sequences and the position ultimately and tests that it works with more than two elements.

- also both aspects from above are combined where seq1 and seq2 are separated by a dash and seq2 and seq3 should be merged.

```
>>> test_A1 = {"beta-lactam": {"abcdefg sdf-2_jkle2kdsfjksldfka": {"query_string": "AAA", "sbjct_string": "AAA", "query_end": 3, "query_start": 1}, "abcdefg sdf-3_jkle2kdsfjksldfka": {"query_string": "AAB", "sbjct_string": "AAB", "query_end": 7, "query_start": 5},"abcdefg fff-3_jkle2kdsfjksldfka": {"query_string": "CCC", "sbjct_string": "CCC", "query_end": 3, "query_start": 1}, "abcdefg sdf-1_jkle2kdsfjksldfka": {"query_string": "EEE", "sbjct_string": "AAA", "query_end": 8, "query_start": 6}}}
>>> A = FindCommonRegion(test_A1)
>>> A.merged_query_string()
>>> merged_object = A.merged_seq_region
>>> beta_lactam = merged_object["beta-lactam"]
>>> assert beta_lactam['sdf'].get("query_string") == "AAA-AABE", f"current string is {beta_lactam['abcdefg sdf'].get('query_string')}"
>>> assert beta_lactam['sdf'].get("query_start") == 1, f"current start is {beta_lactam['abcdefg sdf'].get('query_start')}"
>>> assert beta_lactam['sdf'].get("query_end") == 8, f"current end is {beta_lactam['abcdefg sdf'].get('query_end')}"

```