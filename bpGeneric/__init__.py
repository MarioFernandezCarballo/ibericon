from flask import Blueprint, render_template
from flask_login import current_user


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def general():
    return render_template(
        'general.html',
        title="General",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/about", methods={"GET", "POST"})
def about():
    return render_template(
        'about.html',
        title="About",
        user=current_user if not current_user.is_anonymous else None
    )
