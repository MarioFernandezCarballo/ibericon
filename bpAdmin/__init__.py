from flask import Blueprint, redirect, url_for, current_app, request, flash
from flask_login import login_required

from utils.user import setPlayerPermission, getUser
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import addNewTournament

adminBP = Blueprint('adminBluePrint', __name__)


@adminBP.route("/player/<pl>/permission", methods={"GET", "POST"})
@login_required
@only_left_hand
def changePlayerPermissions(pl):
    if setPlayerPermission(current_app.config["database"], pl, request.form):
        flash("OK")
    else:
        flash("No OK")
    pl = getUser(pl)
    return redirect(url_for('userBluePrint.user', pl=pl['sql'].id))


@adminBP.route("/add/tournament", methods={"POST"})
@login_required
@only_collaborator
def randomize():
    if request.method == 'POST':
        newTournament = addNewTournament(current_app.config['database'], request.form)
        return redirect(url_for('genericBluePrint.general'))
