from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 123456
app.config['JWT_SECRET_KEY'] = "adconnect"

CORS(app, origins="*")
jwt = JWTManager(app)
api = Api(app) 
db = SQLAlchemy(app)