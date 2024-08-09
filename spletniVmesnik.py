import bottle
from model2 import Agenti, Klijenti, Nepremicnine, Zastopa, Interes
import secrets
#from model2 import pripravi_bazo


#pripravi_bazo()

# Generate a random secret key
secret_key = "bla"
secrets.token_hex(32)


@bottle.get('/')
def naslovna_stran():

    bottle.response.delete_cookie('id', path='/')
    bottle.response.delete_cookie('UpIme', path='/')
    bottle.response.delete_cookie('naziv', path='/')
    print("po brisanju")
    print(bottle.request.get_cookie("id",secret=secret_key))
    print(bottle.request.get_cookie("UpIme",secret=secret_key))
    print(bottle.request.get_cookie("naziv",secret=secret_key))
    return bottle.template('osnova.html', napaka=None)


@bottle.route('/prijava', method=['GET', 'POST'])
def prijava():
    if bottle.request.method == 'POST':
        try:
            print("pred nastavlajnjem")
            print(bottle.request.get_cookie("id",secret=secret_key))
            print(bottle.request.get_cookie("UpIme",secret=secret_key))
            print(bottle.request.get_cookie("naziv",secret=secret_key))
            ime = bottle.request.forms.get('uporabnisko_ime')
            geslo1 = bottle.request.forms.get('geslo')
            

            (geslo2,id,agent,naziv)= Agenti.geslo(ime)

            bottle.response.set_cookie("naziv",str(naziv),secret=secret_key,path='/')
            bottle.response.set_cookie("id",str(id),secret=secret_key,path='/')
            bottle.response.set_cookie("UpIme",str(agent),secret=secret_key,path='/')
            """
            bottle.response.set_cookie("naziv_p",str(naziv),secret=secret_key,path='/prijava')
            bottle.response.set_cookie("id_p",str(id),secret=secret_key,path='/prijava')
            bottle.response.set_cookie("UpIme_p",str(agent),secret=secret_key,path='/prijava')
            """



            print(agent)
            print(geslo1)
            print(geslo2)
            print(bottle.request.get_cookie("id",secret=secret_key))
            print(bottle.request.get_cookie("UpIme",secret=secret_key))
            print(bottle.request.get_cookie("naziv",secret=secret_key))
            """
            print(bottle.request.get_cookie("id_p",secret=secret_key))
            print(bottle.request.get_cookie("UpIme_p",secret=secret_key))
            print(bottle.request.get_cookie("naziv_p",secret=secret_key))
            """
            if geslo1==geslo2:
                if naziv==1:
                    klijenti = Agenti.klijenti_agenta(int(id))
                    return bottle.template('agent.html', klijenti=klijenti,ime_agent=agent,uporabnik_id=int(naziv))
                    
                elif naziv==0:
                    return bottle.template('boss.html', ime_agent=agent,uporabnik_id=int(naziv))

               
            else:
                return bottle.template('prijava.html', napaka="Napačno uporabniško ime ali geslo.")
            
        except Exception as e:
            # Handle exceptions gracefully
            print(f"An error occurred: {e}")
            return bottle.template('prijava.html', napaka="Napačno uporabniško ime ali geslo.")
  
    else:
                        
        return bottle.template('prijava.html', napaka=None)



@bottle.route('/agent', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')

    if selected_action == 'nepremicnine':
        bottle.redirect('/nepremicnine')
    elif selected_action == 'klijenti':
        bottle.redirect('/klijenti')
    else:
        return "Invalid action selected"

@bottle.route('/klijenti')
def klijenti():
    return bottle.template('klijenti.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    print(bottle.request.get_cookie("UpIme",secret=secret_key))
    if selected_action == 'nepremicnine':
        bottle.redirect('/nepremicnine')
    elif selected_action == 'agenti':
        bottle.redirect('/agenti')
    elif selected_action == 'klijenti_boss':
        bottle.redirect('/klijenti_boss')
    else:
        return "Invalid action selected"

@bottle.route('/klijenti_boss')
def klijenti_boss():
    print(bottle.request.get_cookie("id",secret=secret_key))
    print(bottle.request.get_cookie("UpIme",secret=secret_key))
    print(bottle.request.get_cookie("naziv",secret=secret_key))
    return bottle.template('klijenti_boss.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/agenti')
def agenti():
    return bottle.template('agenti.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/agenti', method='POST')
def agenti():
    selected_action = bottle.request.forms.get('actions')
    print(bottle.request.get_cookie("UpIme",secret=secret_key))
    if selected_action == 'dodaj-agenta':
        bottle.redirect('/dodaj-agenta')
    elif selected_action == 'klijenti-agenta':
        bottle.redirect('/klijenti_agenta_izbor')
    elif selected_action == 'vsi-agenti':
        bottle.redirect('/vsi_agenti')
    else:
        return "Invalid action selected"

@bottle.route('/nepremicnine')
def nepremicnine():
    return bottle.template('nepremicnine.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/nepremicnine', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-nepremicnino':
        bottle.redirect('/dodaj-nepremicnino')
    elif selected_action == 'brskaj-nepremicnine':
        bottle.redirect('/brskaj_nepremicnine')
    elif selected_action == 'vse-nepremicnine':
        bottle.redirect('/vse_nepremicnine')
    else:
        return "Invalid action selected"
    
@bottle.route('/klijenti', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-klijenta':
        bottle.redirect('/dodaj-klijenta')
    elif selected_action == 'nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-klijenta-agent')
    else:
        return "Invalid action selected"
    
@bottle.route('/klijenti_boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-klijenta':
        bottle.redirect('/dodaj-klijenta')
    elif selected_action == 'vsi-klijenti':
        bottle.redirect('/vsi-klijenti')
    elif selected_action == 'agenti-klijenta':
        bottle.redirect('/select-klijenta')
    elif selected_action == 'Nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-klijenta-boss')
    else:
        return "Invalid action selected"

@bottle.route('/brskaj_nepremicnine')
def brskaj_nepremicnine():
    return bottle.template('brskaj_nepremicnine.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/brskaj_nepremicnine', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'vse-lokacije':
        bottle.redirect('/vse-lokacije')
    elif selected_action == 'na-lokaciji':
        bottle.redirect('/na-lokaciji')
    elif selected_action == 'manjse-od-cene':
        bottle.redirect('/manjse-od-cene')
    elif selected_action == 'glede-na-vrsto':
        bottle.redirect('/glede-na-vrsto')
    else:
        return "Invalid action selected"

######################################################################################gor meniji

@bottle.route('/dodaj-klijenta')
def dodaj_klijenta():
    return bottle.template('dodaj_klijenta.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),napaka=None,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/pregled-nepremicnine')
def pregled_nepremicnine():
    lokacije = Nepremicnine.vse_lokacije()
    return bottle.template('pregled_nepremicnin.html', lokacije=lokacije,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/pregled-klijente')
def pregled_klijente():
    return bottle.template('pregled_klijente.html')

@bottle.route('/dodaj-nepremicnino', method=['GET', 'POST'])
def dodaj_nepremicnino():
    if bottle.request.method == 'POST':
        # Handle the form submission
        lastnik = bottle.request.forms.get('lastnik')
        cena = bottle.request.forms.get('cena')
        vrsta = bottle.request.forms.get('vrsta')
        lokacija = bottle.request.forms.get('lokacija')

        # Here, you should validate the inputs (e.g., check if fields are not empty, if 'cena' is a valid number, etc.)
        if not lastnik or not cena or not vrsta or not lokacija:
            return bottle.template('dodaj_nepremicnino.html', napaka="Please fill in all the fields.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))
        
        try:
            # Convert 'cena' to a number if necessary (depending on your storage logic)
            cena = int(cena)
        except ValueError:
            return bottle.template('dodaj_nepremicnino.html', napaka="Please enter a valid number for price.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

     
        Nepremicnine.dodaj_nepremicnino(lastnik,cena,vrsta,lokacija)
       

        return bottle.redirect("/nepremicnine")
    else:
        # Display the form for adding a new property
        return bottle.template('dodaj_nepremicnino.html', napaka=None, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/dodaj-agenta', method=['GET', 'POST'])
def dodaj_agenta():
    if bottle.request.method == 'POST':
        # Retrieve form data
        ime = bottle.request.forms.get('ime')
        kontakt = bottle.request.forms.get('kontakt')
        geslo = bottle.request.forms.get('geslo')
        naziv = bottle.request.forms.get('naziv')

        # Basic validation
        if not ime or not kontakt or not geslo or not naziv:
            return bottle.template('dodaj_agenta.html', napaka="Vsa polja so obvezna.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))
        
        Agenti.dodaj_agenta(ime, kontakt, geslo, naziv)

        return bottle.redirect('/agenti') 
    else:
        return bottle.template('dodaj_agenta.html', napaka=None,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/dodaj-klijenta', method=['GET', 'POST'])
def dodaj_klijenta():
    if bottle.request.method == 'POST':
        # Retrieve form data
        ime = bottle.request.forms.get('ime')
        kontakt = bottle.request.forms.get('kontakt')
        budget = bottle.request.forms.get('budget')
        lokacija = bottle.request.forms.get('lokacija')
        vrsta = bottle.request.forms.get('vrsta')

        # Basic validation
        if not ime or not kontakt or not budget or not lokacija or vrsta not in ['apartment', 'house', 'land']:
            return bottle.template('dodaj_klijenta.html', napaka="Vsa polja so obvezna in vrsta mora biti apartment, house ali land.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

        try:
            budget = int(budget)
        except ValueError:
            return bottle.template('dodaj_klijenta.html', napaka="Budget mora biti številčna vrednost.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

       
        Klijenti.dodaj_klijenta(ime, kontakt, budget, lokacija, vrsta)

        
        return bottle.redirect('/klijenti') 
    else:
        return bottle.template('dodaj_klijenta.html', napaka=None,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#########################################################gor je dodajanje

#agenti klijenta
@bottle.route('/agenti-klijenta/<id_klijent:int>')
def agenti_klijenta(id_klijent):
    # Fetch agents associated with the buyer
    agenti = Klijenti.agenti(id_klijent)
    
    # Render the template with the list of agents
    return bottle.template('agenti_klijenta.html', id_klijent=id_klijent, agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/select-klijenta')
def select_klijenta():
    
    buyers = Klijenti.klijenti()  
    return bottle.template('agenti_klijenta_izbor.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klijenta', method='POST')
def handle_select_klijenta():
    id_klijenta = bottle.request.forms.get('id_klijenta')
    if id_klijenta:
        return bottle.redirect(f'/agenti-klijenta/{id_klijenta}')
    else:
        return "No buyer selected", 400
    
#nepremicnine ki lahko zanimajo klijenta za agente
@bottle.route('/select-klijenta-agent')
def select_klijenta():
    
    buyers = Klijenti.klijenti_agenta(int(bottle.request.get_cookie("id",secret=secret_key)))  
    return bottle.template('klijenta_izbor_agent.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klijenta_agent', method='POST')
def handle_select_klijenta():
    id_klijenta = bottle.request.forms.get('id_klijenta')
    if id_klijenta:
        return bottle.redirect(f'/neprem-klijenta_agent/{id_klijenta}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem-klijenta_agent/<id_klijent:int>')
def agenti_klijenta(id_klijent):
    # Fetch agents associated with the buyer
    nepremicnine = Klijenti.nepremicnine(id_klijent)
    
    # Render the template with the list of agents
    return bottle.template('nepremicnine_klijenta_agent.html', id_klijent=id_klijent, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#nepremicnine ki lahko zanimajo klijenta za boss
@bottle.route('/select-klijenta-boss')
def select_klijenta():
    
    buyers = Klijenti.klijenti()
    return bottle.template('klijenta_izbor_boss.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klijenta_boss', method='POST')
def handle_select_klijenta():
    id_klijenta = bottle.request.forms.get('id_klijenta')
    if id_klijenta:
        return bottle.redirect(f'/neprem-klijenta_agent/{id_klijenta}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem-klijenta_boss/<id_klijent:int>')
def agenti_klijenta(id_klijent):
    # Fetch agents associated with the buyer
    nepremicnine = Klijenti.nepremicnine(id_klijent)
    
    # Render the template with the list of agents
    return bottle.template('nepremicnine_klijenta_agent.html', id_klijent=id_klijent, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#klijenti agenta
@bottle.route('/klijenti_agenta_izbor')
def select_agent():
    
    agenti = Agenti.agenti()
    return bottle.template('izbor_agent.html', agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_agenta', method='POST')
def handle_select_agent():
    id_agenta = bottle.request.forms.get('id_agenta')
    print(f"Selected agent ID: {id_agenta}")  # Debug print
    if id_agenta:
        return bottle.redirect(f'/klijenti_agenta/{id_agenta}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/klijenti_agenta/<id_agenta:int>')
def agenti_klijenta(id_agenta):
    # Fetch agents associated with the buyer
    klijenti = Agenti.klijenti_agenta(int(id_agenta))
    
    # Render the template with the list of agents
    return bottle.template('klijenti_agenta.html', id_agenta=id_agenta, klijenti=klijenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#vsi klijenti
@bottle.route('/vsi-klijenti')
def vsi_klijenti():
    klijenti=Klijenti.vsi_klijenti()
    return bottle.template('vsi-klijenti.html',klijenti=klijenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#vsi agenti
@bottle.route('/vsi_agenti')
def vsi_agenti():
    agenti=Agenti.vsi_agenti()
    return bottle.template('vsi_agenti.html',agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


#vse nepremicnine
@bottle.route('/vse_nepremicnine')
def vse_nepremicnine():
    nepremicnine=Nepremicnine.vse_nepremicnine()
    return bottle.template('vse_nepremicnien.html',nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#brskaj nepremicnine
#vse lokacije

@bottle.route('/vse-lokacije')
def vse_lokacije():
    lokacije=Nepremicnine.vse_lokacije()
    return bottle.template('vse-lokacije.html',lokacije=lokacije,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#filtriranje glede na lokacije
@bottle.route('/na-lokaciji')
def na_lokaciji():
    
    lokacije=Nepremicnine.vse_lokacije()
    return bottle.template('na-lokaciji-izbor.html', lokacije=lokacije,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/poslji-lokacijo', method='POST')
def poslji_lokacijo():
    lokacija = str(bottle.request.forms.get('lokacija'))
    if lokacija:
        return bottle.redirect(f'/neprem_na_lokaciji/{lokacija}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem_na_lokaciji/<lokacija>')
def neprem_na_lokaciji(lokacija):
    nepremicnine = Nepremicnine.f_lokacija(lokacija)
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#filtriraj glede na ceno(manjse)
@bottle.route('/manjse-od-cene')
def manjse_od_cene():
    return bottle.template('manjse-od-cene.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/max-cena', method='POST')
def poslji_ceno():
    budget = bottle.request.forms.get('budget')
    if budget:
        return bottle.redirect(f'/neprem_pod_ceno/{budget}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem_pod_ceno/<budget>')
def neprem_pod_ceno(budget):
    nepremicnine = Nepremicnine.f_manjse_od_cena(budget)
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#filtriraj glede na vrsto
@bottle.route('/glede-na-vrsto')
def glede_na_vrsto():
    
    vrste=Nepremicnine.vse_vrste()
    return bottle.template('vrste-izbor.html', vrste=vrste, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/poslji-vrsto', method='POST')
def poslji_vrsto():
    vrsta = str(bottle.request.forms.get('vrsta'))
    if vrsta:
        return bottle.redirect(f'/neprem_vrste/{vrsta}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem_vrste/<vrsta>')
def neprem_vrste(vrsta):
    nepremicnine = Nepremicnine.f_vrsta_nepremicnine(vrsta)
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))




bottle.run(debug=True, reloader=True)