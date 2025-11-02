from turtle import title
from flask import Blueprint, render_template
import os

template_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'templates', 'main')
)

bp_main = Blueprint('main', __name__, template_folder=template_dir)

@bp_main.route('/')
def index():
    return render_template('index.html', title='Início')