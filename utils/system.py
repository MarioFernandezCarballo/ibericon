import json
import secrets
import os

from database import db
from bpAuth import loginManager, jwt


def createApp(app):
    config = json.load(open("secret/config.json"))

    app.config["SECRET_KEY"] = handleSecretKey()
    app.config['PORT'] = config['port']
    app.config['HOST'] = config['host']

    app.config["JWT_SECRET_KEY"] = handleSecretKey()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = config['db-uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["BCP_API"] = config['api-base-uri']

    loginManager.init_app(app)
    app.config["loginManager"] = loginManager
    jwt.init_app(app)
    app.config["jwt"] = jwt
    db.init_app(app)
    app.config["database"] = db

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(app.config['database'])
            file = open('database.txt', 'w')
            file.write("Database Created")
            file.close()


def handleSecretKey():
    keys = json.load(open("secret/config.json"))
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/config.json", 'w'), indent=4)
        return key


def createTables(database):
    database.create_all()
    database.session.commit()
