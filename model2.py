import baza2
import sqlite3
from sqlite3 import IntegrityError
#from geslo import sifriraj_geslo, preveri_geslo
import os

#
#if os.path.exists('baza.db'):
#    os.remove('baza.db')


conn = sqlite3.connect('baza.db')
"""
baza2.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')


agenti , klijenti, nepremicnine, zastopa, interes = baza2.pripravi_tabele(conn)
baza2.pripravi_tabele(conn)
conn.commit()
conn.close()
"""





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
    def agenti():
        '''vrne id ter ime klijenta'''

        sql = """
            SELECT id, ime FROM agent;
            """
        results = []
        for id, ime  in conn.execute(sql):
            results.append((id, ime))
        return results
    
    @staticmethod
    def geslo(ime):
        """
        Preveri, ali sta uporabniško ime geslo pravilna.
        """
        sql = """
            SELECT id,geslo,ime,naziv FROM agent
            WHERE kontakt = ?
        """
        geslo = conn.execute(sql, [ime]).fetchone()[1]
        id = conn.execute(sql, [ime]).fetchone()[0]
        agent=conn.execute(sql, [ime]).fetchone()[2]
        naziv=conn.execute(sql, [ime]).fetchone()[3]
        return (geslo,id,agent,naziv)

        
    def klijenti_agenta(id_agenta):
        '''vrne vse klijente ki jih ima agent'''

        sql = """
            SELECT klijenti.id, klijenti.ime,klijenti.kontakt, klijenti.buget,klijenti.lokacija,klijenti.vrsta FROM klijenti
            JOIN zastopa on id_klijent=klijenti.id
            WHERE id_agent= ?;
            """
        results = []
        for id, ime, kontakt, buget, lokacija, vrsta in conn.execute(sql, [id_agenta]):
            results.append(Klijenti(id, ime, kontakt, buget, lokacija, vrsta))
        return results
    
    @staticmethod
    def dodaj_agenta(ime, kontakt, geslo, naziv):
        '''doda agenta'''

        sql = """
            INSERT INTO agent (ime, kontakt,geslo,naziv) VALUES (?, ?, ?, ?);
            """
        conn.execute(sql, [ime, kontakt, geslo, naziv])
        conn.commit()

        """
        try:
            conn.execute(sql, [ime, kontakt, geslo, naziv])
            conn.commit()  # Commit the transaction
            print(f"Agent {ime} added successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    """
    
    @staticmethod
    def vsi_agenti():
        '''vrne katere vse agente'''

        sql = """
            SELECT id, ime, kontakt, geslo,naziv FROM agent
            """
        results = []
        for id, ime, kontakt, geslo,naziv in conn.execute(sql, []):
            results.append(Agenti(id, ime, kontakt, geslo,naziv))
        return results




class Klijenti:
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
    def dodaj_klijenta(ime, kontakt, buget, lokacija, vrsta):
        '''doda klijenta'''

        sql = """
            INSERT INTO klijenti (ime, kontakt,buget,lokacija,vrsta) VALUES (?,?,?,?,?);
            """
        conn.execute(sql, [ime, kontakt, buget, lokacija, vrsta])
        conn.commit()
        """
        try:
            conn.execute(sql, [ime, kontakt, buget, lokacija, vrsta])
            conn.commit()  # Commit the transaction
            print(f"Customer {ime} added successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
"""

    @staticmethod
    def klijenti():
        '''vrne id ter ime klijenta'''

        sql = """
            SELECT id, ime FROM klijenti;
            """
        results = []
        for id, ime  in conn.execute(sql):
            results.append((id, ime))
        return results

    @staticmethod
    def agenti(id_klijent):
        '''vrne katere vse agente ima klijent'''

        sql = """
            SELECT agent.id, agent.ime, agent.kontakt, agent.geslo,agent.naziv FROM agent
            JOIN zastopa on id_agent=agent.id
            WHERE id_klijent= ?;
            """
        results = []
        for id, ime, kontakt, geslo, naziv  in conn.execute(sql, [id_klijent]):
            results.append(Agenti(id, ime, kontakt, geslo, naziv))
        return results
    
    @staticmethod
    def nepremicnine(id_klijent):
        '''vrne katere vse nepremicnine lahko zanimajo klijenta'''

        sql = """
            SELECT nepremicnine.id, nepremicnine.lastnik, nepremicnine.cena, nepremicnine.vrsta,lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            WHERE id_klijent = ?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_klijent]):
            results.append(Nepremicnine(id,lastnik,cena,vrsta,lokacija))
        return results
    
    @staticmethod
    def klijenti_agenta(id_agent):
        '''vrne katere vse klijente od agenta'''

        sql = """
            SELECT id, ime FROM klijenti
            JOIN zastopa ON klijenti.id=zastopa.id_klijent
            WHERE zastopa.id_agent = ?;
            """
        results = []
        for id, ime in conn.execute(sql, [id_agent]):
            results.append((id,ime))
        return results
    
    @staticmethod
    def vsi_klijenti():
        '''vrne katere vse klijente'''

        sql = """
            SELECT id, ime, kontakt, buget,lokacija,vrsta FROM klijenti
            """
        results = []
        for id, ime, kontakt, buget,lokacija,vrsta in conn.execute(sql, []):
            results.append(Klijenti(id, ime, kontakt, buget,lokacija,vrsta))
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
    def vse_nepremicnine():
        '''vrne katere vse nepremicnine'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija FROM nepremicnine
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija in conn.execute(sql, []):
            results.append(Nepremicnine(id, lastnik, cena, vrsta, lokacija))
        return results

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
    def vse_vrste():
        """vrne seznam vrst nepremicnin"""

        sql = """
        SELECT vrsta FROM nepremicnine
        GROUP BY vrsta;
        """
        vrste = []
        for vrsta in conn.execute(sql):
            vrste.append(vrsta)
        
        return vrste
    
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
    def klijenti(id_nepremicnina):
        '''kateri klijenti odgovarjajo tisti nepremicnini'''

        sql = """
            SELECT id,ime,kontakt,buget,lokacija,vrsta FROM klijenti
            JOIN interes ON klijenti.id=id_klijent
            WHERE id_nepremicnine= ?;
            """
        results = []
        for id,ime,kontakt,buget,lokacija,vrsta  in conn.execute(sql, [id_nepremicnina]):
            results.append(Klijenti(id,ime,kontakt,buget,lokacija,vrsta))
        return results
    
    @staticmethod
    def dodaj_nepremicnino(lastnik, cena, vrsta, lokacija):
        '''doda nepremicnino'''

        sql = """
            INSERT INTO nepremicnine (lastnik,cena,vrsta,lokacija) VALUES (?, ?, ?, ?);
            """
    
        conn.execute(sql, [lastnik, cena, vrsta, lokacija])
        conn.commit()

    @staticmethod
    def pogled_agenta(id_agenta, id_klijenta):
        '''vrne vse neopremicnine ka odgovarjajo enemu klijentu od enega agenta'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            JOIN zastopa on zastopa.id_klijent=interes.id_klijent
            WHERE interes.id_klijent=? and zastopa.id_agent=?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_klijenta, id_agenta]):
            results.append(Nepremicnine(id, lastnik, cena, vrsta, lokacija))
        return results

class Zastopa:
    def __init__(self,klijent,agent):
        self.klijent=klijent
        self.agent=agent

class Interes:
    def __init__(self,klijent,nepremicnina):
        self.klijent=klijent
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

# for elt in Klijenti.agenti(5):
#     print(elt)

# print(Klijenti)
# for elt in Klijenti.nepremicnine(2):
#     print(elt)

# print(Nepremicnine.klijenti(4))
# for item in Nepremicnine.klijenti(4):
#     print(item)

# Klijenti.dodaj_klijenta("ime", "kontakt", 6000, "lokacija", "vrsta")
#Agenti.dodaj_agenta("neki", "neki", "neki", 1)
#Nepremicnine.dodaj_nepremicnino("ndki", 90, "house", "Tudjemili")

# for item in Nepremicnine.pogled_agenta(2,131):
#     print(item)

#conn.commit()
#conn.close()
