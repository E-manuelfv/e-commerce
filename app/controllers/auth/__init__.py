from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models.supabase_client import supabase
from app.models.user import User
from .forms import RegistrationForm, LoginForm
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required_custom(f):
    """Decorator alternativo para views que não usam Flask-Login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Se já estiver logado, redireciona
    if current_user.is_authenticated:
        flash('Você já está logado!', 'info')
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        
        print(f"📝 Tentativa de registro: {email}")  # Debug
        
        # Validação adicional de senhas
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html', form=form)
        
        if not supabase:
            flash('Erro de configuração do banco de dados.', 'danger')
            return render_template('auth/register.html', form=form)

        try:
            # Registro no Supabase com dados adicionais
            response = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        "full_name": name
                    }
                }
            })
            
            print(f"✅ Resposta do Supabase: {response}")  # Debug
            
            if response.user:
                flash('Registro realizado com sucesso! Verifique seu email para confirmar a conta.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Erro no registro. Tente novamente.', 'danger')
                
        except Exception as e:
            print(f"❌ Erro detalhado: {e}")  # Debug
            
            # Tratamento de erros específicos do Supabase
            error_msg = str(e).lower()
            if 'user already registered' in error_msg:
                flash('Este email já está cadastrado.', 'danger')
            elif 'password should be at least' in error_msg:
                flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            else:
                flash(f'Erro no registro: {str(e)}', 'danger')
            
        return render_template('auth/register.html', form=form)
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona
    if current_user.is_authenticated:
        flash('Você já está logado!', 'info')
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        remember_me = form.remember_me.data
        
        print(f"🔐 Tentativa de login: {email}")  # Debug
        
        if not supabase:
            flash('Erro de configuração do banco de dados.', 'danger')
            return render_template('auth/login.html', form=form)
        
        try:
            # Login no Supabase
            response = supabase.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            
            print(f"✅ Resposta do login: {response.user.id if response.user else 'None'}")  # Debug
            
            if response.user:
                # Cria instância do usuário para Flask-Login
                user = User(
                    id=response.user.id,
                    email=response.user.email,
                    name=response.user.user_metadata.get('name', '')
                )
                
                # Login no Flask-Login
                login_user(user, remember=remember_me)
                
                # Também salva na session para compatibilidade
                session['user_id'] = response.user.id
                session['user_email'] = response.user.email
                session['user_name'] = response.user.user_metadata.get('name', '')
                session['access_token'] = response.session.access_token
                
                flash('Login realizado com sucesso!', 'success')
                
                # Redireciona para página solicitada ou index
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            else:
                flash('Erro no login. Tente novamente.', 'danger')
                
        except Exception as e:
            print(f"❌ Erro detalhado no login: {e}")  # Debug
            
            # Tratamento de erros específicos
            error_msg = str(e).lower()
            if 'invalid login credentials' in error_msg:
                flash('Email ou senha incorretos.', 'danger')
            elif 'email not confirmed' in error_msg:
                flash('Por favor, confirme seu email antes de fazer login.', 'warning')
            else:
                flash('Erro ao fazer login. Tente novamente.', 'danger')
            
        return render_template('auth/login.html', form=form)
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # Logout no Supabase
    if 'access_token' in session and supabase:
        try:
            supabase.auth.sign_out()
        except Exception as e:
            print(f"⚠️ Erro ao fazer logout no Supabase: {e}")
    
    # Logout no Flask-Login
    logout_user()
    
    # Limpa sessão do Flask
    session.clear()
    
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/test-supabase')
def test_supabase():
    """Rota para testar conexão com Supabase"""
    try:
        response = supabase.table('produtos').select('*').limit(1).execute()
        return f"✅ Conexão OK! Resposta: {response.data}"
    except Exception as e:
        return f"❌ Erro na conexão: {e}"