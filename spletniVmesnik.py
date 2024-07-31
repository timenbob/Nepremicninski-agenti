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
                    return bottle.template('agent.html', ime_agent=agent)
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
        bottle.redirect('/klijenti_agenta')
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
        bottle.redirect('/nepremicnine-ki-ustrezajo')
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
        bottle.redirect('/agenti-kupca')
    elif selected_action == 'nepremicnine-ki-ustrezajo':
        bottle.redirect('/nepremicnine-ki-ustrezajo')
    else:
        return "Invalid action selected"

@bottle.route('/brskaj_nepremicnine')
def brskaj_nepremicnine():
    return bottle.template('brskaj_nepremicnine.html',ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))

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

        # Process the data
        nepremicnina = Nepremicnine(lastnik=lastnik, cena=cena, vrsta=vrsta, lokacija=lokacija, id=None)

        # Save the nepremicnina object to your database or data structure here

        # Redirect to the home page or another page after successfully adding the property
        return bottle.redirect('/')
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
        
        # Process the data (e.g., store the agent information)
        agent = Agent(ime=ime, kontakt=kontakt, geslo=geslo, naziv=naziv)
        
        # Save the agent (implement your own saving logic, like to a database)
        save_agent(agent)
        
        # Redirect or show success message
        return bottle.redirect('/agents')  # Redirect to a list of agents or another page
    else:
        return bottle.template('dodaj_agenta.html', napaka=None,ime_agent=bottle.request.get_cookie("UpIme",secret=secret_key))


@bottle.route('/handle-dodaj-stranko', method='POST')
def handle_dodaj_stranko():
    ime = bottle.request.forms.get('ime')
    kontakt = bottle.request.forms.get('kontakt')

    kupci = Kupci(ime=ime, kontakt=kontakt, buget=0, lokacija="", vrsta="", id=None)

    return bottle.redirect('/')


bottle.run(debug=True, reloader=True)
