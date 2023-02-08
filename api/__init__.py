from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


# create_app function
# This function is used to create the app
# It takes in a config parameter which is used to set the app config
# It returns the app
# It also registers the namespaces and the shell context processor
# The shell context processor is used to add the db, User and Order models to the shell context
# This allows us to use the models in the shell
def create_app(config_=config_dict['dev']):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config_)

    # initialize extensions
    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    # instantiate the api
    api = Api(app)

    # register the namespaces
    # they will appear under /orders and /auth
    api.add_namespace(order_namespace)
    # the path parameter is used to set the path for the namespace
    api.add_namespace(auth_namespace, path='/auth')

    # shell context processor
    # this allows us to use the models in the shell
    # it adds the db, User and Order models to the shell context
    # this allows us to use the models in the shell
    # for example, we can use User.query.all() to get all users
    # or Order.query.all() to get all orders
    # or User.query.filter_by(username='admin').first() to get the admin user
    # or Order.query.filter_by(id=1).first() to get the order with id 1
    # or User.query.filter_by(username='admin').first().orders to get the orders for the admin user
    # or Order.query.filter_by(id=1).first().user to get the user for the order with id 1
    # or User.query.filter_by(username='admin').first().orders[0].user to get the user for the first order for the admin user
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order
        }

    # return app
    return app
