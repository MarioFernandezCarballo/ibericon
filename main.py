# Web page for Ibericon Kill Team circuit

from flask import Flask
from utils import createApp, createDatabase

from bpGeneric import genericBP
from bpAuth import authBP
from bpAdmin import adminBP


app = Flask(__name__)
app.register_blueprint(genericBP)
app.register_blueprint(authBP)
app.register_blueprint(adminBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])


# TODO WEB
#  - Crear roles
