import csv

with open("podatki/Agenti.csv", encoding="UTF-8") as datoteka:
            podatki = csv.reader(datoteka)
            stolpci = next(podatki)
            for vrstica in podatki:
                vrstica = {k: None if v == "" else v for k, v in zip(stolpci, vrstica)}
                print(vrstica)
