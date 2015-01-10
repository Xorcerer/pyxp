# pyxp
Python library for construct arithmetic expression (including function calls),
which can be serialize to/deserialize from json.


## Installation

    easy_install pyxp
    
or

    pip install pyxp

## Example

```python

# Functions and variables sharing the same namespace.
context_ = context(
    a=10,
    b=2,
    double=lambda x: x * 2,
    add=lambda x, y: x + y,
    my_sum=lambda *args: sum(args),
)

# Expression variables could be assign to python variables to use later,
# or use them inline, see 'val.my_sum'.
double = val.double
add = val.add
a = val.a
b = val.b

exp = double(a + b) + add(a, b) - (val.my_sum(a, b) << 1)

actual = exp.calc(context_)
assert actual == 12

# Serialize to string, so you could send over network. 
json_str = exp.to_json()

# Deserialization
exp_deserialized = from_json(json_str)

```

More examples
[Test Cases](tests/exps.py)
