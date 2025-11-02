from flask import Flask


class MyApp():
    def __init__(self):
        self.app = Flask(__name__, template_folder='views/templates')
        self.register_blueprint()

    def register_blueprint(self):
        from app.controllers.main.routes import bp_main

        self.app.register_blueprint(bp_main, url_prefix='/')
    
    def run(self):
        self.app.run(debug=True)