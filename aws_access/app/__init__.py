from flask import Flask
def create_app():
    app = Flask(__name__)
    from app.home.routes import home_bp
    app.register_blueprint(home_bp , url_prefix='/home') 
    return app
