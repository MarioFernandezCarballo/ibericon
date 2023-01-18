import requests
import json

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
            if User.query.filter_by(name=form['username']).first():
                return 402, None
            if "https://www.bestcoastpairings.com/user/" in form['bcpLink']:
                bcpId = form["bcpLink"].split("/")[-1]

                # TODO hacer llamada a bcp para saber si existe
                #  si todo esta bien, guardar user o actualizar si ya existe en nuestra bd
                data = requests.get()

                user = json.loads(data.text)
                if not user:
                    return 402, None
                usr = User.query.filter_by(bcpId=bcpId).first()
                if usr:
                    usr.name = form['username']
                    usr.shortName = form['username'].lower().replace(" ", "")
                    usr.password = hashed_password
                    database.session.commit()
                    return 200, usr
                else:
                    new_user = User(
                        bcpId=bcpId,
                        name=form['username'],
                        password=hashed_password,
                        bcpName=user['user']['firstName'] + " " + user['user']['lastName'],
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
        user = User.query.filter_by(name=form['username']).first()
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


def getUsers(qty=0):
    if qty > 0:
        result = User.query.all()
        return result[0:qty-1]
    else:
        return User.query.all()

