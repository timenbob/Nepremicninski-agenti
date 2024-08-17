import bottle
from model import Agenti, Klienti, Nepremicnine, Zastopa, Interes
import secrets

secret_key = "bla"
secrets.token_hex(32)


@bottle.get('/')
def naslovna_stran():

    bottle.response.delete_cookie('id', path='/')
    bottle.response.delete_cookie('UpIme', path='/')
    bottle.response.delete_cookie('naziv', path='/')
    return bottle.template('osnova.html', napaka=None)


@bottle.route('/prijava', method=['GET', 'POST'])
def prijava():
    if bottle.request.method == 'POST':
        try:
            ime = bottle.request.forms.get('uporabnisko_ime')
            geslo1 = bottle.request.forms.get('geslo')
            

            (geslo2,id,agent,naziv)= Agenti.geslo(ime)

            bottle.response.set_cookie("naziv",str(naziv),secret=secret_key,path='/')
            bottle.response.set_cookie("id",str(id),secret=secret_key,path='/')
            bottle.response.set_cookie("UpIme",str(agent),secret=secret_key,path='/')
                      
            if geslo1==geslo2:
                if naziv==1:
                    klienti = Agenti.klienti_agenta(int(id))
                    return bottle.template('agent.html', klienti=klienti,ime_agent=agent,uporabnik_id=int(naziv))
                    
                elif naziv==0:
                    return bottle.template('boss.html', ime_agent=agent,uporabnik_id=int(naziv))

               
            else:
                return bottle.template('prijava.html', napaka="Napačno uporabniško ime ali geslo.")
            
        except Exception as e:
            # Handle exceptions gracefully
            #print(f"NAPAKA: {e}")
            return bottle.template('prijava.html', napaka="Napačno uporabniško ime ali geslo.")
  
    else:
                        
        return bottle.template('prijava.html', napaka=None)

@bottle.route('/domov')
def domov():
    agent=bottle.request.get_cookie("UpIme",secret=secret_key)
    naziv=int(bottle.request.get_cookie("naziv",secret=secret_key))
    id=int(bottle.request.get_cookie("naziv",secret=secret_key))
    if naziv==1:
        klienti = Agenti.klienti_agenta(int(id))
        return bottle.template('agent.html', klienti=klienti,ime_agent=agent,uporabnik_id=int(naziv))
        
    elif naziv==0:
        return bottle.template('boss.html', ime_agent=agent,uporabnik_id=int(naziv))
@bottle.route('/agent', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')

    if selected_action == 'nepremicnine':
        bottle.redirect('/nepremicnine')
    elif selected_action == 'klienti':
        bottle.redirect('/klienti')
    else:
        return "Invalid action selected"

@bottle.route('/klienti')
def klienti():
    return bottle.template('klienti.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    #print(bottle.request.get_cookie("UpIme",secret=secret_key))
    if selected_action == 'nepremicnine':
        bottle.redirect('/nepremicnine')
    elif selected_action == 'agenti':
        bottle.redirect('/agenti')
    elif selected_action == 'klienti_boss':
        bottle.redirect('/klienti_boss')
    else:
        return "Invalid action selected"

@bottle.route('/klienti_boss')
def klienti_boss():
    return bottle.template('klienti_boss.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/agenti')
def agenti():
    return bottle.template('agenti.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/agenti', method='POST')
def agenti():
    selected_action = bottle.request.forms.get('actions')
    #print(bottle.request.get_cookie("UpIme",secret=secret_key))
    if selected_action == 'dodaj-agenta':
        bottle.redirect('/dodaj-agenta')
    elif selected_action == 'klienti-agenta':
        bottle.redirect('/klienti_agenta_izbor')
    elif selected_action == 'vsi-agenti':
        bottle.redirect('/vsi_agenti')
    else:
        return "Napačna izbira"

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
        return "Napačna izbira"
    
@bottle.route('/klienti', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-klienta':
        bottle.redirect('/dodaj-klienta')
    elif selected_action == 'nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-klienta-agent')
    else:
        return "Napačna izbira"
    
@bottle.route('/klienti_boss', method='POST')
def agent():
    selected_action = bottle.request.forms.get('actions')
    if selected_action == 'dodaj-klienta':
        bottle.redirect('/dodaj-klienta')
    elif selected_action == 'vsi-klienti':
        bottle.redirect('/vsi-klienti')
    elif selected_action == 'agenti-klienta':
        bottle.redirect('/select-klienta')
    elif selected_action == 'Nepremicnine-ki-ustrezajo':
        bottle.redirect('/select-klienta-boss')
    else:
        return "Napačna izbira"

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
        return "Napačna izbira"

######################################################################################gor meniji

@bottle.route('/dodaj-klienta')
def dodaj_klienta():
    return bottle.template('dodaj_klienta.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),napaka=None,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/pregled-nepremicnine')
def pregled_nepremicnine():
    lokacije = Nepremicnine.vse_lokacije()
    return bottle.template('pregled_nepremicnin.html', lokacije=lokacije,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/pregled-kliente')
def pregled_kliente():
    return bottle.template('pregled_kliente.html')

@bottle.route('/dodaj-nepremicnino', method=['GET', 'POST'])
def dodaj_nepremicnino():
    if bottle.request.method == 'POST':
        # Handle the form submission
        lastnik = bottle.request.forms.get('lastnik')
        cena = bottle.request.forms.get('cena')
        vrsta = bottle.request.forms.get('vrsta')
        lokacija = bottle.request.forms.get('lokacija')

        if not lastnik or not cena or not vrsta or not lokacija:
            return bottle.template('dodaj_nepremicnino.html', napaka="Izpolni vsa obmocja",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))
        
        try:
            cena = int(cena)
        except ValueError:
            return bottle.template('dodaj_nepremicnino.html', napaka="Vnesi veljavno ceno.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

     
        Nepremicnine.dodaj_nepremicnino(lastnik,cena,vrsta,lokacija)
       

        return bottle.redirect("/nepremicnine")
    else:
        # Display the form for adding a new property
        return bottle.template('dodaj_nepremicnino.html', napaka=None, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/dodaj-agenta', method=['GET', 'POST'])
def dodaj_agenta():
    if bottle.request.method == 'POST':
        ime = bottle.request.forms.get('ime')
        kontakt = bottle.request.forms.get('kontakt')
        geslo = bottle.request.forms.get('geslo')
        naziv = bottle.request.forms.get('naziv')

        if not ime or not kontakt or not geslo or not naziv:
            return bottle.template('dodaj_agenta.html', napaka="Vsa polja so obvezna.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))
        
        Agenti.dodaj_agenta(ime, kontakt, geslo, naziv)

        return bottle.redirect('/agenti') 
    else:
        return bottle.template('dodaj_agenta.html', napaka=None,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))


@bottle.route('/dodaj-klienta', method=['GET', 'POST'])
def dodaj_klienta():
    if bottle.request.method == 'POST':
        ime = bottle.request.forms.get('ime')
        kontakt = bottle.request.forms.get('kontakt')
        budget = bottle.request.forms.get('budget')
        lokacija = bottle.request.forms.get('lokacija')
        vrsta = bottle.request.forms.get('vrsta')

        if not ime or not kontakt or not budget or not lokacija or vrsta not in ['stanovanje', 'hisa', 'zemljisce']:
            return bottle.template('dodaj_klienta.html', napaka="Vsa polja so obvezna in vrsta mora biti stanovanje, hisa ali zemljisce.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

        try:
            budget = int(budget)
        except ValueError:
            return bottle.template('dodaj_klienta.html', napaka="Budget mora biti številčna vrednost.",uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

       
        Klienti.dodaj_klienta(ime, kontakt, budget, lokacija, vrsta)
        id_klient=int(Klienti.id_klienti(kontakt))
        id_agent=int(bottle.request.get_cookie("id",secret=secret_key))
        Zastopa.agent_klient(id_klient, id_agent)
        Interes.dodaj_interes(id_klient)
        
        return bottle.redirect('/klienti') 
    else:
        return bottle.template('dodaj_klienta.html', napaka=None,uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)),ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

#########################################################gor je dodajanje

#agenti klienta
@bottle.route('/agenti-klienta/<id_klient:int>')
def agenti_klienta(id_klient):
    agenti = Klienti.agenti(id_klient)
    
    return bottle.template('agenti_klienta.html', id_klient=id_klient, agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/select-klienta')
def select_klienta():
    
    buyers = Klienti.klienti()  
    return bottle.template('agenti_klienta_izbor.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klienta', method='POST')
def handle_select_klienta():
    id_klienta = bottle.request.forms.get('id_klienta')
    if id_klienta:
        return bottle.redirect(f'/agenti-klienta/{id_klienta}')
    else:
        return "Noben kupec izbran.", 400
    
#nepremicnine ki lahko zanimajo klienta za agente
@bottle.route('/select-klienta-agent')
def select_klienta():
    
    buyers = Klienti.klienti_agenta(int(bottle.request.get_cookie("id",secret=secret_key)))  
    return bottle.template('klienta_izbor_agent.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klienta_agent', method='POST')
def handle_select_klienta():
    id_klienta = bottle.request.forms.get('id_klienta')
    if id_klienta:
        return bottle.redirect(f'/neprem-klienta_agent/{id_klienta}')
    else:
        return "Noben kupec izbran.", 400
    
@bottle.route('/neprem-klienta_agent/<id_klient:int>')
def agenti_klienta(id_klient):
    nepremicnine = Klienti.nepremicnine(id_klient)
    
    return bottle.template('nepremicnine_klienta_agent.html', id_klient=id_klient, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#nepremicnine ki lahko zanimajo klienta za boss
@bottle.route('/select-klienta-boss')
def select_klienta():
    
    buyers = Klienti.klienti()
    return bottle.template('klienta_izbor_boss.html', buyers=buyers,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_klienta_boss', method='POST')
def handle_select_klienta():
    id_klienta = bottle.request.forms.get('id_klienta')
    if id_klienta:
        return bottle.redirect(f'/neprem-klienta_agent/{id_klienta}')
    else:
        return "Noben kupec izbran.", 400
    
@bottle.route('/neprem-klienta_boss/<id_klient:int>')
def agenti_klienta(id_klient):
    nepremicnine = Klienti.nepremicnine(id_klient)
    
    return bottle.template('nepremicnine_klienta_agent.html', id_klient=id_klient, nepremicnine=nepremicnine,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#klienti agenta
@bottle.route('/klienti_agenta_izbor')
def select_agent():
    
    agenti = Agenti.agenti()
    return bottle.template('izbor_agent.html', agenti=agenti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

@bottle.route('/izbor_agenta', method='POST')
def handle_select_agent():
    id_agenta = bottle.request.forms.get('id_agenta')
    if id_agenta:
        return bottle.redirect(f'/klienti_agenta/{id_agenta}')
    else:
        return "Noben kupec izbran.", 400
    
@bottle.route('/klienti_agenta/<id_agenta:int>')
def agenti_klienta(id_agenta):
    klienti = Agenti.klienti_agenta(int(id_agenta))
    
    return bottle.template('klienti_agenta.html', id_agenta=id_agenta, klienti=klienti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

#vsi klienti
@bottle.route('/vsi-klienti')
def vsi_klienti():
    klienti=Klienti.vsi_klienti()
    return bottle.template('vsi-klienti.html',klienti=klienti,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))

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
        return "Nobena lokacija izbrana.", 400
    
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
        return "Cena ni določena.", 400
    
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
        return "Vrsta ni izbrana", 400
    
@bottle.route('/neprem_vrste/<vrsta>')
def neprem_vrste(vrsta):
    nepremicnine = Nepremicnine.f_vrsta_nepremicnine(vrsta)
    return bottle.template('vse_nepremicnien.html', nepremicnine=nepremicnine, ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key),uporabnik_id=int(bottle.request.get_cookie("naziv",secret=secret_key)))




bottle.run(debug=True, reloader=True)