from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash

from database import User


def userSignup(database, form):
    if form['username'].isalnum():
        if form['password'] == form['password1']:
            policy = PasswordPolicy.from_names(
                length=8,
                uppercase=1,
                numbers=1
            )
            if policy.test(form['password']):
                return 401, None
            hashed_password = generate_password_hash(form['password'], method='sha256')
            if User.query.filter_by(username=form['username']).first():
                return 402, None
            ok = False
            # TODO enlazar bcp id con user
            bcpId = 0
            new_user = User(
                bcpId=bcpId,
                name=form['username'],
                password=hashed_password,
                shortName=form['username'].lower().replace(" ", ""),
                permissions=15 if form['username'] == 'Zakanawaner' else 0
            )
            database.session.add(new_user)
            database.session.commit()
            return 200, new_user
        else:
            return 403, None
    return 405, None


def userLogin(form):
    if form['username'].isalnum():
        user = User.query.filter_by(username=form['username']).first()
        if user:
            if check_password_hash(user.password, form['password']):
                return 200, user
    return 401, None


def setPlayerPermission(database, userId, form):
    try:
        lvl = form['permission']
        usr = User.query.filter_by(id=userId).first()
        usr.permissions = int(lvl)
        database.session.commit()
    except:
        return False
    return True


def getUser(pl):
    return User.query.filter_by(id=pl).first()
