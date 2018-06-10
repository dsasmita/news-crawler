from flask import render_template, Blueprint

module_home = Blueprint('module_home', __name__, template_folder='templates')


@module_home.route('/')
def index():
    return 'home index'
