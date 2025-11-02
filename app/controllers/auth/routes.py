# from flask import Blueprint, render_template
# import os

# template_dir = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'templates', 'auth')
# )

# bp_auth = Blueprint('auth', __name__, template_folder=template_dir)

# @bp_auth.route('/login')
# def login():
#     return render_template('login.html', title='Login')

# @bp_auth.route('/register')
# def register():
#     return render_template('register.html', title='Registro')