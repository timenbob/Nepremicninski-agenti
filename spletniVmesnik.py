import bottle
from model2 import Agenti, Kupci, Nepremicnine, Zastopa, Interes


@bottle.route('/prijava/', method=['GET', 'POST'])
def prijava():
    ime = bottle.request.forms.get('ime')
    geslo1 = bottle.request.forms.get('geslo')
    geslo2=Agenti.geslo(ime)

    if ime == 'admin' and geslo1 == 'admin':
        bottle.redirect('/izpolnitev/')
    else:
        return bottle.template('prijava.html')



bottle.run(debug=True, reloader=True)