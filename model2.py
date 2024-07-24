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

    def __init__(self, id, ime, kontakt,geslo,naziv):
        """
        Konstruktor uporabnika.
        """
        # prej je bilo na koncu id = None, sem spremenila
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
    def klijenti_agenta(id_agenta):
        '''vrne vse klijente ki jih ima agent'''

        sql = """
            SELECT kupci.id, kupci.ime,kupci.kontakt, kupci.buget,kupci.lokacija,kupci.vrsta FROM kupci
            JOIN zastopa on id_kupec=kupci.id
            WHERE id_agent= ?;
            """
        results = []
        for id, ime, kontakt, buget, lokacija, vrsta in conn.execute(sql, [id_agenta]):
            results.append(Kupci(id, ime, kontakt, buget, lokacija, vrsta))
        return results
    
    @staticmethod
    def dodaj_agenta(ime, kontakt, geslo, naziv):
        '''doda agenta'''

        sql = """
            INSERT INTO agent (ime, kontakt,geslo,naziv) VALUES (?, ?, ?, ?);
            """
    
        try:
            conn.execute(sql, [ime, kontakt, geslo, naziv])
            conn.commit()  # Commit the transaction
            print(f"Agent {ime} added successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    



class Kupci:
    def __init__ (self, id,ime,kontakt,buget,lokacija,vrsta):
        self.id= id
        self.ime = ime
        self.kontakt=kontakt
        self.buget=buget
        self.lokacija=lokacija
        self.vrsta=vrsta

    def __str__(self):
        return f"ID: {self.id}, Name: {self.ime}, Contact: {self.kontakt}, Budget: {self.buget}, Location: {self.lokacija}, Type: {self.vrsta}"
    
    @staticmethod
    def dodaj_kupca(ime, kontakt, buget, lokacija, vrsta):
        '''doda kupca'''

        sql = """
            INSERT INTO kupci (ime, kontakt,buget,lokacija,vrsta) VALUES (?,?,?,?,?);
            """
    
        try:
            conn.execute(sql, [ime, kontakt, buget, lokacija, vrsta])
            conn.commit()  # Commit the transaction
            print(f"Customer {ime} added successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



    @staticmethod
    def agenti(id_kupec):
        '''vrne katere vse agente ima kupec'''

        sql = """
            SELECT agent.id, agent.ime, agent.kontakt, agent.geslo,agent.naziv FROM agent
            JOIN zastopa on id_agent=agent.id
            WHERE id_kupec= ?;
            """
        results = []
        for id, ime, kontakt, geslo, naziv  in conn.execute(sql, [id_kupec]):
            results.append(Agenti(id, ime, kontakt, geslo, naziv))
        return results
    
    @staticmethod
    def nepremicnine(id_kupec):
        '''vrne katere vse nepremicnine lahko zanimajo kupca'''

        sql = """
            SELECT nepremicnine.id, nepremicnine.lastnik, nepremicnine.cena, nepremicnine.vrsta,lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            WHERE id_kupec = ?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_kupec]):
            results.append(Nepremicnine(id,lastnik,cena,vrsta,lokacija))
        return results
    
    




class Nepremicnine:
    def __init__ (self, id, lastnik, cena, vrsta, lokacija):
        self.id=id
        self.lastnik = lastnik
        self.cena=cena
        self.vrsta=vrsta
        self.lokacija=lokacija

    def __str__(self):
        return f'id : {self.id}, Lastnik: {self.lastnik}, Cena :{self.cena}, Lokacija :{self.lokacija}, Vrsta: {self.vrsta}'

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
    
    @staticmethod
    def kupci(id_nepremicnina):
        '''kateri kupci odgovarjajo tisti nepremicnini'''

        sql = """
            SELECT id,ime,kontakt,buget,lokacija,vrsta FROM kupci
            JOIN interes ON kupci.id=id_kupec
            WHERE id_nepremicnine= ?;
            """
        results = []
        for id,ime,kontakt,buget,lokacija,vrsta  in conn.execute(sql, [id_nepremicnina]):
            results.append(Kupci(id,ime,kontakt,buget,lokacija,vrsta))
        return results
    
    @staticmethod
    def dodaj_nepremicnino(lastnik, cena, vrsta, lokacija):
        '''doda nepremicnino'''

        sql = """
            INSERT INTO nepremicnine (lastnik,cena,vrsta,lokacija) VALUES (?, ?, ?, ?);
            """
    
        conn.execute(sql, [lastnik, cena, vrsta, lokacija])

    @staticmethod
    def pogled_agenta(id_agenta, id_kupca):
        '''vrne vse neopremicnine ka odgovarjajo enemu kupcu od enega agenta'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            JOIN zastopa on zastopa.id_kupec=interes.id_kupec
            WHERE interes.id_kupec=? and zastopa.id_agent=?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_kupca, id_agenta]):
            results.append(Nepremicnine(id, lastnik, cena, vrsta, lokacija))
        return results

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

# for elt in Agenti.klijenti_agenta(2):
#     print(elt)
# print(Nepremicnine.vse_lokacije())

# for item in Nepremicnine.f_lokacija('Ljubljana'):
#     print(item)

# for item in Nepremicnine.f_vrsta_nepremicnine("house"):
#     print(item)

# for elt in Kupci.agenti(5):
#     print(elt)

# print(Kupci)
# for elt in Kupci.nepremicnine(2):
#     print(elt)

# print(Nepremicnine.kupci(4))
# for item in Nepremicnine.kupci(4):
#     print(item)

# Kupci.dodaj_kupca("ime", "kontakt", 6000, "lokacija", "vrsta")
#Agenti.dodaj_agenta("neki", "neki", "neki", 1)
#Nepremicnine.dodaj_nepremicnino("ndki", 90, "house", "Tudjemili")

# for item in Nepremicnine.pogled_agenta(2,131):
#     print(item)

conn.commit()
#conn.close()