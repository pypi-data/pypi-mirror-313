# Result class test

```python

>>> from cgecore.output.result import Result, ResultParser
>>> from cgecore.output.exceptions import CGECoreOutTypeError, CGECoreOutInputError

```

## Usage for CGE developers

### Initialize the root Result class for CGE tools

The format of "software_result" and all other results created by the CGE tools
should adhere to the format defined here: [Templates](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/beone/README.md)

All CGE tools should have some common basic information. Hence, this method
should be used to initialize a result object in which the tool will store all
results produces that are meant to be useful for the user of the tool.

```python

>>> res = Result.init_software_result(name="ResFinder", gitdir=".")
>>> res["type"]
'software_result'
>>> res["software_name"]
'ResFinder'

```

### Initialize object for database entries

```python

>>> res["databases"]
{}
>>> res.init_database("ResFinder", ".")
>>> db_key = res.get_db_key("ResFinder")[0]
>>> dbinfo = res["databases"][db_key]
>>> dbinfo["type"]
'database'
>>> dbinfo["database_name"]
'ResFinder'
>>> assert(len(dbinfo["database_commit"]) == 40
...        or dbinfo["database_commit"] == "unknown")

```

## Usage in general

### Initialize Result class

A Result object can be initialized using a dict containing many key-value pairs.
The "type" key is always mandatory, but other key-values depend on the given
template.
```python

>>> res = Result(type="software_result", **{"key1": "val1", "key2": "val2"})
>>> res.val_parsers["char64"]("54d762f5aacbd706457d109d520e3c550feb8df"
...                           "edc4f0d8ccae1ad203e3388c0")

```

When the Result instance is created, the class used to test the format of the
values is also chosen. Per default it is the ValueParsers class.
**Important:** It is the class that is given as argument, not an instance of the
class.
```python

>>> from cgecore.output.valueparsers import ValueParsers
>>> custom_parser = ValueParsers
>>> res = Result(parsers=custom_parser, **{"type": "software_result"})

```

### Initialize ResultParser class

An instance of the Result class loads the json template(s) provided and stores
them in a dict. Each template class is a dict within the dict, and the key is
the class "type".

For each template class an instance of ResultParser is created.

A ResultParser instance is created to hold the definition of a single template
class. The test below uses a previously loaded Result object and provides a dict
from within a dict as argument to ResultParser.

ResultParser is a dict that holds all the definitions from the template class.
Furthermore it detects which values are dictionaries and which values are lists.
It removes the "dict" or "array" part and stores only the rest of the value. But
keeps two dictionaries named "dicts" and "arrays" with the key-value pairs in
order to determine if the value of the key is expected to be a list or a
dictionary.
Values that are not dictionaries or lists are not stored in specific
dictionaries, but just in the "root" dictionary.

```python

>>> res_parser1 = ResultParser(result_def=res.defs["software_result"])
>>> res_parser1["type"]
'software_result'
>>> res_parser1["databases"]
'database:class'
>>> res_parser1.dicts["databases"]
'database:class'
>>> "databases" in res_parser1.dicts
True
>>> "databases" in res_parser1.arrays
False
>>> res_parser2 = ResultParser(result_def=res.defs["seq_region"])
>>> res_parser2["type"]
'seq_region'
>>> res_parser2.arrays["phenotypes"]
'phenotype.key'

```

### Methods

#### Result.add(**kwargs)

Stores key value pairs in result object, where both key and value are single
values. Not lists or dictionaries. The method is designed to store several key
value pairs with a single call provided a dictionary of pairs.
- Keys with 'None' values are ignored.
- Values that does not adhere to the template definition is stored without any
warnings, errors or exceptions. Failure to comply with definitions are found
using the method Result.check_results.

```python

>>> res.add(**{"key1": "val1", "key2": "val2", "key3": None})
>>> res["key1"]
'val1'
>>> res["key3"]
Traceback (most recent call last):
KeyError: 'key3'

```

#### Result.add_class(cl, type, **kwargs)

Classes defined in a template become instances of the Result object. This method
stores a Result instance within a Result instance. Results can be stored in
either dictionaries or arrays, this is defined by the json template and stored
in the ResultParser object within the Result instance.
**cl**: Name/Key of Result instance to store.
**type**: Type of the Result instance to store.
**kwargs**: Dictionary of key value pairs to be content of the Result instance
to store.
- Results stored in a dictionary must contain a key named 'key'.
- Results must be one of the valid types provided in the json template.

```python

>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key": "phen", "key2": "val2"})
>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key1": "phen", "key2": "val2"})
Traceback (most recent call last):
KeyError: 'key'
>>> res.add_class(cl="phenotypes", type=None,
...               **{"key": "phen", "key2": "val2"})
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutTypeError: Unknown result type given.
    Type given: None. Type must be one of: [...]

```

Most result instances will be stored in arrays or dictionaries. However it is
possible to store a result instance at the root level of another Result as shown
below. Also note that the added class will automatically be populated with empty
dictionaries and lists needed to store Results within the added class/Result
that are stored in dictionaries or arrays.

```python

>>> res.add_class(cl="virulencefinder", type="software_result",
...               **{"key": "VirulenceFinder-d48a0fe",
...                  "software_name": "VirulenceFinder",
...                  "software_version": "d48a0fe"})
>>> assert ("virulencefinder" in res)
>>> assert ("software_name" in res["virulencefinder"])
>>> assert ("seq_regions" in res["virulencefinder"])
>>> assert ("databases" in res["virulencefinder"])
>>> assert ("phenotypes" in res["virulencefinder"])
>>> assert ("seq_variations" in res["virulencefinder"])

```

#### Result.check_results(errors, strict)

All values stored in a Result object is defined in a "template". The template
define what type and form the values can be. You can read more about templates
here: [Templates](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/README.md).

This method "check_results" parses all the values stored to check if they adhere
to the given template definitions. Any errors that are encountered are stored in
the calling Result object dictionary named "errors". If no errors are
encountered the dictionary will be empty and the method will return None. If
errors are encountered the errors dictionary will be populated with the keys
in the templates that failed the check and the values will describe why it
failed. If there are failed checks then the method will also raise a
CGECoreOutInputError exception.

The check_results method is recursive and will call the check_results method for
all Result objects stored within the calling Result object via the private
method _check_result. Hence, you only need to invoke check_results for the
"root" Result object.

**Note**: Keys with no definition will per default be accepted. If strict is set
to True, then undefined keys will cause an error.

**Important**: The errors argument should always be left empty. It is only used
by recursive calls.

```python

>>> res = Result(type="software_result",
...              **{"key": "ResFinder-d48a0fe",
...                 "software_name": "ResFinder",
...                 "software_version": "d48a0fe",
...                 "undefined_key": "some value"})
>>> res.check_results()
>>> res.check_results(strict=True)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutInputError: ("Some input data did not pass
    validation... 'undefined_key': 'Key not defined...'...)

```

Test with incorrect date format.

```python

>>> res = Result(type="software_result",
...              **{"key": "ResFinder-d48a0fe",
...                 "software_name": "ResFinder",
...                 "software_version": "d48a0fe",
...                 "run_date": "Nov. 16 2008"})
>>> res.check_results()
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutInputError: ("Some input data did not pass
    validation... 'run_date': 'Date format not rec...'...)

>>> try:
...     res.check_results()
... except CGECoreOutInputError:
...     assert("run_date" in res.errors)
...     print(res.errors["run_date"])
... #doctest: +ELLIPSIS
Date format not rec...

```

Test with nested Result object (recursive call), this test should not pass, see
ToDo. When ToDo is done, rewrite test to pass by adding "category": "amr" to the
add_class dictionary argument.

```python

>>> res = Result(type="software_result",
...              **{"key": "ResFinder-d48a0fe",
...                 "software_name": "ResFinder",
...                 "software_version": "d48a0fe"})
>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key": "vancomycin"})
>>> res.check_results()

```

Test with nested Result object (recursive call) that has incorrect value.

```python

>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key": "lincomycin", "amr_resistant": "invalid value"})
>>> res.check_results()
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutInputError: ("Some input data did not pass
    validation... 'amr_resistant': 'Value must be a bool...'...)

```

#### get_db_key(name)

See "Initialize object for database entries"

#### json_dumps()

```python

>>> json_str = res.json_dumps()
>>> print(len(json_str))
543

```

### Private Methods

#### Result._add_class_dict(cl, res, clobber, clobber_warn)

```python

>>> pheno_res = Result(type="phenotype",
...                    **{"key": "vancomycin", "amr_resistant": True})

>>> res._add_class_dict(cl="phenotypes", res=pheno_res, clobber=False,
...                     clobber_warn=False)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutDuplicateKeyError:
    The add_class would have clobbered an existing non-empty entry. ...

>>> res["phenotypes"]["vancomycin"].get("amr_resistant", None) is None
True

´´´

Test clobber warning. The cgelib package writes warnings using the logging
module, which is why the doctest needs to add a StreamHandler in order to
capture the warning.

´´´python

>>> import sys
>>> import logging
>>> logger = logging.getLogger()
>>> logger.addHandler(logging.StreamHandler(sys.stdout))
>>> res._add_class_dict(cl="phenotypes", res=pheno_res, clobber=True,
...                     clobber_warn=True)
In phenotypes. Clobbered entry with the key: vancomycin.

>>> res["phenotypes"]["vancomycin"]["amr_resistant"]
True

>>> pheno_res_false = Result(type="phenotype",
...                          **{"key": "vancomycin", "amr_resistant": False})
>>> res._add_class_dict(cl="phenotypes", res=pheno_res_false, clobber=True,
...                     clobber_warn=False)

>>> res["phenotypes"]["vancomycin"]["amr_resistant"]
False

```

#### Result._set_type(*type*)

Set *type* of Result object if it is valid. If not, throw exception:
CGECoreOutTypeError.

```python

>>> res._set_type(type="Not valid type")
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutTypeError:
    Unknown result type given. Type given: Not valid type.
    Type must be one of: [...]
>>> res._set_type("software_result")

```

#### Result._check_result(key, val, errors, index)

## Exceptions

Result must be initialized with a "type". Otherwise an exception is thrown.
```python

>>> res = Result()
... #doctest: +NORMALIZE_WHITESPACE
Traceback (most recent call last):
TypeError: Result.__init__() missing 1 required positional argument: 'type'

```

The "type" given must be defined in the json template provided. These are found
in the "templates_json" folder. If not an exception is thrown and the possible
types of the given json is listed. In the test the exact types has been left out
and replaced with "...".
```python

>>> res = Result(type="some_type")
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Traceback (most recent call last):
cgecore.output.exceptions.CGECoreOutTypeError:
    Unknown result type given. Type given: some_type. Type must be one of: [...]

```

# Result class ToDos and suggestions

## ToDo

### Implement vocabulary

Should not give an error

```python

>>> res = Result(type="software_result",
...              **{"key": "ResFinder-d48a0fe",
...                 "software_name": "ResFinder",
...                 "software_version": "d48a0fe"})
>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key": "vancomycin", "category": "amr"})
>>> res.check_results()

```

### Required keys does not give an error if missing

Should give an error since category is missing

```python

>>> res = Result(type="software_result",
...              **{"key": "ResFinder-d48a0fe",
...                 "software_name": "ResFinder",
...                 "software_version": "d48a0fe"})
>>> res.add_class(cl="phenotypes", type="phenotype",
...               **{"key": "vancomycin"})
>>> res.check_results()

```

## Suggestions

- If trying to add a class with a key/name close to existing, raise a warning.
