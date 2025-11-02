from flask import Flask
from flask_login import LoginManager
import secrets

class MyApp():
    def __init__(self):
        self.app = Flask(__name__, template_folder='views/templates')
        self.app.config['SECRET_KEY'] = secrets.token_hex(16)
        
        # Configuração do Flask-Login
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'auth.login'
        self.login_manager.login_message = 'Por favor, faça login para acessar esta página.'
        self.login_manager.login_message_category = 'warning'
        
        self.setup_login_manager()
        self.register_blueprint()

    def setup_login_manager(self):
        from app.models.user import User
        
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

    def register_blueprint(self):
        from app.controllers.main import main_bp
        from app.controllers.auth import auth_bp

        self.app.register_blueprint(main_bp, url_prefix='/')
        self.app.register_blueprint(auth_bp, url_prefix='/auth')
    
    def run(self):
        self.app.run(debug=True)