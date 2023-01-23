from flask import Blueprint, redirect, url_for, current_app, request, flash, render_template
from flask_login import login_required, current_user

from utils.user import setPlayerPermission, getUser
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import addNewTournament

adminBP = Blueprint('adminBluePrint', __name__)


@adminBP.route("/player/<pl>/permission", methods={"GET", "POST"})
@login_required
@only_left_hand
def changePlayerPermissionsEndPoint(pl):
    if setPlayerPermission(current_app.config["database"], pl, request.form):
        flash("OK")
    else:
        flash("No OK")
    return redirect(url_for('userBluePrint.userEndPoint', pl=pl))


@adminBP.route("/add/tournament", methods={"GET", "POST"})
@login_required
@only_collaborator
def addNewTournamentEndPoint():
    if request.method == 'POST':
        addNewTournament(current_app.config['database'], request.form)
        return redirect(url_for('genericBluePrint.generalEndPoint'))
    return render_template(
        'add.html',
        title="Añadir Torneo",
        user=current_user if not current_user.is_anonymous else None
    )
