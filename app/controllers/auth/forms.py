from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.supabase_client import supabase

class RegistrationForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
        DataRequired(), 
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(), 
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    submit = SubmitField('Criar Conta')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')