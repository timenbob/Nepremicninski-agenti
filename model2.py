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
    
    @staticmethod
    def prijava(ime, geslo):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id, zgostitev, sol FROM uporabnik
            WHERE ime = ?
        """
        try:
            id, zgostitev, sol = conn.execute(sql, [ime]).fetchone()
            if preveri_geslo(geslo, zgostitev, sol):
                return Uporabnik(ime, id=id)
        except TypeError:
            pass
        raise LoginError(ime)




class Kupci:
    def __init__ (self,ime,kontakt,buget,lokacija,vrsta, id):
        self.id=id
        self.ime = ime
        self.kontakt=kontakt
        self.buget=buget
        self.lokacija=lokacija
        self.vrsta=vrsta


class Nepremicnine:
    def __init__ (self, id, lastnik, cena, vrsta, lokacija):
        self.id=id
        self.lastnik = lastnik
        self.cena=cena
        self.vrsta=vrsta
        self.lokacija=lokacija

    def __str__(self):
        return f'id : {self.id} : {self.lastnik}, {self.cena}, {self.lokacija}, {self.vrsta}'

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

    @staticmethod
    def f_lokacija(lokacija):
        '''vrne vse nepremicnine ki so na dani lokaciji'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija
            FROM nepremicnine
            WHERE lokacija == ?
            """
        for id, lastnik, cena, vrsta, lokacija in conn.execute(sql, [lokacija]):
            yield Nepremicnine(id, lastnik, cena, vrsta, lokacija)

    @staticmethod
    def vse_lokacije():
        """vrne seznam lokacij nepremicnin ki so v bazi"""

        sql = """
        SELECT lokacija FROM nepremicnine
        GROUP BY lokacija;
        """
        lokacije = []
        for lokacija in conn.execute(sql):
            lokacije.append(lokacija)
        
        return lokacije
    
    @staticmethod
    def f_vrsta_nepremicnine(vrsta):
        """vrne vse nepremicnine te vrste"""
        sql = """
        SELECT id, lastnik, cena, vrsta, lokacija
        FROM nepremicnine
        WHERE vrsta == ?
        """
        for id, lastnik, cena, vrsta, lokacija in conn.execute(sql, [vrsta]):
            yield Nepremicnine(id, lastnik, cena, vrsta, lokacija)
    

class Zastopa:
    def __init__(self,kupec,agent):
        self.kupec=kupec
        self.agent=agent

class Interes:
    def __init__(self,kupec,nepremicnina):
        self.kupec=kupec
        self.nepremicnina=nepremicnina

# for item in Nepremicnine.f_manjse_od_cena(200000):
#     print(item)

# print(Nepremicnine.vse_lokacije())

# for item in Nepremicnine.f_lokacija('Ljubljana'):
#     print(item)

for item in Nepremicnine.f_vrsta_nepremicnine("house"):
    print(item)


conn.commit()
conn.close()