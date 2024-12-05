from .function import function, derivative


class funksjon(function):
    """A klasse som representerer en matematisk funksjon f.

    Args:
        f (str): En tekststrengrepresentasjon av f(x).

    Methods:
        __call__(x): returnerer f(x) for en verdi av x.
        derivert(x=None, order=1): Regner ut den deriverte, enten uttrykket eller for en bestemt x-verdi.
        faktoriser(): Faktoriserer f(x)
        utvid(): Utvider f(x)
        graf(domain=None): Plotter funksjonsgrafen til f.

    Eksempler:
        >>> from casify import *
        >>> f = funksjon("x**2 + 2*x + 1")
        >>> f(2)
        9
        >>> f.derivert()
        2*x + 2
        >>> f.derivert(4)
        10
        >>> f.faktoriser()
        (x + 1)**2
        >>> g = funksjon("(x + 1) * (x - 3)")
        >>> g.utvid()
        x**2 - 2*x - 3
        >>> g.graf() # viser grafen til g.
    """

    def __init__(self, f_expr):
        super().__init__(f_expr)

    def derivert(self, x=None, order=1):
        return self.derivative(x, order)

    def faktoriser(self):
        return self.factor()

    def utvid(self):
        return self.expand()

    def nullpunkter(self):
        return self.zeros()

    def integral(self, a=None, b=None):
        return super().integral(a, b)

    def graf(self, domain=None):
        return self.graph(domain)


def Funksjon(f):
    """Alternativ skrivemåte for `funksjon`."""
    return funksjon(f)


def derivert(uttrykk, var="x"):
    """Regner ut den deriverte av et algebraisk uttrykk med hensyn på `x`

    Args:
        uttrykk (str): det algebraisk uttrykke som skal deriveres med hensyn på `x`.

    Returns:
        sympy.Expr: den deriverte av det algebraiske uttrykket.

    """
    return derivative(uttrykk, var)
