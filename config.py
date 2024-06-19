import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PW")}' +
    f'@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)