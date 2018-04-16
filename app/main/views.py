from flask import render_template, redirect, url_for
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('hello.html')
