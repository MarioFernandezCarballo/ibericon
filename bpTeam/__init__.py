from flask import Blueprint, render_template
from flask_login import current_user

from utils.team import getTeams
from utils.tournament import getTournamentsByTeam


teamBP = Blueprint('teamBluePrint', __name__)


@teamBP.route("/teams", methods={"GET", "POST"})
def teamsEndPoint():
    tms = getTeams()
    return render_template(
        'teams.html',
        title="Equipos",
        teams=tms,
        user=current_user if not current_user.is_anonymous else None
    )


@teamBP.route("/team/<te>", methods={"GET", "POST"})
def teamEndPoint(te):
    trn = getTournamentsByTeam(te)
    return render_template(
        'team.html',
        title=trn[0].teamId.name,
        team=trn[0].teamId,
        tournaments=trn,
        user=current_user if not current_user.is_anonymous else None
    )
