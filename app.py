from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

#Configuracao do Flask e da base de dados
flaskApp = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))

flaskApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flaskApp.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(project_dir, "app.db")
SQLALCHEMY_BINDS = {'user_db': 'sqlite:///' + os.path.join(project_dir, "users.db"), 'plan_db': 'sqlite:///' + os.path.join(project_dir, "plans.db")}

db = SQLAlchemy(flaskApp)

from api.User import User
from api.Plan import Plan
db.create_all()

if __name__ == '__main__':
  
  from api import *
  flaskApp.run(debug=True, port=5000)
