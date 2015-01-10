import json as json_lib
import operator


class Node(object):
    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        return json_lib.dumps(self.to_dict())

class Literal(Node):
    def __init__(self, value):
        self.value = value

    def calc(self, context):
        return self.value

    def to_lisp_code(self):
        return str(self.value)

    def to_dict(self):
        return {'type': 'Literal', 'value': self.value}

    @staticmethod
    def from_dict(d):
        return Literal(d['value'])

    def __repr__(self):
        return 'Literal(%s)' % self.value


class Variable(Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def calc(self, context):
        return context[self.var_name]

    def to_lisp_code(self):
        return self.var_name

    def to_dict(self):
        return {'type': 'Variable', 'var_name': self.var_name}

    @staticmethod
    def from_dict(d):
        return Variable(d['var_name'])

    def __repr__(self):
        return 'Variable(%s)' % self.var_name


class Function(Node):
    def __init__(self, func_name, params=()):
        self.func_name = func_name
        self.params = params

    def calc(self, context):
        f = context[self.func_name]
        params = [p.calc(context) for p in self.params]
        return f(*params)

    def to_lisp_code(self):
        params_str = ' '.join([p.to_lisp_code() for p in self.params])
        return '(%s %s)' % (self.func_name, params_str)

    def to_dict(self):
        return {'type': 'Function', 'func_name': self.func_name,
                'params': [p.to_dict() for p in self.params]}

    @staticmethod
    def from_dict(d):
        return Function(d['func_name'],
                        params=[from_dict(p) for p in d['params']])

    def __repr__(self):
        return self.to_lisp_code()

types = {
    'Literal': Literal,
    'Variable': Variable,
    'Function': Function,
}


class Factor(object):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value or Variable(name)

    def __call__(self, *args):
        value = Function(self.name, [self.to_node(a) for a in args])
        return Factor(self.name, value)

    def op(self, symbol, other):
        value = Function(symbol, [self.value, self.to_node(other)])
        return Factor(None, value)

    def __add__(self, other):
        return self.op('+', other)

    def __sub__(self, other):
        return self.op('-', other)

    def __mul__(self, other):
        return self.op('*', other)

    def __div__(self, other):
        return self.op('/', other)

    def __pow__(self, power, modulo=None):
        return self.op('**', power)

    def calc(self, context):
        return self.value.calc(context)

    def to_dict(self):
        return self.value.to_dict()

    def to_json(self):
        return self.value.to_json()

    def to_lisp_code(self):
        return self.value.to_lisp_code()

    @staticmethod
    def to_node(token):
        if isinstance(token, Factor):
            assert token.value is not None
            return token.value

        return Literal(token)


class FactorFactory(object):
    def __getattr__(self, item):
        return Factor(item)

    def __literal(self, value):
        return Factor(None, Literal(value))


var = FactorFactory()
val = var.__literal


def from_dict(d):
    node_type = types[d['type']]
    return node_type.from_dict(d)


def from_json(json_str):
    return from_dict(json_lib.loads(json_str))


DEFAULT_CONTEXT = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div,
    '**': operator.pow,
    '<<': operator.ilshift,
    '>>': operator.irshift,
}

def context(context_dict):
    r = dict(DEFAULT_CONTEXT)
    r.update(context_dict)
    return r
