import json

from pyxp import var, val, from_json, context


def test_basic_usecase():
    f = var.f
    g = var.g
    a = var.a

    exp = f(10, 10) + g(f(a + 1, 2)) + 1

    ctx = context({
        'f': lambda x, y: x * y,
        'g': lambda x: x * 2,
        'a': 1
    })

    result = exp.calc(ctx)
    assert result == 109


def test_serialization():
    f = var.f
    g = var.g
    a = var.a

    exp = f(10, 10) + g(f(a + 1, 2)) + 1

    json_str = exp.to_json()
    print json_str
    exp_deserialized = from_json(json_str)

    assert exp.to_lisp_code() == exp_deserialized.to_lisp_code()
