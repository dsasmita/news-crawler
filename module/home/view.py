from flask import Blueprint, jsonify

module_home = Blueprint('module_home', __name__, template_folder='templates')


@module_home.route('/')
def index():
    data = {'page': 'crawler', 'title': 'home crawler'}
    return jsonify(data)