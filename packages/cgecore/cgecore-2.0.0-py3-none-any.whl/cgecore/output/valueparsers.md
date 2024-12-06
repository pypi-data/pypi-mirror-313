# ValueParsers class

TODO: Write documentation for ValueParsers.

```python

>>> from cgecore.output.valueparsers import ValueParsers

### Test ValueParsers.parse_bool_or_unknown
>>> ValueParsers.parse_bool(True)
>>> ValueParsers.parse_bool(False)
>>> ValueParsers.parse_bool("True")
>>> ValueParsers.parse_bool("False")
>>> ValueParsers.parse_bool("unknown")
'Value must be a boolean (True/False). Value was: unknown'
>>> ValueParsers.parse_bool(0)
'Value must be a boolean (True/False). Value was: 0'

### Test ValueParsers.parse_bool_or_unknown
>>> ValueParsers.parse_bool_or_unknown(True)
>>> ValueParsers.parse_bool_or_unknown(False)
>>> ValueParsers.parse_bool_or_unknown("True")
>>> ValueParsers.parse_bool_or_unknown("False")
>>> ValueParsers.parse_bool_or_unknown("Unknown")
>>> ValueParsers.parse_bool_or_unknown("unknown")
>>> ValueParsers.parse_bool_or_unknown(0)
'Value must be a boolean (True/False) or unknown. Value was: 0'

### Test ValueParsers.parse_char64
>>> ValueParsers.parse_char64("54d762f5aacbd706457d109d520e3c550feb8df"
...                           "edc4f0d8ccae1ad203e3388c0")
>>> ValueParsers.parse_char64("String of char size 22")
'This field expects a string of lenght 64 but the lenght of the string is 22. The string is: String of char size 22'

### Test ValueParsers.parse_date
>>> ValueParsers.parse_date("2020-08-25")
>>> ValueParsers.parse_date("Not a date")
'Date format not recognised. Date format must adhere to the ISO 8601 format (YYYY-MM-DD). Provided value was: Not a date'

### Test ValueParsers.parse_integer
>>> ValueParsers.parse_integer("20")
>>> ValueParsers.parse_integer("Not an integer")
'Value must be an integer. Value was: Not an integer'

### Test ValueParsers.parse_percentage
>>> ValueParsers.parse_percentage("20")
>>> ValueParsers.parse_percentage(20)
>>> ValueParsers.parse_percentage(500)
'Percentage value must be between 0 and 100. The value was: 500.0'
>>> ValueParsers.parse_percentage("Not a percentage")
'Value must be a number. Value was: Not a percentage'

### Test ValueParsers.parse_string
>>> ValueParsers.parse_string("some string")

### Test ValueParsers.parse_float
>>> ValueParsers.parse_float("20.6")
>>> ValueParsers.parse_float(20.6)
>>> ValueParsers.parse_float("Not a number")
'Value must be a float. Value was: Not a number'
>>> ValueParsers.parse_float("20,6")
'Value must be a float. Value was: 20,6'

```
