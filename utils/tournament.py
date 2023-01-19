import requests
import json
import datetime

from flask import current_app

from database import Tournament, UserTournament, UserTeam, UserFaction
from utils.user import addUser
from utils.faction import addFaction
from utils.team import addTeam


def getTournament(to):
    return Tournament.query.filter_by(id=to).first()


def getAllTournaments():
    return Tournament.query.all()


def addNewTournament(db, form):
    if "https://www.bestcoastpairings.com/event/" in form['bcpLink']:
        eventId = form["bcpLink"].split("/")[-1].split("?")[0]
        uri = current_app.config["BCP_API"].replace("####event####", eventId)
        response = requests.get(uri)
        info = json.loads(response.text)
        info = info['data']
        if Tournament.query.filter_by(bcpId=info[0]['eventId']).first():
            return 400
        isTeamTournament = False  # TODO saber si es torneo de equipos o no
        db.session.add(Tournament(
            bcpId=info[0]['eventId'],
            bcpUri=form['bcpLink'],
            name=info[0]['event']['name'],
            shortName=info[0]['event']['name'].replace(" ", "").lower(),
            isTeam=isTeamTournament,
            date=info[0]['eventDate'].split("T")[0]
        ))
        db.session.commit()
        tor = Tournament.query.filter_by(bcpId=info[0]['eventId']).first()
        for user in info:
            usr = addUser(db, user)
            fct = addFaction(db, user)
            te = addTeam(db, user)

            tor.users.append(usr)
            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = user['placing']
            usrTor.bcpScore = user['ITCPoints']
            # TODO calcular ibericon score de este user para este torneo
            usrTor.ibericonScore = 0

            if fct:
                if fct not in usr.factions:
                    usr.factions.append(fct)
                usrTor.factionId = fct.id
                usrFct = UserFaction.query.filter_by(userId=usr.id).filter_by(factionId=fct.id).first()
                # TODO calcular y actualizar Ibericon Score de facción de este user
                usrFct.ibericonScore = 0
            if te:
                if te not in usr.teams:
                    usr.teams.append(te)
                usrTor.teamId = te.id
                usrTe = UserTeam.query.filter_by(userId=usr.id).filter_by(teamId=te.id).first()
                # TODO calcular y actualizar Ibericon Score de equipo para este torneo
                usrTe.ibericonScore = 0
                # TODO Update global team score
                te.ibericonScore = 0

            # TODO calcular global ibericon score ya sea para jugador o para equipo
            globalIbericonScore = 0
            usr.ibericonScore = globalIbericonScore
            db.session.commit()
        return 200
    return 400
