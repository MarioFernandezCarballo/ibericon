from database import Faction


def getFaction(fct):
    return Faction.query.filter_by(id=fct).first()


def addFaction(fct):
    pass
