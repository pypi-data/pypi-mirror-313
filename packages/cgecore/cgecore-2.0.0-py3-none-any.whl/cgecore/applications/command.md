
### Testing of Application error

```python

>>> from cgecore.applications.command import ApplicationError
>>> err = ApplicationError(1, "helloworld", "", "Some error text")
>>> err.returncode, err.cmd, err.stdout, err.stderr
(1, 'helloworld', '', 'Some error text')
>>> print(err)
... #doctest: +NORMALIZE_WHITESPACE
Non-zero return code 1 from 'helloworld', with the error message: Some error text
>>> noterr = ApplicationError(1, "helloworld", "Some success text", "")
>>> noterr.returncode, noterr.cmd, noterr.stdout, noterr.stderr
(1, 'helloworld', 'Some success text', '')
>>> print(noterr)
Non-zero return code 1 from 'helloworld'

```
