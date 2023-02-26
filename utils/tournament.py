import requests
import json

from flask import current_app
from geopy.geocoders import Nominatim

from database import Tournament, UserTournament
from utils.user import addUser
from utils.faction import addFaction
from utils.club import addClub


def getTournament(to):
    return Tournament.query.filter_by(id=to).first()


def getAllTournaments():
    return Tournament.query.all()


def addNewTournament(db, form):
    if "https://www.bestcoastpairings.com/event/" in form['bcpLink']:
        eventId = form["bcpLink"].split("/")[-1].split("?")[0]
        uri = current_app.config["BCP_API_EVENT"].replace("####event####", eventId)
        response = requests.get(uri)
        info = json.loads(response.text)
        if not info['ended']:
            return 400, None
        if Tournament.query.filter_by(bcpId=eventId).first():
            return 400, None
        isTeamTournament = info['teamEvent']
        geoLocator = Nominatim(user_agent="geoapiExercises")
        location = geoLocator.reverse(str(info['coordinate'][1])+","+str(info['coordinate'][0]))
        try:
            city = location.raw['address']['state_district']
        except KeyError:
            city = location.raw['address']['city']
        db.session.add(Tournament(
            bcpId=info['id'],
            bcpUri="https://www.bestcoastpairings.com/event/" + info['id'],
            name=info['name'].strip(),
            shortName=info['name'].replace(" ", "").lower(),
            city=city,
            isTeam=isTeamTournament,
            date=info['eventDate'].split("T")[0],
            totalPlayers=info['totalPlayers'],
            rounds=info['numberOfRounds']
        ))
        db.session.commit()
        tor = Tournament.query.filter_by(bcpId=info['id']).first()
        if tor.isTeam:
            uri = current_app.config["BCP_API_TEAM"].replace("####event####", tor.bcpId)
            response = requests.get(uri)
            info = json.loads(response.text)
        else:
            uri = current_app.config["BCP_API_USERS"].replace("####event####", tor.bcpId)
            response = requests.get(uri)
            info = json.loads(response.text)

        for user in info['data']:
            usr = addUser(db, user)
            fct = addFaction(db, user)
            cl = addClub(db, user)
            tor.users.append(usr)
            usrTor = UserTournament.query.filter_by(userId=usr.id).filter_by(tournamentId=tor.id).first()
            usrTor.position = user['placing']

            # Algoritmo mágico warp
            # OPCION 1
            # performance = [0, 0, 0]
            # for game in user['total_games']:
            #     performance[game['gameResult']] += 1
            # score = ((performance[2]*3) + performance[1]) * (1 + (tor.totalPlayers / 100))
            # usrTor.ibericonScore = (score*10)/tor.rounds

            # OPCION 2
            # performance = [0, 0, 0]
            # for game in user['total_games']:
            #     performance[game['gameResult']] += 1
            # playerModifier = 1 + tor.totalPlayers/100
            # roundModifier = (tor.rounds/(tor.rounds+2)) - ((tor.rounds-len(user['total_games']))/30)
            # performanceModifier = ((performance[2] * 3) + performance[1])
            # usrTor.ibericonScore = playerModifier * roundModifier * performanceModifier

            # OPCION 3
            # performance = [0, 0, 0]
            # victoryMod = 1
            # for game in user['total_games']:
            #     if game['gameResult'] > 1:
            #         victoryMod += .05
            #     elif game['gameResult'] < 1:
            #         victoryMod -= .05
            #     if game['gameResult'] == 2:
            #         performance[game['gameResult']] += 1 * victoryMod
            #     else:
            #         performance[game['gameResult']] += 1
            # playerModifier = 1 + tor.totalPlayers / 100
            # roundModifier = (tor.rounds / (tor.rounds + 2)) - ((tor.rounds-len(user['total_games']))/30)
            # performanceModifier = (len(user['total_games'])) + ((performance[2] * 3) + performance[1] - (performance[1] * .3))
            # usrTor.ibericonScore = playerModifier * performanceModifier * roundModifier

            # OPCION 4
            performance = [0, 0, 0]
            maxPoints = len(user['games']) * 3
            maxIbericon = 3
            playerModifier = 1 + tor.totalPlayers / 100
            for game in user['games']:
                performance[game['gameResult']] += 1
            points = ((performance[2] * 3) + performance[1])
            finalPoints = points * maxIbericon / maxPoints
            usrTor.ibericonScore = finalPoints * playerModifier

            if fct:
                if fct not in usr.factions:
                    usr.factions.append(fct)
                usrTor.factionId = fct.id
            if cl:
                if cl not in usr.clubs:
                    usr.clubs.append(cl)
                usrTor.clubId = cl.id
            db.session.commit()
        return 200, tor
    return 400, None


def deleteTournament(db, to):
    UserTournament.query.filter_by(tournamentId=to).delete()
    db.session.delete(Tournament.query.filter_by(id=to).first())
    db.session.commit()
    return 200
