from flask import Blueprint, render_template
from flask_login import current_user

from utils.user import getUsers
from utils.team import getTeams


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def generalEndPoint():
    usr = getUsers()
    tms = getTeams()
    return render_template(
        'general.html',
        title="General",
        users=usr,
        teams=tms,
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def aboutEndPoint():
    return render_template(
        'about.html',
        title="About",
        user=current_user if not current_user.is_anonymous else None
    )
