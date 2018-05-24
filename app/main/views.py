from flask import render_template, redirect, url_for
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('hello.html')


@main.route('/run', methods=['GET', 'POST'])
def run():
    name = 'Admin'
    return render_template('testbootstrap2.html',name=name)

@main.route('/run_extends')
def run_extends():
    return render_template('base_frame.html')

