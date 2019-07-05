from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

""" from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

#configuration
app = Flask(__name__)
#Added this line for CH3 Forms
app.config['SECRET_KEY'] = 'pwkey'
#Added this line for CH4 SQLite to Postgres SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///photography.db'
#Added this line for CH4 DB make database instance below
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)

from flaskchapel import routes, models """
