# Pliers test

```python

>>> import re
>>> from cgecore.utils.pliers_mixin import PliersMixin

>>> version, commit = PliersMixin.get_version_commit(gitdir="./")
>>> len(commit)
40

>>> version, commit = PliersMixin.get_version_commit(gitdir="~/")
>>> commit
'unknown'

>>> version = PliersMixin.get_version_pymodule(name="cgecore")
>>> assert(re.search(r'\d+\.\d+\.\d+', version))

>>> PliersMixin.get_version_database(db_path="/not/real/path")
'unknown'
>>> PliersMixin.get_version_database(db_path="tests/db_folder_test")
'test.test.test'

```
