# This file is based on unrepr.py, which was in the public domain
import ast
import math


def getObj(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    s = "a=" + s
    return ast.parse(s).body[0].value


class UnknownType(Exception):
    pass


class Builder:

    def build(self, o):
        m = getattr(self, 'build_'+o.__class__.__name__, None)
        if m is None:
            raise UnknownType(o.__class__.__name__)
        return m(o)

    def build_List(self, o):
        return [self.build(elt) for elt in o.elts]

    def build_Num(self, o):
        # For Python < 3.8
        return o.n

    def build_Str(self, o):
        # For Python < 3.8
        return o.s

    def build_Bytes(self, o):
        # For Python < 3.8
        return o.s

    def build_NameConstant(self, o):
        # For Python < 3.8
        return o.value

    def build_Constant(self, o):
        # For Python >= 3.8
        return o.value

    def build_Name(self, o):
        if o.id == 'nan':
            return math.nan
        raise NameError(o.id)

    def build_Ellipsis(self, o):
        return Ellipsis

    def build_Dict(self, o):
        return {
            self.build(o.keys[i]): self.build(o.values[i])
            for i in range(len(o.keys))
        }

    def build_Tuple(self, o):
        return tuple(self.build_List(o))

    def build_Set(self, o):
        return set(self.build_List(o))

    def build_Call(self, o):
        if o.func.id == 'set' and o.args == [] and o.keywords == []:
            return set()
        raise UnknownType('Call')

    def build_BinOp(self, o):
        if isinstance(o.op, ast.Add):
            # For complex numbers
            left = self.build(o.left)
            right = self.build(o.right)
            if not isinstance(right, complex) or right.real != 0.0:
                raise UnknownType('Add')
            return left + right
        else:
            raise UnknownType('BinOp')

    def build_UnaryOp(self, o):
        if isinstance(o.op, ast.USub):
            return -self.build(o.operand)
        else:
            raise UnknownType('UnaryOp')


def unrepr(s):
    return Builder().build(getObj(s))
