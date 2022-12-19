from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel

app = Flask(__name__)
app.secret_key='@2141241231%$'
app.config["SQLALCHEMY_DATABASE_URI"] ='mysql+pymysql://root:%s@localhost/saledb' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app=app)

app.config['CART_KEY'] = 'cart'
babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return "vi"