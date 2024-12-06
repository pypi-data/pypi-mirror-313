Hit class test
=================

### Testing results

```python
>>> from cgecore.sequence.SeqHit import AlnHit, BlastnHit, KMAHit
>>> kmahit = KMAHit()
>>> kmahit["evalue"] = 0.3
>>> kmahit["templateID"] = "Templatekma1"
>>> kma3hit = KMAHit()
>>> kma3hit["coverage"] = 80.
>>> kma3hit["query_coverage"] = 80.
>>> kma3hit["templateID"] = "Templatekma1"
>>> print(kma3hit)
>>> new_hit = KMAHit.merge_hits([kmahit, kma3hit])
>>> print(new_hit)
>>> print(kmahit)
>>> kmahit.add_hit(kma3hit)
>>> print(kmahit)
>>> kmahit2 = KMAHit()
>>> kmahit2["evalue"] = 0.4
>>> kmahit2["templateID"] = "Templatekma1"
>>> kmahit.add_hit(kmahit2)
>>> print(kmahit)
>>> kmahit4 = KMAHit()
>>> kmahit4["mismatch"] = 1
>>> kmahit4["templateID"] = "Templatekma2"
>>> kmahit.add_hit(kmahit4)
>>> print(kmahit)
>>> kmahit5 = KMAHit()
>>> kmahit5["aln_scheme"] = 0.4
>>> print(kmahit5)
```
