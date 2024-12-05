from .equation import solve


def løs(*likninger, variabler=None, pprint=True):
    """Løser én eller flere likninger (et likningssystem), eller én ulikhet.

    Args:
        *likninger (str): Et variabelt antall likninger eller ulikheter separert med komma som representerer likningene eller ulikheten.
        pprint (bool): Hvis `True` gir en matematisk tekststreng-representasjon av løsningen. Standardverdi: `True`.

    Returns:
        str eller list: En tekststreng-representasjon (str) av løsningen(e) hvis `pprint` er `True`. Hvis ikke en liste med dictionaries som inneholder løsningene. Returnerer "Ingen løsning" hvis ingen reelle løsninger finnes.

    Eksempler:
        >>> from casify import *
        >>> løs("x**2 - x - 6 = 0")
        'x = -2    ∨    x = 3'
        >>> løs("x + y - z = 1", "x + y + 2*z = 3", "-x + y + z = -1")
        'x = 5/3 ∧ y = 0 ∧ z = 2/3'

        >>> f = funksjon("a * x**2 + b*x + c")
        >>> løs("f(1) = 2", "f(-1) = 3", "f(3) = 4")
        'a = 3/8 ∧ b = -1/2 ∧ c = 17/8'

        >>> f = funksjon("x**2 - x - 2")
        >>> løs("f(x) = 0")
        'x = -1    ∨    x = 2'
        >>> løs("f(x) > 0")
        '( (x < -1))  ∨  ((2 < x) )'
        >>> løs("f(x) <= 0")
        '(-1 <= x)  ∧  (x <= 2)'

    """
    løsning = solve(*likninger, variables=variabler, pprint=pprint)
    if løsning == "No solution":
        return "Ingen løsning"
    else:
        return løsning


def Løs(*likninger, variabler=None, pprint=True):
    """Alternativ skrivemåte for `løs`."""
    return løs(*likninger, variabler=variabler, pprint=pprint)
