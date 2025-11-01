from flask import Flask, render_template

class MyApp(Flask):
    def __init__(self):
        self.app = Flask(__name__, template_folder='views/templates')
    
    def run(self):
        self.app.run(debug=True)