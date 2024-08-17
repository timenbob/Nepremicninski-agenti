import baza
import sqlite3
import os


if not os.path.exists('baza.db'):
    #os.remove('baza.db')
    conn = sqlite3.connect('baza.db')
    baza.ustvari_bazo_ce_ne_obstaja(conn)
    conn.execute('PRAGMA foreign_keys = ON')


    agenti , klienti, nepremicnine, zastopa, interes = baza.pripravi_tabele(conn)
    baza.pripravi_tabele(conn)
    conn.commit()
    conn.close()


conn = sqlite3.connect('baza.db')

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
        '''vrne id ter ime klienta'''

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
        Preveri, ali sta uporabniško ime in geslo pravilna.
        """
        sql = """
            SELECT id, geslo, ime, naziv FROM agent
            WHERE kontakt = ?
        """
        result = conn.execute(sql, [ime]).fetchone()
        id, geslo, agent, naziv = result
        return (geslo, id, agent, naziv)


        
    def klienti_agenta(id_agenta):
        '''vrne vse kliente ki jih ima agent'''

        sql = """
            SELECT klienti.id, klienti.ime,klienti.kontakt, klienti.buget,klienti.lokacija,klienti.vrsta FROM klienti
            JOIN zastopa on id_klient=klienti.id
            WHERE id_agent= ?;
            """
        results = []
        for id, ime, kontakt, buget, lokacija, vrsta in conn.execute(sql, [id_agenta]):
            results.append(Klienti(id, ime, kontakt, buget, lokacija, vrsta))
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




class Klienti:
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
    def dodaj_klienta(ime, kontakt, buget, lokacija, vrsta):
        '''doda klienta'''

        sql = """
            INSERT INTO klienti (ime, kontakt,buget,lokacija,vrsta) VALUES (?,?,?,?,?);
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
    def klienti():
        '''vrne id ter ime klienta'''

        sql = """
            SELECT id, ime FROM klienti;
            """
        results = []
        for id, ime  in conn.execute(sql):
            results.append((id, ime))
        return results

    @staticmethod
    def id_klienti(kontakt):
        '''vrne id ter ime klienta'''

        sql = """
            SELECT id FROM klienti
            where kontakt=?;
            """
        
        id = conn.execute(sql,[kontakt]).fetchone()[0]
        return id


    @staticmethod
    def agenti(id_klient):
        '''vrne katere vse agente ima klient'''

        sql = """
            SELECT agent.id, agent.ime, agent.kontakt, agent.geslo,agent.naziv FROM agent
            JOIN zastopa on id_agent=agent.id
            WHERE id_klient= ?;
            """
        results = []
        for id, ime, kontakt, geslo, naziv  in conn.execute(sql, [id_klient]):
            results.append(Agenti(id, ime, kontakt, geslo, naziv))
        return results
    
    @staticmethod
    def nepremicnine(id_klient):
        '''vrne katere vse nepremicnine lahko zanimajo klienta'''

        sql = """
            SELECT nepremicnine.id, nepremicnine.lastnik, nepremicnine.cena, nepremicnine.vrsta,lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            WHERE id_klient = ?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_klient]):
            results.append(Nepremicnine(id,lastnik,cena,vrsta,lokacija))
        return results
    
    @staticmethod
    def klienti_agenta(id_agent):
        '''vrne katere vse kliente od agenta'''

        sql = """
            SELECT id, ime FROM klienti
            JOIN zastopa ON klienti.id=zastopa.id_klient
            WHERE zastopa.id_agent = ?;
            """
        results = []
        for id, ime in conn.execute(sql, [id_agent]):
            results.append((id,ime))
        return results
    
    @staticmethod
    def vsi_klienti():
        '''vrne katere vse kliente'''

        sql = """
            SELECT id, ime, kontakt, buget,lokacija,vrsta FROM klienti
            """
        results = []
        for id, ime, kontakt, buget,lokacija,vrsta in conn.execute(sql, []):
            results.append(Klienti(id, ime, kontakt, buget,lokacija,vrsta))
        return results




class Nepremicnine:
    def __init__ (self, id, lastnik, cena, vrsta, lokacija):
        self.id=id
        self.lastnik = lastnik
        self.cena=cena
        self.vrsta=vrsta
        self.lokacija=lokacija

    def __str__(self):
        return f'id: {self.id}, Lastnik: {self.lastnik}, Cena: {self.cena}, Lokacija: {self.lokacija}, Vrsta: {self.vrsta}'

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
    def klienti(id_nepremicnina):
        '''kateri klienti odgovarjajo tisti nepremicnini'''

        sql = """
            SELECT id,ime,kontakt,buget,lokacija,vrsta FROM klienti
            JOIN interes ON klienti.id=id_klient
            WHERE id_nepremicnine= ?;
            """
        results = []
        for id,ime,kontakt,buget,lokacija,vrsta  in conn.execute(sql, [id_nepremicnina]):
            results.append(Klienti(id,ime,kontakt,buget,lokacija,vrsta))
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
    def pogled_agenta(id_agenta, id_klienta):
        '''vrne vse neopremicnine ka odgovarjajo enemu klientu od enega agenta'''

        sql = """
            SELECT id, lastnik, cena, vrsta, lokacija FROM nepremicnine
            JOIN interes ON nepremicnine.id=id_nepremicnine
            JOIN zastopa on zastopa.id_klient=interes.id_klient
            WHERE interes.id_klient=? and zastopa.id_agent=?;
            """
        results = []
        for id, lastnik, cena, vrsta, lokacija  in conn.execute(sql, [id_klienta, id_agenta]):
            results.append(Nepremicnine(id, lastnik, cena, vrsta, lokacija))
        return results

class Zastopa:
    def __init__(self,klient,agent):
        self.klient=klient
        self.agent=agent

    @staticmethod
    def agent_klient(id_klient, id_agent):
        '''doda klienta agentu'''

        check_sql = """
            SELECT COUNT(*) FROM zastopa WHERE id_klient = ? AND id_agent = ?;
        """

        cursor = conn.execute(check_sql, [id_klient, id_agent])
        count = cursor.fetchone()[0]

        if count == 0:
            insert_sql = """
                INSERT INTO zastopa (id_klient, id_agent) VALUES (?, ?);
            """
            conn.execute(insert_sql, [id_klient, id_agent])
            conn.commit()

class Interes:
    def __init__(self,klient,nepremicnina):
        self.klient=klient
        self.nepremicnina=nepremicnina

    @staticmethod
    def dodaj_interes(id_klient):
        '''Pregleda katere nepremicnine ustrezajo klientu'''

        sql = """
            INSERT INTO interes (id_klient, id_nepremicnine)
            SELECT ?, t2.id
            FROM nepremicnine AS t2
            JOIN klienti AS t1 ON t1.vrsta = t2.vrsta AND t1.lokacija = t2.lokacija
            WHERE t1.id = ? AND t1.buget >= t2.cena;
        """
        
        conn.execute(sql, (id_klient, id_klient))
        conn.commit()

# for item in Nepremicnine.f_manjse_od_cena(200000):
#     print(item)

# for elt in Agenti.klienti_agenta(2):
#     print(elt)
# print(Nepremicnine.vse_lokacije())

# for item in Nepremicnine.f_lokacija('Ljubljana'):
#     print(item)

# for item in Nepremicnine.f_vrsta_nepremicnine("hisa"):
#     print(item)

# for elt in Klienti.agenti(5):
#     print(elt)

# print(Klienti)
# for elt in Klienti.nepremicnine(2):
#     print(elt)

# print(Nepremicnine.klienti(4))
# for item in Nepremicnine.klienti(4):
#     print(item)

# Klienti.dodaj_klienta("ime", "kontakt", 6000, "lokacija", "vrsta")
#Agenti.dodaj_agenta("neki", "neki", "neki", 1)
#Nepremicnine.dodaj_nepremicnino("ndki", 90, "hisa", "Tudjemili")

# for item in Nepremicnine.pogled_agenta(2,131):
#     print(item)

#conn.commit()
#conn.close()
