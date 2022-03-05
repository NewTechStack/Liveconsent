from Model.liveconsent import *

def setuproute(app, call):
    @app.route('/',                             ['OPTIONS', 'GET'],         lambda x = None: call([origin_check])) #done
    @app.route('/sign',                         ['OPTIONS', 'POST'],        lambda x = None: call([liveconsent_signature_request])) #done
    def base():
        return
