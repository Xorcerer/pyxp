import json


class Node(object):
    @staticmethod
    def from_json(json):
        node_type = types[json['type']]
        return node_type.from_json(json)


class Literal(Node):
    def __init__(self, value):
        self.value = value

    def calc(self, context):
        return self.value

    def to_code(self):
        return str(self.value)

    def to_json(self):
        return {'type': 'Literal', 'value': self.value}

    @staticmethod
    def from_json(json):
        return Literal(json['value'])

    def __repr__(self):
        return 'Literal(%s)' % self.value


class Variable(Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def calc(self, context):
        return context[self.var_name]

    def to_code(self):
        return self.var_name

    def to_json(self):
        return {'type': 'Variable', 'var_name': self.var_name}

    @staticmethod
    def from_json(json):
        return Variable(json['var_name'])

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

    def to_code(self):
        params_str = ' '.join([p.to_code() for p in self.params])
        return '(%s %s)' % (self.func_name, params_str)

    def to_json(self):
        return {'type': 'Function', 'func_name': self.func_name,
                'params': [p.to_json() for p in self.params]}

    @staticmethod
    def from_json(json):
        return Function(json['func_name'],
                        params=[Node.from_json(p) for p in json['params']])

    def __repr__(self):
        return self.to_code()

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

    def calc(self, context):
        return self.value.calc(context)

    def to_json(self):
        return self.value.to_json()

    def to_code(self):
        return self.value.to_code()

    @staticmethod
    def to_node(token):
        if isinstance(token, Factor):
            assert token.value is not None
            return token.value

        return Literal(token)


class FactorFactory(object):
    def __getattr__(self, item):
        return Factor(item)

    def literal(self, value):
        return Factor(None, Literal(value))

    v = literal
    value = literal


def build_exp1():
    ff = FactorFactory()
    f = ff.f
    g = ff.g
    a = ff.a

    return f(10, 10) + g(f(a + 1, 2)) + 1


def test1():
    exp = build_exp1()

    context = {
        '+': lambda x, y: x + y,
        'f': lambda x, y: x * y,
        'g': lambda x: x * 2,
        'a': 1
    }

    print exp.to_code()
    result = exp.calc(context)
    assert result == 109


def test2():
    exp1 = build_exp1()

    json_str = json.dumps(exp1.to_json())

    exp2 = Node.from_json(json.loads(json_str))

    assert exp1.to_code() == exp2.to_code()


if __name__ == '__main__':
    test1()
    test2()
