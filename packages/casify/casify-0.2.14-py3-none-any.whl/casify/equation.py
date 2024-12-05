# import sympy
# import sys


def _get_func(expr):
    import re

    match = re.match(r"(\w+)\((-?\w+|-?\d+)\)", expr.strip())
    if match:
        func_name, arg = match.groups()
        return func_name, arg
    else:
        return False, False


def _handle_expression(expr):
    known_functions = [
        "cos",
        "sin",
        "tan",
        "exp",
        "acos",
        "asin",
        "atan",
    ]

    func_name, arg = _get_func(expr)
    if func_name:
        if func_name in known_functions:
            import sympy

            return sympy.sympify(expr)
        else:
            import sys

            main_module = sys.modules["__main__"]
            main_globals = main_module.__dict__
            func = main_globals.get(func_name)

            return func(arg)
    else:
        import sympy

        return sympy.sympify(expr)


def solve(*equations, variables=None, pprint=True):
    """Solves an equation or a set of equations or inequalities.

    Args:
        *equations (str): a variable number of strings representing equations or inequalities.
        pprint (bool): Gives a mathematical-like output. Defaults to `True`.

    Returns:
        str or list: A string representation of the solutions if pprint is True, otherwise a list of dictionaries containing the solutions. Return "No solution" if no real solutions are found.

    Examples:
        >>> from casify import *
        >>> solve("x**2 - x - 6 = 0")
        'x = -2    ∨    x = 3'
        >>> solve("x + y - z = 1", "x + y + 2*z = 3", "-x + y + z = -1")
        'x = 5/3 ∧ y = 0 ∧ z = 2/3'
        >>> f = function("a * x**2 + b*x + c")
        >>> solve("f(1) = 2", "f(-1) = 3", "f(3) = 4")
        'a = 3/8 ∧ b = -1/2 ∧ c = 17/8'

    """
    import sympy

    eqs = []
    # Parse the equations
    for eq in equations:
        if ">" in eq or "<" in eq:
            if ">=" in eq:
                lhs, rhs = eq.split(">=")
                sign = ">="

            elif "<=" in eq:
                lhs, rhs = eq.split("<=")
                sign = "<="

            elif ">" in eq:
                lhs, rhs = eq.split(">")
                sign = ">"

            elif "<" in eq:
                lhs, rhs = eq.split("<")
                sign = "<"

            lhs = _handle_expression(lhs)
            rhs = _handle_expression(rhs)
            eq = " ".join([str(lhs), sign, str(rhs)])

            return _solve_inequality(eq)

        else:
            if "==" in eq:
                lhs, rhs = eq.split("==")

            elif "=" in eq:
                lhs, rhs = eq.split("=")

            lhs = _handle_expression(lhs)
            rhs = _handle_expression(rhs)

            eqs.append(sympy.Eq(lhs, rhs))

    if variables:
        solutions = sympy.solve(eqs, variables, dict=True)
    else:
        solutions = sympy.solve(eqs, dict=True)

    # Remove complex solutions from the solution set.
    real_solutions = []
    if isinstance(solutions, dict):
        real_solutions = {
            key: solutions.get(key) for key in solutions if solutions.get(key).is_real
        }
        real_solutions = [real_solutions]
    else:
        for sol in solutions:
            if not False in [sol.get(key).is_real for key in sol]:
                real_solutions.append(sol)

    if real_solutions == [] or real_solutions == {}:
        return "No solution"

    elif pprint:
        pprint_solution = ""
        for i, sol in enumerate(real_solutions):
            pprint_solution += (
                str(sol)
                .replace(":", " =")
                .replace("{", "")
                .replace("}", "")
                .replace(",", " ∧")
            )
            if i < len(real_solutions) - 1:
                pprint_solution += "    ∨    "

        return pprint_solution
    else:
        return real_solutions


def Solve(*equations, variables=None, pprint=True):
    """Alternative way to write `solve`."""
    return solve(*equations, variables=variables, pprint=pprint)


def _simplify_expression(expression):
    """
    Simplify logical expressions of the form:
    ((-oo < x) ∧ (x <= ...)) ∨ ((x < oo) ∧ (... <= x))
    or
    ((-oo < x) ∧ (... < x)) ∨ ((x < oo) ∧ (x < ...))
    """
    import re

    # Define a generic pattern
    pattern = r"""
        \(\(-oo < ([a-zA-Z0-9_]+)\)\s+∧\s+\(\1\s*([<>]=?)\s*(.*?)\)\)\s+∨\s+  # First part (-oo < x and x <= ...)
        \(\(\1 < oo\)\s+∧\s+\((.*?)\s*\2\s*\1\)\)                            # Second part (x < oo and ... <= x)
    """

    # Replacement for the simplified version
    replacement = r"\3 \2 \1  ∨  \4 \2 \1"

    # Perform the substitution with verbose regex for readability
    simplified = re.sub(pattern, replacement, expression, flags=re.VERBOSE)
    return simplified


def _solve_inequality(expr, variables=None):
    import sympy
    import re

    if variables:
        solution = sympy.solve(expr, variables, dict=True)
    else:
        solution = sympy.solve(expr, dict=True)

    solution = str(solution)
    if solution == "False":
        return "No solution"

    solution = solution.replace("(-oo < x) & (x < oo)", "x ∈ ℝ")

    expression = solution.split("|")
    new_expression = []
    for i, expr in enumerate(expression):
        tmp = []
        expr = expr.split("&")
        for j, s in enumerate(expr):
            if (
                "(-oo < x)" in s
                or "(x < oo)" in s
                or "(-oo <= x)" in s
                or "(x <= oo)" in s
            ):
                pass
            elif "sqrt" not in s:
                s = s.replace(")", "")
                s = s.replace("(", "")
                tmp.append(s)
            else:
                s = s[2:-2]
                while (
                    s[-1] == s[-2]
                ):  # remove unecessary parenthesis "))". Only leave single parenthesis ")"
                    s = s[:-1]
                tmp.append(s)

        tmp = "  ∧  ".join(tmp)

        new_expression.append(tmp)

    new_expression = "    ∨    ".join(new_expression)
    return new_expression
    # solution = solution.replace("(-oo < x))", "")

    # solution = solution.replace("((x < oo)", "")
    # solution = solution.replace("(-oo < x)", "")
    # solution = solution.replace("(x < oo)", "")
    # solution = solution.replace("(", "")
    # solution = solution.replace(")", "")
    # solution = solution.replace("|", " ∨ ").replace("&", " ∧ ")
    # solution = _simplify_expression(solution)

    # return solution
