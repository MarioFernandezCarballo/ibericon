from flask import Flask
from utils import createApp, createDatabase

from bpGeneric import genericBP
from bpAuth import authBP
from bpAdmin import adminBP
from bpTeam import teamBP
from bpUser import userBP
from bpFaction import factionBP
from bpTournament import tournamentBP

app = Flask(__name__)
app.register_blueprint(genericBP)
app.register_blueprint(authBP)
app.register_blueprint(adminBP)
app.register_blueprint(teamBP)
app.register_blueprint(userBP)
app.register_blueprint(factionBP)
app.register_blueprint(tournamentBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])


# TODO WEB
#  - Puntuaciones:
#       1. Puntuación user con respecto a torneo
#       2. Puntuación equipo con respecto a torneo (¿¿solo de equipos??)
#       3. Puntuación user con respecto a facción
#       4. Puntuacion user con respecto a equipo (Torneo individual)
