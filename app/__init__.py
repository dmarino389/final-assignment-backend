from flask import Flask
from config import Config  # Import the Config class from config.py which contains configuration settings
from .models import db, User  # Import the database instance and the User model from the models module
from flask_migrate import Migrate  # Import Migrate for handling database migrations
from flask_login import LoginManager  # Import LoginManager for handling user sessions
from flask_moment import Moment  # Import Moment for formatting dates and times
from flask_cors import CORS  # Import CORS to handle Cross-Origin Resource Sharing

# Import Blueprints
from .social import social  # Import the 'social' Blueprint
from .shop import shop  # Import the 'shop' Blueprint
from .auth import auth  # Import the 'auth' Blueprint
from .api import api  # Import the 'api' Blueprint

app = Flask(__name__)  # Create an instance of the Flask class for our web app
app.config.from_object(Config)  # Load configuration settings from Config class

# Register Blueprints with the Flask application instance
app.register_blueprint(social)
app.register_blueprint(shop)
app.register_blueprint(auth)
app.register_blueprint(api)

# Initialize extensions with the Flask application instance
db.init_app(app)  # Initialize SQLAlchemy with Flask app
migrate = Migrate(app, db)  # Initialize Flask-Migrate for database migrations
login_manager = LoginManager(app)  # Initialize Flask-Login to manage user sessions
moment = Moment(app)  # Initialize Flask-Moment for date and time formatting
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@login_manager.user_loader
def load_user(user_id):
    # Define a user loader callback for Flask-Login, which loads a user from the database
    return User.query.filter_by(id=user_id).first()

# Flask-Login configuration
login_manager.login_view = 'auth.login_page'  # Define the view to redirect to when login is required
login_manager.login_message = 'Please log in to access this page!'  # Define the message to flash when a user is redirected to the login page
login_manager.login_message_category = 'danger'  # Define the category for the message to be flashed (used for styling the message)
