from functools import partial
from pyxp import val, from_json, context


def test_basic_usecase():
    # Functions and variables sharing the same namespace.
    context_ = context(
        a=10,
        b=2,
        double=lambda x: x * 2,
        add=lambda x, y: x + y,
        my_sum=lambda *args: sum(args),
    )

    # Expression variables could be assign to python variables to use later,
    # or use them inline, see `val.my_sum`.
    double = val.double
    add = val.add
    a = val.a
    b = val.b

    exp = double(a + b) + add(a, b) - val.my_sum(a, b) * 2

    actual = exp.calc(context_)
    assert actual == 12

    # Serialization
    json_str = exp.to_json()

    # Deserialization
    exp_deserialized = from_json(json_str)

    # To lisp like expression string.
    assert exp.to_lisp_code() == exp_deserialized.to_lisp_code()


def _test_exp(context_, exp, expected):
    actual = exp.calc(context_)
    assert actual == expected, 'Error calculating exp: ' + exp.to_lisp_code()

    json_str = exp.to_json()
    exp_deserialized = from_json(json_str)

    assert exp.to_lisp_code() == exp_deserialized.to_lisp_code()


def test_basic_operators():
    context_ = context(
        a = 10,
        b = 2,
    )
    t = partial(_test_exp, context_)

    a = val.a
    b = val.b

    # The following 2 exps should result the same.
    # For the python operator overriding rule,
    # we have to replace `2` with `val(2)` if it is the lhs.
    t(val(2) + a, 12)
    t(a + 2, 12)

    t(a + b, 12)
    t(a * b, 20)
    t(a / b, 5)
    t(a ** b, 100)
    t(a << b, 40)
    t(a >> b, 2)


def test_complex_exps():
    context_ = context(
        a=10,
        b=2,
        double=lambda x: x * 2,
        add=lambda x, y: x + y,
        my_sum=lambda *args: sum(args),
    )
    t = partial(_test_exp, context_)

    double = val.double
    add = val.add
    my_sum = val.my_sum

    a = val.a
    b = val.b

    t(double(a + b) + add(a, b) - my_sum(a, b), 24)
    t(my_sum(1, 2, 3, 4, a - b, my_sum(a, b)), 30)
