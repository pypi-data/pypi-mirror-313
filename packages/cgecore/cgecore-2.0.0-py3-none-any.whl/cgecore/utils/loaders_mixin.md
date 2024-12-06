# LoadersMixin Tests

```python

>>> from cgecore.utils.loaders_mixin import LoadersMixin

```

## load_md_table_after_keyword

```python

>>> import os.path
>>> import inspect
>>> loadersmixin_file = inspect.getfile(LoadersMixin)
>>> loadersmixin_dir = os.path.dirname(os.path.realpath(loadersmixin_file))
>>> md_test_file = ("{}/../../../tests/test_table.md".format(loadersmixin_dir))

>>> table_dict = LoadersMixin.load_md_table_after_keyword(
...     md_test_file, "## Abbreviations")

>>> len(table_dict)
3
>>> table_dict["Ceftobiprole"]
['2', 'CTO']

```

## load_md_table_to_dict

```python

>>> md_table = """
... | Antimicrobial                 | Abbreviation |
... |-------------------------------|--------------|
... | Amikacin                      | AMI          |
... | Amoxicillin                   | AMO          |
... | Amoxicillin-clavulanate       | AMC          |
... | Ampicillin                    | AMP          |
... | Ampicillin-sulbactam          | AMS          |
... """

>>> md_dict = LoadersMixin.load_md_table_to_dict(md_table)
>>> md_dict["Amikacin"]
['AMI']
>>> md_dict["Ampicillin"][0]
'AMP'

>>> md_table2 = """
... | Antimicrobial          | midheader       | Abbreviation |
... |------------------------|-----------------|--------------|
... | Amikacin               |   1             | AMI          |
... | Amoxicillin            |   2             | AMO          |
... | Amoxicillin-clavulanate|   3             | AMC          |
... | Ampicillin             |   4             | AMP          |
... | Ampicillin-sulbactam   |   5             | AMS          |
... """

>>> md_dict2 = LoadersMixin.load_md_table_to_dict(md_table2, key="midheader")
>>> md_dict2["3"]
['Amoxicillin-clavulanate', 'AMC']

>>> md_dict2 = LoadersMixin.load_md_table_to_dict(md_table2, key="Midheader")
>>> md_dict2["5"]
['Ampicillin-sulbactam', 'AMS']

```

## split_and_clean_str(string=str, delimiter=char)

```python

>>> some_string = "| Cefalexin                     | CLE          |"
>>> clean = LoadersMixin.split_and_clean_str(string=some_string, delimiter="|")
>>> print(clean)
['Cefalexin', 'CLE']

```

## _get_header_index(key=[str|int], headers=list, ignore_case=bool)

```python

>>> headers_list = ["header1", "header2", "key_header", "header_last"]
>>> index = LoadersMixin._get_header_index(1, headers_list, True)
>>> index
1
>>> index = LoadersMixin._get_header_index("key_header", headers_list, False)
>>> index
2
>>> index = LoadersMixin._get_header_index("Key_header", headers_list, True)
>>> index
2

>>> index = LoadersMixin._get_header_index("Key_header", headers_list, False)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
KeyError: "The argument provided as key: Key_header did not match ..."

>>> index = LoadersMixin._get_header_index(10, headers_list, True)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
IndexError: The argument provided as key: 10 was larger or equal to the ...

```
