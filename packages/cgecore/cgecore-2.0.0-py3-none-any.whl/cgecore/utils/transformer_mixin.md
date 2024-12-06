# TransformerMixin test

## userdict_to_dict(userdict)

### Setup

```python

>>> import json
>>> from collections import UserDict
>>> from cgecore.utils.transformer_mixin import TransformerMixin

>>> mydict = UserDict()
>>> mydict["key1"] = "val1"
>>> mydict["key2"] = "val2"
>>> mydict["userdict1"] = UserDict()
>>> mydict["userdict1"]["ukey1"] = "uval1"
>>> mydict["userdict1"]["ukey2"] = "uval2"
>>> mydict["userdict1"]["ukey3"] = "uval3"
>>> mydict["userdict1"]["userdict_inner"] = UserDict()
>>> mydict["userdict1"]["userdict_inner"]["inner_key1"] = "inner_val1"
>>> mydict["userdict1"]["userdict_inner"]["inner_key2"] = "inner_val2"
>>> mydict["userdict1"]["userdict_inner"]["inner_key3"] = "inner_val3"
>>> mydict["userdict1"]["builtin_inner"] = {
...   "builtin_key1": "builtin_val1",
...   "builtin_key2": "builtin_val2",
...   "builtin_key3": "builtin_val3",
... }
>>> mydict["key3"] = "val3"
>>> mydict["empty"] = UserDict()
>>> mydict["list"] = [1, 2, 3]

```

### Test

```python

>>> builtin_dict = TransformerMixin.userdict_to_dict(mydict)
>>> print(type(builtin_dict["userdict1"]))
<class 'dict'>
>>> print(type(builtin_dict["userdict1"]["userdict_inner"]))
<class 'dict'>
>>> print(type(builtin_dict["userdict1"]["builtin_inner"]))
<class 'dict'>
>>> json_str = json.dumps(builtin_dict)
>>> builtin_dict["key1"]
'val1'
>>> builtin_dict["key2"]
'val2'
>>> builtin_dict["key3"]
'val3'
>>> builtin_dict["userdict1"]["ukey1"]
'uval1'
>>> builtin_dict["userdict1"]["ukey2"]
'uval2'
>>> builtin_dict["userdict1"]["ukey3"]
'uval3'
>>> builtin_dict["userdict1"]["userdict_inner"]["inner_key1"]
'inner_val1'
>>> builtin_dict["userdict1"]["userdict_inner"]["inner_key2"]
'inner_val2'
>>> builtin_dict["userdict1"]["userdict_inner"]["inner_key3"]
'inner_val3'
>>> builtin_dict["userdict1"]["builtin_inner"]["builtin_key1"]
'builtin_val1'
>>> builtin_dict["userdict1"]["builtin_inner"]["builtin_key2"]
'builtin_val2'
>>> builtin_dict["userdict1"]["builtin_inner"]["builtin_key3"]
'builtin_val3'
>>> builtin_dict["empty"]
{}
>>> builtin_dict["list"]
[1, 2, 3]

```
