from database import Team


def getTeam(te):
    return Team.query.filter_by(id=te).first()


def addTeam(te):
    pass
