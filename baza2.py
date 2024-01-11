import csv

PARAM_FMT = ":{}" # za PostgreSQL/MySQL


class Tabela:

    ime = None #ime tabele
    podatki = None #ime datoteke s podatki

    def __init__(self, conn, ime = None, podatki = None):
        self.conn = conn
        self.ime = ime
        self.podatki = podatki

    def ustvari(self):
        """zdej nic ne dela, pol ustvarimo za vsak razred za se"""
        raise NotImplementedError
    
    def izbrisi(self):
        """izbrise tabelo"""
        self.conn.execute(f"DROP TABLE IF EXISTS {self.ime};")
    
    def uvozi(self, encoding = "UTF-8"):
        if self.podatki is None:
            return None
        with open(self.podatki, encoding=encoding) as datoteka:
            podatki = csv.reader(datoteka)
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
                self.dodaj_vrstico(**vrstica)

    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute(f"DELETE FROM {self.ime};")

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.

        Argumenti:
        - stolpci: seznam stolpcev
        """
        return f"""
            INSERT INTO {self.ime} ({", ".join(stolpci)})
            VALUES ({", ".join(PARAM_FMT.format(s) for s in stolpci)});
        """

    def dodaj_vrstico(self, **podatki):
        """
        Metoda za dodajanje vrstice.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items()
                   if vrednost is not None}
        print(podatki)
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid


class Agenti(Tabela):
    """
    Tabela za uporabnike.
    """
    ime = "agenti"
    podatki = "podatki/agenti.csv"

    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE agent(
            id integer PRIMARY KEY AUTOINCREMENT,
            ime text NOT NULL,
            kontakt text NOT NULL,
            geslo text NOT NULL,
            naziv integer NOT NULL
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj uporabnika.

        Če sol ni podana, zašifrira podano geslo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """

        assert "ime" in podatki
        cur = self.conn.execute("""
            SELECT id FROM agenti
            WHERE ime = :ime;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            return id
        
    def uvozi(self, encoding = "UTF-8"):
        super().uvozi()
        
        
class Kupci(Tabela):
    """
    Tabela za kupce.
    """
    ime = "kupci"
    podatki = "podatki/kupci.csv"

    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE kupec(
            id integer PRIMARY KEY AUTOINCREMENT,
            ime text NOT NULL,
            kontakt text NOT NULL,
            Cena integer NOT NULL CHECK (Cena > 0),
            Lokacija text NOT NULL
            );
        """)

    def uvozi(self, encoding = "UTF-8"):
        super().uvozi()
        

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj uporabnika.

        Če sol ni podana, zašifrira podano geslo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """

        assert "ime" in podatki
        cur = self.conn.execute("""
            SELECT id FROM agenti
            WHERE ime = :ime;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)

class Nepremicnine(Tabela):
    """
    Tabela za nepremicnine.
    """
    ime = "nepremicnine"
    podatki = "podatki/nepremicnine.csv"

    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE nepremicnine(
            id integer PRIMARY KEY AUTOINCREMENT,
            Prodajalec text NOT NULL,
            Cena integer NOT NULL CHECK (Cena > 0),
            Vrsta text,
            Lokacija text NOT NULL,
            Opis text
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj uporabnika.

        Če sol ni podana, zašifrira podano geslo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """

        assert "ime" in podatki
        cur = self.conn.execute("""
            SELECT id FROM agenti
            WHERE ime = :ime;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)

class Zastopa(Tabela):
    """
    Tabela kdo zastopa koga - agenti/kljenti.
    """
    ime = "zastopa"
    podatki = "podatki/zastopa.csv"


    # def __init__(self, conn, oznaka):
    #     ''''''

    #     super().__init__(conn)
    #     self.oznaka = oznaka


    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE zastopa(
            id_kupec integer REFERENCES kupec(id),
            id_agent integer REFERENCES agent(id),
            PRIMARY KEY (id_kupec, id_agent)
            );
        """)

    def dodaj_vrstico(self, **podatki):
        """
        Dodaj uporabnika.

        Če sol ni podana, zašifrira podano geslo.

        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        return
    
class Interes(Tabela):
    """
    Tabela kdo zastopa koga - agenti/kljenti.
    """
    ime = "interes"
    #podatki = "podatki/zastopa.csv"

    def ustvari(self):
        """
        Ustvari tabelo uporabnik.
        """
        self.conn.execute("""
            CREATE TABLE interes(
            id_kupec integer REFERENCES kupec(id),
            id_nepremicnine integer REFERENCES nepremicnine(id),
            PRIMARY KEY (id_kupec, id_nepremicnine)
            );
        """)


def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()


def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    for t in tabele:
        t.izbrisi()


def uvozi_podatke(tabele):
    """
    Uvozi podatke v podane tabele.
    """
    for t in tabele:
        t.uvozi()


def izprazni_tabele(tabele):
    """
    Izprazni podane tabele.
    """
    for t in tabele:
        t.izprazni()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)
    uvozi_podatke(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    agenti = Agenti(conn)
    kupci = Kupci(conn)
    nepremicnine = Nepremicnine(conn)
    zastopa = Zastopa(conn)
    interes = Interes(conn)
    return [agenti, kupci, nepremicnine, zastopa, interes]

def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)


