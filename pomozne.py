from enum import Enum
from functools import wraps

class Meni(Enum):
    """
    Razred za izbire v menijih.
    """
    def __init__(self, ime, funkcija):
        """
        Konstruktor izbire.
        """
        self.ime = ime
        self.funkcija = funkcija

    def __str__(self):
        """
        Znakovna predstavitev izbire.
        """
        return self.ime
    
def prekinitev(fun):
    """
    Dekorator za obravnavo prekinitev s Ctrl+C.
    """
    @wraps(fun)
    def funkcija(*largs, **kwargs):
        try:
            fun(*largs, **kwargs)
        except KeyboardInterrupt:
            print("\nPrekinitev!")
    return funkcija