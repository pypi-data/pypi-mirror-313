# Templates

## Introduction

Output from CGE tools are written into
[JSON](https://en.wikipedia.org/wiki/JSON) formatted files. The output is in
addition to being JSON formatted further defined in a set of definition files
(templates), which are also JSON formatted.  
The templates describe how to read the output from the CGE tools. A
python module has also been developed, that can be used to read CGE JSON files
into python objects. But more importantly the module is implemented by the
CGE tools to write output JSON files that adhere to the definitions provided.
In order to change or add to the CGE tools output, one just needs to alter the
template that defines the results that needs to be output.

## Definitions

The idea is that several templates can exist, but at the moment there is only
one, and we hope to keep it this way.

A template consists of one or more JSON files. A template consists of one or
more dictionaries (associative arrays/hashes/maps). Each JSON file should
contain at least one dictionary, but are allowed to contain several
dictionaries.

### Classes

Dictionaries should always be defined at root level in the JSONs. We refer to
them as classes. Each class is meant to store data of a specific type.
For example annotated genes could be a type, and this class could hold
information on gene name, function etc.

Information is stored as key-value pairs. In the template, the key defines the
literal name of the key in the output. The value defines what kind of output
to expect. The definition of kinds of output is written in detail in the
"Values" section.

**Simple class example**
```json

{
  "gene": {
    "type": "gene",
    "key": "string*",
    "name": "string",
    "function": "string"
  }
}

```

**Obligatory class fields**  

- **type**: should be identical to the class name (gene in the example above).
- **key**: A string that uniquely identifies an entry of the type gene.

Classes can also be stored within classes. Classes can be stored in either
lists/arrays or dictionaries. For example, a class called "software_result"
could collect information stored in the previously defined gene class. Below is
an example where the software_result class defines a key called "genes" to store
a dictionary of gene classes.

**Class in class example**
```json

{
  "software_result": {
    "type": "software_result",
    "key": "string*",
    "genes": "dict gene:class"
  }
}

```

The key name can be any valid json key, in the above example it is "genes". The
value needs to adhere to a specific format if it stores another class.

**Class in class field format**  

1. First word must be either "dict" or "array". It defines the data structure the
class should be stored in, dictionary or array/list, respectively.
2. After the first word must follow a white space character.
3. Following the white space character must be a string following the format:
<class_type>:class, where <class_type> is identical to the type value in the
respective class that is to be stored.

### Values

In the templates the values, with the exception of the "type" value, defines
the types of output that are expected in the field. Most value types are also
associated to a value parser, it creates warnings if values does not adhere
to their definition.

#### Value Parsers

Each value definition that has a corresponding function in the "ValueParsers"
class, will be checked using that function.

**How to add a new value definition**  

1. Make sure the name of the value definition does not already exist from the
table below named "Value Definitions". Add it to the table (this file) and push
the change to the repository (to make sure no one uses that name).
2. Add a function to the "ValueParsers" class named "parse_<val_name>", where
val_name is the name of the value definition. See [ValueParsers](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/valueparsers.md) for more details.

#### Obligatory Values

A value can always be made obligatory by ending it with an asterixis (*)

#### Cross-Reference Values

All values must belong to a single class. However, if several classes need to
store the same value, it can be defined by using dot annotation. The format is:
<origin_class>.<key>. This defines that the value stored here is identical
to a value stored in the class of type <origin_class> with the key named <key>.

**Cross-Reference Example**
```json

{
  "mutation": {
    "type": "mutation",
    "key": "string*",
    "gene": "gene.name"
  }
}

```

## Value Definitions

| Value name      | Definition                                        |
| :-------------- | ------------------------------------------------: |
| string          | Basically anything can appear in this field.      |
| integer         | Integer values.                                   |
| char64          | String of exactly 64 characters (ex.: checksums). |
| date            | ISO 8601 format (ex.: 2003-03-20).                |
| percentage      | Float between 0 and 100.                          |
| float           | Floating-point number.                            |
| bool            | True or False                                     |
| bool_or_unknown | True, False or Unknown (not case sensitive)       |

## BeOne template

The default definition for all CGE tools. Named BeOne after the collaboration in
which it was developed.  
**Detailed description**:
[BeOne definition](https://bitbucket.org/genomicepidemiology/cge_core_module/src/2.0/cge2/output/templates_json/beone/)
