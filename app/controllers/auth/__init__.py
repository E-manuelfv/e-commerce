from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.supabase_client import supabase 
from functools import wraps

# Decorador para verificar autenticação
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Blueprint de autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# --- Rota de Registro ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        
        # Validação de senhas
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/register.html', email=email)
        
        if not supabase:
            flash('Erro de configuração do Supabase.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            # Registro no Supabase
            res = supabase.auth.sign_up({
                "email": email, 
                "password": password
            })
            
            flash('Registro completo! Verifique seu Email.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(f'Erro no registro: {e}', 'danger')
            return render_template('auth/register.html', email=email)
    
    return render_template('auth/register.html')

# --- Rota de Login ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not supabase:
            flash('Erro de configuração do Supabase.', 'danger')
            return redirect(url_for('auth.login'))
        
        try:
            # Login no Supabase
            res = supabase.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            
            # Salva sessão do usuário
            session['user_id'] = res.user.id
            session['user_email'] = res.user.email
            session['access_token'] = res.session.access_token
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('shop.index'))
            
        except Exception as e:
            flash(f'Credenciais inválidas: {e}', 'danger')
            return render_template('auth/login.html', email=email)
            
    return render_template('auth/login.html')

# --- Rota de Logout ---
@auth_bp.route('/logout')
def logout():
    # Logout no Supabase
    if 'access_token' in session and supabase:
        try:
            supabase.auth.sign_out()
        except Exception as e:
            print(f"Erro ao fazer logout no Supabase: {e}")
    
    # Limpa sessão do Flask
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))