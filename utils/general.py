from sqlalchemy import desc

from database import User, UserTournament, UserFaction, UserClub, Club


def updateStats(db, tor):
    for usr in tor.users:
        best = UserTournament.query.filter_by(userId=usr.id).order_by(desc(UserTournament.ibericonScore)).all()
        usr.ibericonScore = sum([t.ibericonScore for t in best[:4]])
        for usrFct in UserFaction.query.filter_by(userId=usr.id).all():
            score = 0
            count = 0
            for t in best:
                if t.factionId == usrFct.factionId:
                    count += 1
                    score += t.ibericonScore
                if count == 3:
                    break
            usrFct.ibericonScore = score
        for usrCl in UserClub.query.filter_by(userId=usr.id).all():
            score = 0
            count = 0
            for t in best:
                if t.clubId == usrCl.clubId:
                    count += 1
                    score += t.ibericonScore
                if count == 3:
                    break
            usrCl.ibericonScore = score
    for cl in Club.query.all():
        best = UserClub.query.filter_by(clubId=cl.id).order_by(desc(UserClub.ibericonScore)).all()
        cl.ibericonScore = sum([t.ibericonScore for t in best[:10]])
    db.session.commit()
    return 200
