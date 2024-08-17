# Nepremičninski agent
Ta projekt smo razvili za predmet Podatkovne baze 1 in je namenjen zaposlenim v podjetju, ki posluje z nepremičninami. Omogoča upravljanje podatkov o agentih, klientih in nepremičninah preko spletnega vmesnika. Glavni cilj projekta je omogočiti agentom in lastnikom podjetja enostaven dostop in analizo podatkov.

## Shema Baze
![Shema baze](https://github.com/timenbob/Nepremicninski-agenti/blob/main/Shema%20Baza.jpg)

## Opis baze
Baza podatkov vsebuje šest tabel, ki so med seboj povezane in omogočajo celovito upravljanje podatkov:<br>
Shranjuje informacije o agentih, vključno z ID-jem, imenom, kontaktnimi podatki (ki se uporabljajo za prijavo), geslom in nazivom. Naziv določa, katere podatke lahko agent vidi in upravlja.<br>
Klienti: Vsebuje podatke o klientih, kot so ID, ime, kontakt, proračun, lokacija in vrsta nepremičnine, ki jo iščejo.<br>
Shranjuje podatke o nepremičninah, vključno z ID-jem, lastnikom, ceno, vrsto in lokacijo.<br>
<br>
Interes: Vsebuje podatke o tem, katere nepremičnine ustrezajo posameznim klientom.<br>
Zastopa: Beleži, kateri agent zastopa določenega klienta.<br>

## Povezave
Agent ima lahko 0 ali več klientov.<br>
Klient (kupec) ima lahko enega ali več agentov.<br>
Klientu lahko ustreza 0 ali več nepremičnin.<br>
Nepremičnina lahko ustreza 0 ali več klientom.<br>

## Postopek uporabe
Prenesite celoten repozitorij in zaženite spletni vmesnik.<br>
Ob prijavi v sistem vnesite kontakt in geslo, ki ju najdete v tabeli Agenti.<br>
Primeri:<br>
Kontakt: masch0@lycos.com, Geslo: password123 (Agent)<br>
Kontakt: neki@neki.com, Geslo: password (Lastnik)<br>
Glede na uporabljene prijavne podatke boste dobili dostop do pogleda agenta ali lastnika.<br>

### Upravljanje
#### Agent
Ob prijavi kot agent lahko analizirate nepremičnine in pregledate le svoje kliente.<br>
Omogočeno je dodajanje novih agentov in nepremičnin.<br>
Na osnovni meni se lahko vrnete z uporabo gumbov za korake nazaj ali s klikom na povezave v zgornjem desnem kotu.
#### Lastnik
Lastnik ima dostop do vseh funkcionalnosti agenta ter dodatne možnosti:<br>
Pregled vseh agentov.<br>
Vpogled v vse kliente.

<br>
Ko končate z uporabo programa v Visual Studio, pritisnite Ctrl-C v terminalu, da se program ustrezno zaključi.


## Avtorji
Milica Vukićević<br>
Timen Bobnar
