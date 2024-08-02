import bottle
from model2 import Agenti, Kupci, Nepremicnine, Zastopa, Interes
import secrets

# Generate a random secret key
secret_key = "bla"
secrets.token_hex(32)
print(secret_key) 

agent="heh"

@bottle.get('/')
def naslovna_stran():
    bottle.response.set_cookie("id", "", expires=0)
    bottle.response.set_cookie("UpIme", "", expires=0)

    return bottle.template('osnova.html', napaka=None)


@bottle.route('/prijava/', method=['GET', 'POST'])
def prijava():
    if bottle.request.method == 'POST':
        try:
            ime = bottle.request.forms.get('uporabnisko_ime')
            geslo1 = bottle.request.forms.get('geslo')
            

            (geslo2,id,agent,naziv)= Agenti.geslo(ime)
            bottle.response.set_cookie("id",str(id),secret=secret_key,path='/')
            bottle.response.set_cookie("UpIme",str(agent),secret=secret_key,path='/')

            neki=bottle.request.get_cookie("id",secret=secret_key)
            print(geslo1)
            print(geslo2)
            print(neki)
            print(bottle.request.get_cookie("UpIme",secret=secret_key))
            if geslo1==geslo2:
                if naziv==1:
                    klijenti = Agenti.klijenti_agenta(int(id))
                    return bottle.template('agent.html', klijenti=klijenti,ime_agent=agent)
                elif naziv==0:
                    return bottle.template('boss.html', ime_agent=agent)
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
    elif selected_action == 'kupci':
        bottle.redirect('/kupci')
    else:
        return "Invalid action selected"

@bottle.route('/kupci')
def kupci():
    return bottle.template('kupci.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    print(bottle.request.get_cookie("UpIme",secret=secret_key))
    if selected_action == 'nepremicnine':
        bottle.redirect('/nepremicnine')
    elif selected_action == 'agenti':
        bottle.redirect('/agenti')
    elif selected_action == 'kupci_boss':
        bottle.redirect('/kupci_boss')
    else:
        return "Invalid action selected"

@bottle.route('/kupci_boss')
def kupci_boss():
    return bottle.template('kupci_boss.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/agenti')
def agenti():
    return bottle.template('agenti.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
    return bottle.template('nepremicnine.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
    
@bottle.route('/kupci', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-stranko':
        bottle.redirect('/dodaj-stranko')
    elif selected_action == 'nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-kupca-agent')
    else:
        return "Invalid action selected"
    
@bottle.route('/kupci_boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-stranko':
        bottle.redirect('/dodaj-stranko')
    elif selected_action == 'vsi-kupci':
        bottle.redirect('/vsi-kupci')
    elif selected_action == 'agenti-kupca':
        bottle.redirect('/select-kupca')
    elif selected_action == 'Nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-kupca-boss')
    else:
        return "Invalid action selected"

@bottle.route('/brskaj_nepremicnine')
def brskaj_nepremicnine():
    return bottle.template('brskaj_nepremicnine.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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

@bottle.route('/dodaj-stranko')
def dodaj_stranko():
    return bottle.template('dodaj_kupca.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),napaka=None)


@bottle.route('/pregled-nepremicnine')
def pregled_nepremicnine():
    lokacije = Nepremicnine.vse_lokacije()
    return bottle.template('pregled_nepremicnin.html', lokacije=lokacije)


@bottle.route('/pregled-stranke')
def pregled_stranke():
    return bottle.template('pregled_stranke.html')

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
            return bottle.template('dodaj_nepremicnino.html', napaka="Please fill in all the fields.")
        
        try:
            # Convert 'cena' to a number if necessary (depending on your storage logic)
            cena = int(cena)
        except ValueError:
            return bottle.template('dodaj_nepremicnino.html', napaka="Please enter a valid number for price.")

     
        Nepremicnine.dodaj_nepremicnino(lastnik,cena,vrsta,lokacija)
       

        return bottle.redirect("/nepremicnine")
    else:
        # Display the form for adding a new property
        return bottle.template('dodaj_nepremicnino.html', napaka=None, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
            return bottle.template('dodaj_agenta.html', napaka="Vsa polja so obvezna.")
        
        Agenti.dodaj_agenta(ime, kontakt, geslo, naziv)

        return bottle.redirect('/agenti') 
    else:
        return bottle.template('dodaj_agenta.html', napaka=None,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))


@bottle.route('/dodaj-kupca', method=['GET', 'POST'])
def dodaj_kupca():
    if bottle.request.method == 'POST':
        # Retrieve form data
        ime = bottle.request.forms.get('ime')
        kontakt = bottle.request.forms.get('kontakt')
        budget = bottle.request.forms.get('budget')
        lokacija = bottle.request.forms.get('lokacija')
        vrsta = bottle.request.forms.get('vrsta')

        # Basic validation
        if not ime or not kontakt or not budget or not lokacija or vrsta not in ['apartment', 'house', 'land']:
            return bottle.template('dodaj_kupca.html', napaka="Vsa polja so obvezna in vrsta mora biti apartment, house ali land.")

        try:
            budget = int(budget)
        except ValueError:
            return bottle.template('dodaj_kupca.html', napaka="Budget mora biti številčna vrednost.")

       
        Kupci.dodaj_kupca(ime, kontakt, budget, lokacija, vrsta)

        
        return bottle.redirect('/kupci') 
    else:
        return bottle.template('dodaj_kupca.html', napaka=None)

#########################################################gor je dodajanje

#agenti kupca
@bottle.route('/agenti-kupca/<id_kupec:int>')
def agenti_kupca(id_kupec):
    # Fetch agents associated with the buyer
    agenti = Kupci.agenti(id_kupec)
    
    # Render the template with the list of agents
    return bottle.template('agenti_kupca.html', id_kupec=id_kupec, agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/select-kupca')
def select_kupca():
    
    buyers = Kupci.kupci()  
    return bottle.template('agenti_kupca_izbor.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/izbor_kupca', method='POST')
def handle_select_kupca():
    id_kupca = bottle.request.forms.get('id_kupca')
    if id_kupca:
        return bottle.redirect(f'/agenti-kupca/{id_kupca}')
    else:
        return "No buyer selected", 400
    
#nepremicnine ki lahko zanimajo kupca za agente
@bottle.route('/select-kupca-agent')
def select_kupca():
    
    buyers = Kupci.klijenti_agenta(int(bottle.request.get_cookie("id",secret=secret_key)))  
    return bottle.template('kupca_izbor_agent.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/izbor_kupca_agent', method='POST')
def handle_select_kupca():
    id_kupca = bottle.request.forms.get('id_kupca')
    if id_kupca:
        return bottle.redirect(f'/neprem-kupca_agent/{id_kupca}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem-kupca_agent/<id_kupec:int>')
def agenti_kupca(id_kupec):
    # Fetch agents associated with the buyer
    nepremicnine = Kupci.nepremicnine(id_kupec)
    
    # Render the template with the list of agents
    return bottle.template('nepremicnine_kupca_agent.html', id_kupec=id_kupec, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#nepremicnine ki lahko zanimajo kupca za boss
@bottle.route('/select-kupca-boss')
def select_kupca():
    
    buyers = Kupci.kupci()
    return bottle.template('kupca_izbor_boss.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/izbor_kupca_boss', method='POST')
def handle_select_kupca():
    id_kupca = bottle.request.forms.get('id_kupca')
    if id_kupca:
        return bottle.redirect(f'/neprem-kupca_agent/{id_kupca}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/neprem-kupca_boss/<id_kupec:int>')
def agenti_kupca(id_kupec):
    # Fetch agents associated with the buyer
    nepremicnine = Kupci.nepremicnine(id_kupec)
    
    # Render the template with the list of agents
    return bottle.template('nepremicnine_kupca_agent.html', id_kupec=id_kupec, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#klijenti agenta
@bottle.route('/klijenti_agenta_izbor')
def select_agent():
    
    agenti = Agenti.agenti()
    return bottle.template('izbor_agent.html', agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

@bottle.route('/izbor_agenta', method='POST')
def handle_select_agent():
    id_agenta = bottle.request.forms.get('id_agenta')
    print(f"Selected agent ID: {id_agenta}")  # Debug print
    if id_agenta:
        return bottle.redirect(f'/klijenti_agenta/{id_agenta}')
    else:
        return "No buyer selected", 400
    
@bottle.route('/klijenti_agenta/<id_agenta:int>')
def agenti_kupc(id_agenta):
    # Fetch agents associated with the buyer
    klijenti = Agenti.klijenti_agenta(int(id_agenta))
    
    # Render the template with the list of agents
    return bottle.template('klijenti_agenta.html', id_agenta=id_agenta, klijenti=klijenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#vsi klijenti
@bottle.route('/vsi-kupci')
def vsi_kupci():
    klijenti=Kupci.vsi_klijenti()
    return bottle.template('vsi-klijenti.html',klijenti=klijenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#vsi agenti
@bottle.route('/vsi_agenti')
def vsi_agenti():
    agenti=Agenti.vsi_agenti()
    return bottle.template('vsi_agenti.html',agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))


#vse nepremicnine
@bottle.route('/vse_nepremicnine')
def vse_nepremicnine():
    nepremicnine=Nepremicnine.vse_nepremicnine()
    return bottle.template('vse_nepremicnien.html',nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#brskaj nepremicnine
#vse lokacije

@bottle.route('/vse-lokacije')
def vse_lokacije():
    lokacije=Nepremicnine.vse_lokacije()
    return bottle.template('vse-lokacije.html',lokacije=lokacije,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#filtriranje glede na lokacije
@bottle.route('/na-lokaciji')
def na_lokaciji():
    
    lokacije=Nepremicnine.vse_lokacije()
    return bottle.template('na-lokaciji-izbor.html', lokacije=lokacije,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#filtriraj glede na ceno(manjse)
@bottle.route('/manjse-od-cene')
def manjse_od_cene():
    return bottle.template('manjse-od-cene.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#filtriraj glede na vrsto
@bottle.route('/glede-na-vrsto')
def glede_na_vrsto():
    
    vrste=Nepremicnine.vse_vrste()
    return bottle.template('vrste-izbor.html', vrste=vrste, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))




bottle.run(debug=True, reloader=True)