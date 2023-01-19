from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    bcpName = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))
    shortName = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    ibericonScore = db.Column(db.Float)
    factions = db.relationship('Faction', secondary="userfaction", back_populates='users')
    teams = db.relationship('Team', secondary="userteam", back_populates='users')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='users')


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    shortName = db.Column(db.String(50))
    ibericonScore = db.Column(db.Float)
    users = db.relationship('User', secondary="userteam", back_populates='teams')
    tournaments = db.relationship('Tournament', secondary='usertournament', back_populates='teams')


class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    shortName = db.Column(db.String(30))
    users = db.relationship('User', secondary="userfaction", back_populates='factions')
    tournaments = db.relationship('Tournament', secondary="usertournament", back_populates='factions')


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    bcpId = db.Column(db.String(30), nullable=False)
    bcpUri = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    shortName = db.Column(db.String(50))
    date = db.Column(db.String(50))
    isTeam = db.Column(db.Boolean)
    users = db.relationship('User', secondary="usertournament", back_populates='tournaments')
    teams = db.relationship('Team', secondary="usertournament", back_populates='tournaments')
    factions = db.relationship('Faction', secondary="usertournament", back_populates='tournaments')


class UserTournament(db.Model):
    __tablename__ = 'usertournament'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    factionId = db.Column(db.Integer, db.ForeignKey('faction.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    tournamentId = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    position = db.Column(db.Integer)
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
