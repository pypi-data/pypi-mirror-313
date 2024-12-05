from casify import *

løsning = løs("x**2 - 3*x - 3 >= -x + 4")

print(løsning)

løsning = løs("(x - 2) * (x + 1) > 0")
print(løsning)


løsning = løs("(x - 2) * (x + 1) <= 0")
print(løsning)


# Example usage
expressions = [
    "((-oo < x) & (x <= 1 - 2*sqrt(2))) | ((x < oo) & (1 + 2*sqrt(2) <= x))",
    "((-oo < x) & (x < -1)) | ((2 < x) & (x < oo)) | (x > 3) & (x < oo)",
    "(-1 <= x) & (x <= 2)",
    "(-2 < x) & (x < 3)",
]
new_expressions = []
for expression in expressions:

    expression = expression.split("|")
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

        tmp = " ∧ ".join(tmp)

        new_expression.append(tmp)

    new_expression = " ∨ ".join(new_expression)

    new_expressions.append(new_expression)

for old, new in zip(expressions, new_expressions):
    print(f"Original: {old}")
    print(f"Simplified: {new}")
    print("--" * 50)
