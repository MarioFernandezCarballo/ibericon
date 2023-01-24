from flask import current_app
from sqlalchemy import desc

from database import Team, Tournament, UserTournament


def getTeam(te):
    return current_app.config["database"].session.query(UserTournament, Tournament, Team
                                                        ).filter(UserTournament.teamId == te
                                                                 ).join(Tournament,
                                                                        Tournament.id == UserTournament.tournamentId
                                                                        ).join(Team,
                                                                               Team.id == UserTournament.teamId).all()


def getTeamOnly(te):
    return Team.query.filter_by(id=te).first()


def getTeams(qty=0):
    if qty > 0:
        result = Team.query.order_by(desc(Team.ibericonScore)).all()
        return result[0:qty-1]
    else:
        return Team.query.order_by(desc(Team.ibericonScore)).all()


def addTeam(db, te):
    if te['team']:
        if not Team.query.filter_by(bcpId=te['teamId']).first():
            db.session.add(Team(
                bcpId=te['teamId'],
                name=te['team']['name'].strip(),
                shortName=te['team']['name'].replace(" ", "").lower()
            ))
    db.session.commit()
    return Team.query.filter_by(bcpId=te['teamId']).first() if te['team'] else None
