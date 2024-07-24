import bottle
from model2 import Agenti, Kupci, Nepremicnine, Zastopa, Interes


@bottle.get('/')
def naslovna_stran():
    return bottle.template('osnova.html', napaka=None)


@bottle.route('/prijava/', method=['GET', 'POST'])
def prijava():
    if bottle.request.method == 'POST':
        ime = bottle.request.forms.get('uporabnisko_ime')
        geslo1 = bottle.request.forms.get('geslo')
        geslo2 = Agenti.geslo(ime)

        if geslo1==geslo2:
            bottle.redirect('/dodaj-stranko')
        else:
            return bottle.template('prijava.html', napaka="Napačno uporabniško ime ali geslo.")
    else:
        return bottle.template('prijava.html', napaka=None)


@bottle.route('/handle-form', method='POST')
def handle_form():
    selected_action = bottle.request.forms.get('actions')

    if selected_action == 'dodaj-stranko':
        bottle.redirect('/dodaj-stranko')
    elif selected_action == 'dodaj-nepremicnino':
        bottle.redirect('/dodaj-nepremicnino')
    elif selected_action == 'pregled-nepremicnine':
        bottle.redirect('/pregled-nepremicnine')
    elif selected_action == 'pregled-stranke':
        bottle.redirect('/pregled-stranke')
    else:
        return "Invalid action selected"


@bottle.route('/dodaj-stranko')
def dodaj_stranko():
    return bottle.template('dodaj_stranko')


@bottle.route('/dodaj-nepremicnino')
def dodaj_nepremicnino():
    return bottle.template('dodaj_nepremicnino')


@bottle.route('/pregled-nepremicnine')
def pregled_nepremicnine():
    lokacije = Nepremicnine.vse_lokacije()
    return bottle.template('pregled_nepremicnine', lokacije=lokacije)


@bottle.route('/pregled-stranke')
def pregled_stranke():
    return bottle.template('pregled_stranke')


@bottle.route('/handle-dodaj-nepremicnino', method='POST')
def handle_dodaj_nepremicnino():
    lastnik = bottle.request.forms.get('lastnik')
    cena = bottle.request.forms.get('cena')
    vrsta = bottle.request.forms.get('vrsta')
    lokacija = bottle.request.forms.get('lokacija')

    nepremicnina = Nepremicnine(lastnik=lastnik, cena=cena, vrsta=vrsta, lokacija=lokacija, id=None)

    return bottle.redirect('/')


@bottle.route('/handle-dodaj-stranko', method='POST')
def handle_dodaj_stranko():
    ime = bottle.request.forms.get('ime')
    kontakt = bottle.request.forms.get('kontakt')

    kupci = Kupci(ime=ime, kontakt=kontakt, buget=0, lokacija="", vrsta="", id=None)

    return bottle.redirect('/')


bottle.run(debug=True, reloader=True)
