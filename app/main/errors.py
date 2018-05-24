from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('http_status/404.html'), 404
