import baza2
import sqlite3
from sqlite3 import IntegrityError
#from geslo import sifriraj_geslo, preveri_geslo
import os

if os.path.exists('baza.db'):
    os.remove('baza.db')


conn = sqlite3.connect('baza.db')
baza2.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

agenti , kupci, nepremicnine, zastopa, interes = baza2.pripravi_tabele(conn)





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

    @staticmethod
    def f_manjse_od_cena(max_cena):
        '''vrne vse nepremicnine ki imajo ceno manjso od max_cena'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija
            FROM nepremicnine
            WHERE cena <= ?
            """
        for id, lastnik, cena, vrsta, lokacija in conn.execute(sql, [max_cena]):
            yield Nepremicnine(id, lastnik, cena, vrsta, lokacija)

class Zastopa:
    def __init__(self,kupec,agent):
        self.kupec=kupec
        self.agent=agent

class Interes:
    def __init__(self,kupec,nepremicnina):
        self.kupec=kupec
        self.nepremicnina=nepremicnina

for item in Nepremicnine.f_manjse_od_cena(200000):
    print(item)


conn.commit()
conn.close()