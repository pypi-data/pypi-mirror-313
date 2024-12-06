# Test ParserDict class

## imports

```python

>>> from cgecore.output.parserdict import ParserDict
>>> from cgecore.output.valueparsers import ValueParsers
>>> from cgecore.output.test_data.test_val_parse_fail import CustomValueParsers

```

## ParserDict(input_parser)

```python

>>> default_parser = ParserDict()
>>> default_parser["char64"]("54d762f5aacbd706457d109d520e3c550feb8df"
...                          "edc4f0d8ccae1ad203e3388c0")

>>> parser_class = ValueParsers
>>> custom_parser = ParserDict(parser_class)
>>> custom_parser["char64"]("54d762f5aacbd706457d109d520e3c550feb8df"
...                         "edc4f0d8ccae1ad203e3388c0")

>>> custom_parser_fail = CustomValueParsers
>>> val_parser_list = ParserDict.get_method_names(custom_parser_fail)

>>> try:
...    ParserDict(custom_parser_fail)
... except SyntaxError as e:
...    print(e)
A function in the CustomValueParsers class did not start with 'parse_'. Function is named: char64

```

### Methods

## get_method_names(cls)

```python

>>> parser_class = ValueParsers
>>> val_parser_list = ParserDict.get_method_names(parser_class)

```
