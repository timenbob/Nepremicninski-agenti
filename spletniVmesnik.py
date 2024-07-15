import bottle
from model2 import Agenti, Kupci, Nepremicnine, Zastopa, Interes


@bottle.get('/')
def naslovna_stran():
    return bottle.template('osnova.html', napaka=None)

@bottle.route('/prijava/', method=['GET', 'POST'])
def prijava():
    """ime = bottle.request.forms.get('ime')
    geslo1 = bottle.request.forms.get('geslo')
    geslo2=Agenti.geslo(ime)

    if ime == 'admin' and geslo1 == 'admin':
        bottle.redirect('/izpolnitev/')
    else:"""
    return bottle.template('agent.html')

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

# Route for adding a property
@bottle.route('/dodaj-nepremicnino')
def dodaj_nepremicnino():
    return bottle.template('dodaj_nepremicnino')

# Route for viewing properties
@bottle.route('/pregled-nepremicnine')
def pregled_nepremicnine():
    lokacije = Nepremicnine.vse_lokacije()
    return bottle.template('pregled_nepremicnine', lokacije=lokacije)

# Route for viewing buyers
@bottle.route('/pregled-stranke')
def pregled_stranke():
    # You can add logic here to retrieve and display buyers
    return bottle.template('pregled_stranke')

@bottle.route('/handle-dodaj-nepremicnino', method='POST')
def handle_dodaj_nepremicnino():
    lastnik = bottle.request.forms.get('lastnik')
    cena = bottle.request.forms.get('cena')
    vrsta = bottle.request.forms.get('vrsta')
    lokacija = bottle.request.forms.get('lokacija')

    # Insert property into database
    nepremicnina = Nepremicnine(lastnik=lastnik, cena=cena, vrsta=vrsta, lokacija=lokacija, id=None)
    # You need to implement the method to insert into database in your model2 module
    # Example: baza2.dodaj_nepremicnino(conn, nepremicnina)

    return bottle.redirect('/')

@bottle.route('/handle-dodaj-stranko', method='POST')
def handle_dodaj_stranko():
    ime = bottle.request.forms.get('ime')
    kontakt = bottle.request.forms.get('kontakt')
    
    # Create a new buyer object and insert into database
    kupci = Kupci(ime=ime, kontakt=kontakt, buget=0, lokacija="", vrsta="", id=None)
    # You need to implement the method to insert into database in your model2 module
    # Example: baza2.dodaj_kupca(conn, kupci)
    
    return bottle.redirect('/')

bottle.run(debug=True, reloader=True)