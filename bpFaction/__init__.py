from flask import Blueprint, render_template
from flask_login import current_user

from utils.faction import getFaction
from utils.user import getUserByFaction
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import addNewTournament

factionBP = Blueprint('factionBluePrint', __name__)


@factionBP.route("/faction/<fact>", methods={"GET", "POST"})
def factionEndPoint(fact):
    fct = getFaction(fact)
    fctUsr = getUserByFaction(fact)
    return render_template(
        'faction.html',
        title=fct.name,
        user=current_user if not current_user.is_anonymous else None,
        faction=fct,
        users=fctUsr
    )


@factionBP.route("/factions", methods={"GET", "POST"})
def factionsEndPoint():
    pass
