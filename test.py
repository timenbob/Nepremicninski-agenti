import baza2
import sqlite3
from sqlite3 import IntegrityError
#from geslo import sifriraj_geslo, preveri_geslo

conn = sqlite3.connect('agenti.db')
conn.execute('PRAGMA foreign_keys = ON')

agenti = baza2.pripravi_tabele(conn)
baza2.uvozi_podatke(agenti)



conn.commit()



