# pyxp
Python library for construct arithmetic expression (including function calls),
which can be serialized to/deserialized from json.

## Cases
* Console game *DUST 514* by *CCP*, on PlayStation, used for formula updating.

## Installation

    easy_install pyxp
    
or

    pip install pyxp

## Example

### Construct Expression, Serialization/Deserialization.
```python

from pyxp import val, from_json, context

# Expression variables could be assign to python variables to use later,
# or use them inline, see 'val.my_sum'.
double = val.double
add = val.add
a = val.a
b = val.b

exp = double(a + b) + add(a, b) - (val.my_sum(a, b) << 1)

# Serialize to string, so you could send it over network. 
json_str = exp.to_json()

# Deserialization
exp_deserialized = from_json(json_str)
```

### Calculation

```python

# Functions and variables sharing the same namespace.
context_ = context(
    a=10,
    b=2,
    double=lambda x: x * 2,
    add=lambda x, y: x + y,
    my_sum=lambda *args: sum(args),
)

actual = exp.calc(context_)
assert actual == 12


```

More examples
[Test Cases](tests/exps.py)
