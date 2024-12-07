import relibmss as ms

class _Expression:
    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('&')))
    
    def __or__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('|')))

    def __str__(self):
        if isinstance(self.value, tuple):
            return ' '.join([x.to_rpn() for x in self.value])
        return str(self.value)

    def to_rpn(self):
        if isinstance(self.value, tuple):
            return ' '.join([x.to_rpn() for x in self.value])
        return str(self.value)

class Context:
    def __init__(self):
        self.vars = set([])
        self.bdd = ms.BDD()

    def var(self, name):
        self.vars.add(name)
        return _Expression(name)
    
    def __str__(self):
        return str(self.vars)
    
    def getbdd(self, _Expression):
        rpn = _Expression.to_rpn()
        return self.bdd.rpn(rpn, self.vars)

    def And(self, args: list):
        assert len(args) > 0
        if len(args) == 1:
            return args[0]
        x = args[0]
        for y in args[1:]:
            x = _Expression((x, y, _Expression('&')))
        return x

    def Or(self, args: list):
        assert len(args) > 0
        if len(args) == 1:
            return args[0]
        x = args[0]
        for y in args[1:]:
            x = _Expression((x, y, _Expression('|')))
        return x

    def Not(self, arg: _Expression):
        return _Expression((arg, _Expression('!')))

    def IfThenElse(self, condition: _Expression, then_expr: _Expression, else_expr: _Expression):
        return _Expression((condition, then_expr, else_expr, _Expression('?')))

    def kofn(self, k: int, args: list):
        assert k <= len(args)
        if k == 1:
            return self.Or(args)
        elif k == len(args):
            return self.And(args)
        else:
            return self.IfThenElse(args[0], self.kofn(k-1, args[1:]), self.kofn(k, args[1:]))
