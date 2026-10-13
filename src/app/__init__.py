from flask import Flask
from app.database.db_handler import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'agro_ai_secret_key_12345'

    init_db()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
