from flask import Blueprint

nag = Blueprint('nag', __name__)

from . import views
