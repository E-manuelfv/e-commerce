# from flask import Blueprint, render_template
# import os

# template_dir = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'templates', 'main')
# )

# bp_main = Blueprint('main', __name__, template_folder=template_dir)

# @bp_main.route('/')
# def index():
#     return render_template('index.html', title='Início')

# @bp_main.route('/icons')
# def icons():
#     return render_template('icons.html', title='Teste de ícones')