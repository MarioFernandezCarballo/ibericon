from flask import Blueprint, render_template
from flask_login import current_user

from utils.user import getUsers
from utils.tournament import getTournamentsByUser

userBP = Blueprint('userBluePrint', __name__)


@userBP.route("/users", methods={"GET", "POST"})
def usersEndPoint():
    usr = getUsers()
    return render_template(
        'users.html',
        title="Jugadores",
        users=usr,
        user=current_user if not current_user.is_anonymous else None
    )


@userBP.route("/user/<us>", methods={"GET", "POST"})
def userEndPoint(us):
    trn = getTournamentsByUser(us)
    return render_template(
        'user.html',
        title=trn[0].userId.name,
        usr=trn[0].userId,
        tournaments=trn,
        user=current_user if not current_user.is_anonymous else None
    )
