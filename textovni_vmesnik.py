from pomozne import *
from model import *

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

@prekinitev
def agenti_klijenta():
    """
    izpiše agente klijenta
    """
    id_klijent=input("id_klijenta")
    vrne = Klijenti.agenti(id_klijent)
    for el in vrne:
        print(el)

@prekinitev
def vsi_klijenti():
    """
    izpiše vse klijente
    """
    
    vrne=Klijenti.vsi_klijenti()
    for el in vrne:
        print(el)

@prekinitev
def vse_nepremicnine():
    """
    izpiše vse nepremicnine
    """
    
    vrne=Nepremicnine.vse_nepremicnine()
    for el in vrne:
        print(el)

@prekinitev
def vse_lokacije():
    """
    izpiše vse lokacije
    """
    
    vrne=Nepremicnine.vse_lokacije()
    for el in vrne:
        print(el)

class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    Nepremicnine  = ('Izpiši nepremicnine s ceno manjšo od: ', manse_od_cene)
    Agenti=("izpise vse agente klijenta: ", agenti_klijenta)
    Klijenti=("izpise vse klijente: ", vsi_klijenti)
    Nepremicnine2=("vse nepremicnine: " ,vse_nepremicnine)
    Nepremicnine3=("vse lokacije nepremicnin: " ,vse_lokacije)
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