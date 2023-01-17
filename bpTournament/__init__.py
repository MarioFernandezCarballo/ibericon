from flask import Blueprint, redirect, url_for, current_app, request, flash

from utils.user import setPlayerPermission, getUser
from utils.decorators import only_left_hand, only_collaborator
from utils.tournament import addNewTournament

tournamentBP = Blueprint('tournamentBluePrint', __name__)