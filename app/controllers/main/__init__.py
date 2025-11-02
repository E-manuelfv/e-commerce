from flask import Blueprint, render_template, session, flash
from app.models.supabase_client import supabase 
from app.controllers.auth import login_required

# Blueprint da loja
main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/')
def index():
    products = []
    
    # Verifica configuração do Supabase
    if not supabase: 
        flash('Erro de configuração do Supabase.', 'danger')
        return render_template('main/index.html', products=products)

    try:
        # Busca produtos do banco
        response = supabase.table('produtos').select('*').execute()
        products = response.data
        
    except Exception as e: 
        flash(f'Erro ao carregar produtos: {e}', 'danger')
        print(f"Erro no Supabase: {e}")
        
    return render_template('main/index.html', products=products)

@main_bp.route('/profile')
@login_required
def profile():
    # Passa dados do usuário para o template
    user_data = {
        'id': session.get('user_id', 'N/A'),
        'email': session.get('user_email', 'N/A')
    }
    return render_template('main/profile.html', title='Meu Perfil', user=user_data)