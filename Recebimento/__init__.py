from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='./static')

# Load environment variables from .env file
load_dotenv()

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG_MODE') == 'True'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Import models and routes after initializing extensions to avoid circular imports
from Recebimento.models import Responsavel
from Recebimento import routes

# Configure Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return Responsavel.query.get(int(user_id))