from flask import Flask
import secrets

class MyApp():
    def __init__(self):
        self.app = Flask(__name__, template_folder='views/templates')
        self.register_blueprint()
        self.app.config['SECRET_KEY'] = secrets.token_hex(16)

    def register_blueprint(self):
        from app.controllers.main import main_bp
        from app.controllers.auth import auth_bp

        self.app.register_blueprint(main_bp, url_prefix='/')
        self.app.register_blueprint(auth_bp, url_prefix='/auth')
    
    def run(self):
        self.app.run(debug=True)