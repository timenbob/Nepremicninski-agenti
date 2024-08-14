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
    max_cena=input("Najvišja cena: ")
    vrne=Nepremicnine.f_manjse_od_cena(max_cena)
    for el in vrne:
        print(el)

@prekinitev
def agenti_klijenta():
    """
    izpiše agente klijenta
    """
    id_klijent=input("Id_klijenta: ")
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
        print(el[0])

class GlavniMeni(Meni):
    """
    Izbire v glavnem meniju.
    """
    Nepremicnine  = ('Izpiši nepremičnine s ceno manjšo od: ', manse_od_cene)
    Agenti=("Izpiše vse agente klijenta: ", agenti_klijenta)
    Klijenti=("Izpiše vse klijente: ", vsi_klijenti)
    Nepremicnine2=("Vse nepremičnine: " ,vse_nepremicnine)
    Nepremicnine3=("Vse lokacije nepremičnin: " ,vse_lokacije)
    SEL_DOMOV = ('Šel domov', domov)


@prekinitev
def glavni_meni():
    """
    Prikazuje glavni meni, dokler uporabnik ne izbere izhoda.
    """
    print('Pozdravljen v bazi Nepremicnine!')
    while True:
        print('Kaj bi radi počeli?')
        izbira = vnesi_izbiro(GlavniMeni)
        izbira.funkcija()
        if izbira == GlavniMeni.SEL_DOMOV:
            return


glavni_meni()