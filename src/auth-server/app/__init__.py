from flask import Flask
def create_app():
    app = Flask(__name__)
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    return app
