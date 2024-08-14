# Nepremicninski agent
To je projekt, ki smo ga izdelali pri predmetu Podatkovne baze 1 <br>
Če želimo pognati projekt poženemo le spletni vmesnik.<br>
Sam projekt je mišljen za zaposlene v podjetju, ki posluje z nepremičninami.

## Shema Baze
![Shema baze](https://github.com/timenbob/Nepremicninski-agenti/blob/main/Shema%20Baza.jpg)

## Opis baze
Baza vsebuje 6 tabel:
Agenti, kjer se nahajajo informacije o agentih(id, ime, kontak(katerega se tudi uporabi pri prijavi), geslo, naziv). Naziv je pomemben, saj je odvisno od naziva kaj uporabnik lahko vse vidi.<br>
Klijenti, kjer se nahajajo vse informavije o klijentih(id, ime, kontakt, buget, lokacija, vrsta)<br>
Nepremicnine, kjer so vse informacije o nepremicninah(id, lastnik, cena, vrsta, lokacija)<br>
<br>
Interes: ta tabela vsebuje podatke o tem katere vse nepremicnine ustrezajo klijenu.<br>
Zatopa: ta tabela vsebuje podatke o tem katere klijenta ima posamezni agent.<br>

## Povezave
Agent ima lahko 0 ali več klijentov.<br>
Klijent(kupec) ima lahko enega ali več agentov.<br>
Klijentu lahko ustreza 0 ali več nepremičnin.<br>
Nepremičnina lahko ustreza 0 ali več klijentom.

## Postopek uporabe
Prenesemo celoten repozitorij ter poženemo spletni vmesnik. Ko kliknemo Prijava nas
program vpraša za kontakt ter geslo. Te podatke lahko pridobimo iz baze v tabeli agenti.<br>
Primer:<br>
kontakt                geslo<br>
masch0@lycos.com       password123<br>
neki@neki.com          password<br>

Če uporabimo prvega bomo pridobili pogled agenta. Če pa uporabimo drugega pa pridobimo pogled lastnika.<br>

### Upravlajnje
#### Agent
Ko se vpišemo kot agent, lahko analiziramo vse nepremicnine ter pregledujemo le svoje klijente. Lahko dodajamo agente ter nepremicnine. Ko izberemo kakšne možnosti, da se vrnemo na osnovni meni lahko uporabljamo korake nazaj oziroma v zgodnjem desnem kotu imamo povezave do osnovnoh izbir menija.

#### Lastnik
Lastnik imal poleg funkcionalnosti agentov tudi druge izbire. Lastnik lahko pregleduje tudi posamezen agente ter ima vpogled v vse klijente.


## Avtorji
Milica Vukićević<br>
Timen Bobnar
