import requests
import json
import datetime

from flask import current_app

from database import Tournament, UserTournament, User, Faction, Team, TeamTournament, UserTeam, UserFaction


def getTournament(to):
    return Tournament.query.filter_by(id=to).first()


def getTournamentsByUser(us):
    usrTor = UserTournament.query.filter_by(userId=us).all()
    for ut in usrTor:
        ut.tournamentId = Tournament.query.filter_by(id=ut.tournamentId).first()
        ut.factionId = Faction.query.filter_by(id=ut.factionId).first()
        ut.teamId = Team.query.filter_by(id=ut.teamId).first()
        ut.userId = User.query.filter_by(id=ut.userId).first()
    return usrTor


def getTournamentsByTeam(te):
    teTor = UserTournament.query.filter_by(userId=te).all()
    for ut in teTor:
        ut.tournamentId = Tournament.query.filter_by(id=ut.tournamentId).first()
        ut.teamId = Team.query.filter_by(id=ut.teamId).first()
        ut.userId = User.query.filter_by(id=ut.userId).first()
    return teTor


def addNewTournament(database, form):
    if "https://www.bestcoastpairings.com/event/" in form['bcpLink']:
        eventId = form["bcpLink"].split("/")[-1]
        uri = current_app.config["BCP_API"].replace("####event####", eventId)
        response = requests.get(uri)
        info = json.loads(response.text)
        if Tournament.query.filter_by(bcpId=info[0]['eventId']).first():
            return 400
        database.session.add(Tournament(
            bcpId=info[0]['eventId'],
            bcpUri=form['bcpLink'],
            name=info[0]['event']['name'],
            shortName=info[0]['event']['name'].replace(" ", "").lower(),
            timestamp=datetime.datetime(int(info[0]['eventDate'].split("T")[0].split("-")[0]),
                                        int(info[0]['eventDate'].split("T")[0].split("-")[1]),
                                        int(info[0]['eventDate'].split("T")[0].split("-")[2])).timestamp()

        ))
        database.session.commit()
        tor = Tournament.query.filter_by(bcpId=info[0]['eventId']).first()
        for user in info:
            if not User.query.filter_by(bcpId=user['userId']).first():
                database.session.add(User(
                    bcpId=user['userId'],
                    bcpName=user['user']['firstName'] + " " + user['user']['lastName'],
                    permissions=0
                ))
            if user['army']:
                if not Faction.query.filter_by(bcpId=user['armyId']).first():
                    database.session.add(Faction(
                        bcpId=user['armyId'],
                        name=user['army']['name'],
                        shortName=user['army']['name'].replace(" ", "").lower()
                    ))
            if user['team']:
                if Team.query.filter_by(bcpId=user['teamId']).first():
                    database.session.add(Team(
                        bcpId=user['teamId'],
                        name=user['team']['name'],
                        shortName=user['team']['name'].replace(" ", "").lower()
                    ))
            database.session.commit()
            usr = User.query.filter_by(bcpId=user['userId']).first()
            fct = Faction.query.filter_by(bcpId=user['armyId']).first() if user['army'] else None
            te = Team.query.filter_by(bcpId=user['teamId']).first() if user['team'] else None
            ibericonScore = 0

            database.session.add(UserTournament(
                userId=usr.id,
                factionId=fct.id if fct else None,
                teamId=te.id if te else None,
                tournamentId=tor.id,
                position=user['placing'],
                bcpScore=user['ITCPoints'],
                ibericonScore=ibericonScore
            ))
            # TODO ver un ejemplo en BCP de torneo de equipos para ver que informaciones y resultados coger
            database.session.add(TeamTournament(
                userId=usr.id,
                teamId=te.id if te else None,
                tournamentId=tor.id,
                position=user['placing'],
                bcpScore=user['ITCPoints'],
                ibericonScore=ibericonScore
            ))
            # TODO calcular global ibericon score ya sea para jugador o para equipo
            globalIbericonScore = 0
            usr.ibericonScore = globalIbericonScore
            if fct:
                usrFct = UserFaction.query.filter_by(userId=usr.id).filter_by(factionId=fct.id).first()
                if not usrFct:
                    database.session.add(UserFaction(
                        userId=usr.id,
                        factionId=fct.id,
                        ibericonScore=0  # TODO add faction score
                    ))
                # TODO update faction score
            if te:
                usrTe = UserTeam.query.filter_by(userId=usr.id).filter_by(teamId=te.id).first()
                if not usrTe:
                    database.session.add(UserTeam(
                        userId=usr.id,
                        teamId=te.id,
                        ibericonScore=0  # TODO add team score
                    ))
                # TODO update team score
