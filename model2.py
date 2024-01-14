import baza2
import sqlite3
from sqlite3 import IntegrityError
#from geslo import sifriraj_geslo, preveri_geslo

conn = sqlite3.connect('basaaaa.db')
baza2.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

agenti , kupci, nepremicnine, zastopa = baza2.pripravi_tabele(conn)
#, zastopa, interes



conn.commit()

class LoginError(Exception):
    """
    Napaka ob napačnem uporabniškem imenu ali geslu.
    """
    pass


class Agenti:
    """
    Razred za agente.
    """

    def __init__(self, ime, *, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime

    def __str__(self):
        """
        Znakovna predstavitev uporabnika.
        Vrne uporabniško ime.
        """
        return self.ime


