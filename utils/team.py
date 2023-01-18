from database import Team


def getTeam(te):
    return Team.query.filter_by(id=te).first()


def getTeams(qty=0):
    if qty > 0:
        result = Team.query.all()
        return result[0:qty-1]
    else:
        return Team.query.all()


def addTeam(te):
    pass
