from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200))
    shortName = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    ibericonScore = db.Column(db.Float)


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    shortname = db.Column(db.String(50))
    ibericonScore = db.Column(db.Float)


class Faction(db.Model, UserMixin):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    shortName = db.Column(db.String(30))


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shortname = db.Column(db.String(50))
    timestamp = db.Column(db.Integer)


class UserTournament(db.Model):
    __tablename__ = 'usertournament'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    tournamentId = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    bcpScore = db.Column(db.Float)
    ibericonScore = db.Column(db.Float)


class UserFaction(db.Model):
    __tablename__ = 'userfaction'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    ibericonScore = db.Column(db.Float)


class UserTeam(db.Model):
    __tablename__ = 'userteam'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    ibericonScore = db.Column(db.Float)




