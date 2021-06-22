from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Configure app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize login manager
login = LoginManager(app)
login.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
