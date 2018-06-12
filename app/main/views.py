from flask import render_template, redirect, url_for
from . import main
from .. import db
from .services import SDProjectData as SD


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('hello.html')


@main.route('/run', methods=['GET', 'POST'])
def run():
    name = 'Admin'
    return render_template('hello.html',name=name)

@main.route('/run_extends')
def run_extends():
    result = SD().run_case_id(2,1)
    return result.text

