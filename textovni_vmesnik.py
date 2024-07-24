from pomozne import *
from model2 import *

def vnesi_izbiro(moznosti):
    """
    Uporabniku da na izbiro podane možnosti.
    """
    moznosti = list(moznosti)
    for i, moznost in enumerate(moznosti, 1):
        print(f'{i}) {moznost}')
    izbira = None
    while True:
        try:
            izbira = int(input('> ')) - 1
            return moznosti[izbira]
        except (ValueError, IndexError):
            print("Napačna izbira!")

def domov():
    """
    Pozdravi pred izhodom.
    """
    print('Adijo!')

@prekinitev
def manse_od_cene():
    """
    izpiše filme z ceno pod max_cena
    """
    max_cena=input("maxsimalna cena")
    vrne=Nepremicnine.f_manjse_od_cena(max_cena)
    for el in vrne:
        print(el)


class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    Nepremicnine  = ('Izpiši nepremicnine s ceno manjšo od: ', manse_od_cene)
    #POGLEDAL_DOBRE_FILME = ('Pogledal dobre filme', najboljsi_filmi)
    #DODAL_OSEBO = ('Dodal osebo', dodajanje_osebe)
    #DODAL_FILM = ('Dodal film', dodajanje_filma)
    SEL_DOMOV = ('Šel domov', domov)


@prekinitev
def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi Nepremicnine!')
    while True:
        print('Kaj bi rad počel?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return


glavni_meni()