import baza2
import sqlite3
from sqlite3 import IntegrityError
#from geslo import sifriraj_geslo, preveri_geslo
import os

if os.path.exists('basaaaa.db'):
    os.remove('basaaaa.db')


conn = sqlite3.connect('baza.db')
baza2.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

agenti , kupci, nepremicnine, zastopa, interes = baza2.pripravi_tabele(conn)





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

    def __init__(self, ime, kontakt,geslo,naziv, id=None):
        """
        Konstruktor uporabnika.
        """
        self.id = id
        self.ime = ime
        self.kontakt=kontakt
        self.geslo=geslo
        self.naziv=naziv


    def __str__(self):
        """
        Znakovna predstavitev uporabnika.
        Vrne uporabniško ime.
        """
        return self.ime


class Kupci:
    def __init__ (self,ime,kontakt,buget,lokacija,vrsta, id):
        self.id=id
        self.ime = ime
        self.kontakt=kontakt
        self.buget=buget
        self.lokacija=lokacija
        self.vrsta=vrsta


class Nepremicnine:
    def __init__ (self,lastnik,cena,lokacija,vrsta, id):
        self.id=id
        self.lastnik = lastnik
        self.cena=cena
        self.vrsta=vrsta
        self.lokacija=lokacija
        

class Zastopa:
    def __init__(self,kupec,agent):
        self.kupec=kupec
        self.agent=agent

class Interes:
    def __init__(self,kupec,nepremicnina):
        self.kupec=kupec
        self.nepremicnina=nepremicnina