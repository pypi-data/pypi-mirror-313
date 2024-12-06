# Test of exception classes

```python

>>> from cgecore.output.exceptions import (CGECoreOut, CGECoreOutTypeError,
...                                        CGECoreOutInputError,
...                                        CGECoreOutTranslateError)


```

## Test CGECoreOutTypeError

```python

>>> try:
...    raise CGECoreOutTypeError("Raised CGECoreOutTypeError")
... except CGECoreOutTypeError as e:
...    print(e.message)
Raised CGECoreOutTypeError

```

## Test CGECoreOutInputError

```python

>>> try:
...    errs = ["err1", "err2"]
...    raise CGECoreOutInputError("Raised CGECoreOutInputError", errs)
... except CGECoreOutInputError as e:
...    print(e.message)
...    print(e.errors)
Raised CGECoreOutInputError
['err1', 'err2']

```

## Test CGECoreOutTranslateError

```python

>>> try:
...    raise CGECoreOutTranslateError("Raised CGECoreOutTranslateError")
... except CGECoreOutTranslateError as e:
...    print(e.message)
Raised CGECoreOutTranslateError

```

## Test CGECoreOut

```python

>>> try:
...    raise CGECoreOutTypeError("Raised CGECoreOut")
... except CGECoreOut as e:
...    print("Raised CGECoreOut")
Raised CGECoreOut

```

## TODO
* Elaborate on tests
