from typing import List, Callable
from itertools import product
from fractions import Fraction


class Variable:
    def __init__(self, name, degree=1):
        if "^" in name:
            name, degree = name.split("^")
            degree = int(degree)
        self.name = name
        self.degree = degree

    def __eq__(self, other):
        return self.name == other.name and self.degree == other.degree

    def __lt__(self, other):
        return (self.name, self.degree) < (other.name, other.degree)

    def __gt__(self, other):
        return (self.name, self.degree) > (other.name, other.degree)

    def __mul__(self, other):
        if self.name != other.name:
            raise ValueError("Variable names do not match")
        return Variable(self.name, self.degree + other.degree)

    def __str__(self):
        if self.degree == 1:
            return self.name
        return self.name + "^" + str(self.degree)

    def __repr__(self):
        return str(self)


class Monomial:
    def __init__(self, s: str = None):
        if s is None:
            self.vars = []
            self.coef = Fraction(0)
            return

        s = s.strip()
        if s[0] == "-":
            self.coef = Fraction(-1)
            s = s[1:]
        else:
            self.coef = Fraction(1)
        self.vars = []
        for v in s.split(" "):
            if v == "":
                continue
            if v[0].isalpha():
                self.vars.append(Variable(v))
            else:
                self.coef *= Fraction(v)
        self.simplify()

    # def pm1(self):
    #     for v

    @classmethod
    def from_vars(cls, vars: List[Variable], coef: Fraction):
        self = cls()
        self.vars = vars
        self.coef = coef
        self.simplify()
        return self
    # def __init__(self, vars: List[Variable], coef: Fraction):
    #     self.vars = vars
    #     self.coef = coef
    #     self.simplify()

    def __add__(self, other):
        if self.vars != other.vars:
            raise ValueError("Variables do not match")
        return Monomial.from_vars(self.vars, self.coef + other.coef)

    def __mul__(self, other):
        new_vars = self.vars + other.vars
        new_coef = self.coef * other.coef
        return Monomial(f"{new_coef} {' '.join([str(v) for v in new_vars])}")

    def __lt__(self, other):
        if self.degree() != other.degree():
            return self.degree() < other.degree()
        return self.vars < other.vars

    def __gt__(self, other):
        if self.degree() != other.degree():
            return self.degree() > other.degree()
        return self.vars > other.vars

    def degree(self):
        return sum([v.degree for v in self.vars])


    def simplify(self):
        vars = sorted(self.vars)
        new_vars = []
        for v in vars:
            if not new_vars or new_vars[-1].name != v.name:
                new_vars.append(v)
            else:
                new_vars[-1] = new_vars[-1] * v
        self.vars = new_vars

    def __str__(self):
        if not self.vars:
            return str(self.coef)
        return str(self.coef) + " " + " ".join([str(v) for v in self.vars])

    def __repr__(self):
        return str(self)




class Polynomial:
    def __init__(self, s: str = None):
        if s is None:
            self.monomials = []
            return
        s = s.strip()
        self.monomials = []
        for m in s.split("+"):
            m = m.strip()
            self.monomials.append(Monomial(m))
        self.monomials.sort()

    @classmethod
    def from_monomials(cls, monomials: List[Monomial]):
        self = cls()
        self.monomials = monomials
        self.simplify()
        return self

    def __add__(self, other):
        i, j = 0, 0
        new_monomials = []
        while i < len(self.monomials) and j < len(other.monomials):
            if self.monomials[i] < other.monomials[j]:
                new_monomials.append(self.monomials[i])
                i += 1
            elif self.monomials[i] > other.monomials[j]:
                new_monomials.append(other.monomials[j])
                j += 1
            else:
                new_monomials.append(self.monomials[i] + other.monomials[j])
                i += 1
                j += 1
        if i < len(self.monomials):
            new_monomials += self.monomials[i:]
        if j < len(other.monomials):
            new_monomials += other.monomials[j:]
        return Polynomial.from_monomials(new_monomials)

    def __mul__(self, other):
        new_monomials = []
        for m1, m2 in product(self.monomials, other.monomials):
            new_monomials.append(m1 * m2)
        return Polynomial.from_monomials(new_monomials)

    def simplify(self):
        new_monomials = []
        for m in self.monomials:
            if m.coef == 0:
                continue
            if not new_monomials or new_monomials[-1].vars != m.vars:
                new_monomials.append(m)
            else:
                new_monomials[-1] = new_monomials[-1] + m
                if new_monomials[-1].coef == 0:
                    new_monomials.pop()
        self.monomials = sorted(new_monomials)

    def __str__(self):
        if not self.monomials:
            return "0"
        return "\n".join([str(m) for m in self.monomials])

    def __repr__(self):
        return str(self)


def fourier_expansion(f: Callable, n: int):
    p = Polynomial("0")
    for a in product([-1, 1], repeat=n):
        q = Polynomial(str(f(*a)))
        for i in range(n):
            if a[i] == 1:
                q = q * Polynomial(f"1/2 + 1/2 x{i+1}")
            else:
                q = q * Polynomial(f"1/2 + -1/2 x{i+1}")
        p += q
    return p

def maj(*args):
    return 1 if sum(args) > 0 else -1


if __name__ == "__main__":
    # p = Polynomial("1")
    # for i in range(1, 5):
    #     p = p * Polynomial(f"1/2 + -1/2 x{i}")
    # print(p)
    print(fourier_expansion(maj, 5))
