from flask import render_template, redirect, url_for
from . import main
from .. import db
from .services import SDProjectData as SD


@main.route('/hello', methods=['GET', 'POST'])
def test_hello():
    return render_template('hello.html')


@main.route('/run', methods=['GET', 'POST'])
def run():
    name = 'Admin'
    return render_template('hello.html', name=name)


@main.route('/run_extends')
def run_extends():
    # result = SD().run_case_id(2,1)
    result = SD().assemble_body_parameter(2, 1, 1)
    return '<p>' + str(result[0]) + '</p>' + '<p>' + str(result[1]) + '</p>' + '<p>' + str(result[2]) + '</p>'


@main.route('/test_run_cases')
def test_run_cases():
    result = SD().run_case_with_parameters(2, 1, 1, 1)
    result_display = str(result)
    return result_display

@main.route('/compare_all')
def compare_all():
    result = SD().compare_all_results(2,1,2,1,1)
    return result

@main.route('/')
def url_for_all():
    url_list = []
    url_list.append(url_for('main.url_for_all', _external=True))
    url_list.insert(0, url_for('main.test_hello', _external=True))
    url_list.append(url_for('main.run_extends', _external=True))
    url_list.append(url_for('main.test_run_cases', _external=True))
    url_list.append(url_for('main.compare_all',_external=True))
    url_list.append(url_for('main.compare_test',_external=True))

    return render_template('main_templates/urls.html', url_list=url_list)

@main.route('/compare_test')
def compare_test():
    return render_template('main_templates/compare_cases.html')
