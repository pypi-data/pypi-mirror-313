# import sympy

from .equation import solve


class function:
    """A class representing a mathematical function.

    Args:
        f (str): A string representing the function expression.

    Methods:
        __call__(x): Evaluates the function at a given value of x.
        derivative(x=None, order=1): Computes the derivative of the function.
        factor(): Factors the function expression.
        expand(): Expands the function expression.
        plot(domain=None): Plots the function within the specified domain.

    Examples:
        >>> from casify import *
        >>> f = function("x**2 + 2*x + 1")
        >>> f(2)
        9
        >>> f.derivative()
        2*x + 2
        >>> f.factor()
        (x + 1)**2
        >>> g = function("(x + 1) * (x - 3)")
        >>> g.expand()
        x**2 - 2*x - 3
        >>> g.graph() # displays the graph of the function
    """

    known_functions = [
        "cos",
        "sin",
        "tan",
        "exp",
        "log",
        "ln",
        "log2",
        "log10",
    ]

    def __init__(self, f_expr):
        import sympy

        self._f_expr = sympy.sympify(f_expr)

    def __call__(self, x):
        return self._f_expr.subs("x", x)

    def derivative(self, x=None, order=1):
        import sympy

        if x is not None:
            return sympy.diff(self._f_expr, "x", order).subs("x", x)
        else:
            return sympy.diff(self._f_expr, "x", order)

    def factor(self):
        import sympy

        return sympy.factor(self._f_expr)

    def expand(self):
        import sympy

        return sympy.expand(self._f_expr)

    def zeros(self):
        equation = " ".join([str(self._f_expr), "=", "0"])
        return solve(equation)

    def integral(self, a=None, b=None):
        import sympy

        if a == "inf":
            a = sympy.oo
        elif a == "-inf":
            a = -sympy.oo
        if b == "inf":
            b = sympy.oo
        elif b == "-inf":
            b = -sympy.oo

        x = sympy.sympify("x")
        if a is not None and b is None:
            return sympy.integrate(self._f_expr, (x, a, x))
        elif a is None and b is not None:
            return sympy.integrate(self._f_expr, (x, x, b))
        elif a is not None and b is not None:
            return sympy.integrate(self._f_expr, (x, a, b))
        else:
            return sympy.integrate(self._f_expr, x)

    def graph(self, domain=None):
        import plotmath
        import numpy
        import sympy

        numpy_func = sympy.lambdify("x", self._f_expr, "numpy")
        if domain is not None:
            xmin, xmax = domain
            x_vals = numpy.linspace(xmin, xmax, 1024)
            codomain = (numpy.min(numpy_func(x_vals)), numpy.max(numpy_func(x_vals)))
            ymin, ymax = domain
        else:
            xmin, xmax = (-6, 6)
            ymin, ymax = (-6, 6)
        plotmath.plot(
            functions=[numpy_func],
            fn_labels=None,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
        )
        plotmath.show()

    def __str__(self):
        return str(self._f_expr)


def Function(f):
    """Alternative way to write `function`"""
    return function(f)


def derivative(expr, var="x"):
    """Computes the derivative of an algebraic expression with respect to `x`.

    Args:
        expr (str): the algebraic expression to differentiate with respect to `x`.

    Returns:
        sympy.Expr: the derivative of the algebraic expression

    """
    import sympy

    expr = sympy.sympify(expr)
    return sympy.diff(expr, sympy.symbols(var))
