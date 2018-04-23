from flask import Blueprint

sd_admin = Blueprint('sd_admin', __name__)

from . import views