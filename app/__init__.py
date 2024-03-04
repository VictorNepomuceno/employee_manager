#INICIAR APP, INICIAR BANCO DE DADOS e LOGIN
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager





app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost: 5433/employeesmanager'
app.secret_key = 'secreto'



login_manager = LoginManager(app)
db = SQLAlchemy(app)
app.app_context().push()



