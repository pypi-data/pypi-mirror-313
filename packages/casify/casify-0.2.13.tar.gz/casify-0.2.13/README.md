# `casify`
`casify` is a Python package that implements a simplified CAS (Computer Algebra System) for symbolic computation, wrapping around `sympy` for facilitate its computations. The implementation provides both Norwegian and English names for all of its functions. 

## Basic examples

### Example 1: solving equations

```python
from casify import *

solution = solve("x**2 - x - 6 = 0")
print(solution)

```

### Eksempel 1: løse likninger

```python
from casify import *

løsning = løs("x**2 - x - 6 = 0")
print(løsning)

```


### Example 2: solve system of equations

```python
from casify import *

solution = solve("x + y = 2", "x - y = -1")

print(solution)

```

### Eksempel 2: løse likningssystemer

```python
from casify import *

løsning = løs("x + y = 2", "x - y = -1")

print(løsning)
```


### Example 3: function evalution

```python
from casify import *

f = function("x**2 - x - 6")

print(f(2)) # Computes f(2)
```

### Eksempel 3: funksjonsverdier

```python
from casify import *

f = funksjon("x**2 - x - 6")

print(f(2)) # Regner ut f(2)
```


### Example 4: Differentiation

```python
from casify import *

f = function("x**2 - x - 6")


print(f.derivative()) # Gives the general expression for the derivative

print(f.derivative(2)) # computes f'(2)
```

### Eksempel 4: Derivasjon

```python
from casify import *

f = funksjon("x**2 - x - 6")

print(f.derivert()) # gir det generelle uttrykket for den deriverte

print(f.derivert(2)) # regner ut f'(2)
```


### Example 5: algebraic expansion and factorization

```python
from casify import *

print(factor("x**2 - x - 6"))  # faktoriserer x**2 - x - 6

print(expand("2*(x - 1) * (x + 4)"))  # utvider 2 * (x - 1) * (x + 4)
```

### Eksempel 5: algebraisk utvidelse og faktorisering

```python
from casify import *

print(faktoriser("x**2 - x - 6"))  # faktoriserer x**2 - x - 6

print(utvid("2*(x - 1) * (x + 4)"))  # utvider 2 * (x - 1) * (x + 4)
```