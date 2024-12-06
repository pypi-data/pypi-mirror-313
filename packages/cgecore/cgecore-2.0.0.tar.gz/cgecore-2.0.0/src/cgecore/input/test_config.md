

## Imports


```python
>>> from .config import Config
>>> from .handling_args import CGEArgumnents

```

## Parse Args

```python
>>> def collect_args(argv):
...     ArgumentHandler = CGEArgumnents(program_description="test")
...     ArgumentHandler.fasta_input()
...     parser = ArgumentHandler.parser
...     args = parser.parse_args(argv)
...     return args, parser

```

```python
>>> args, parser = collect_args(["--inputfasta", "/home/people/s220672/resfinder/tests/data/test_isolate_01.fa"])
>>> Config(args, "resfinder", ".")

```
