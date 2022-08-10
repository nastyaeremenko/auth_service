from flasgger import Swagger
from flask import Blueprint, Flask
from flask_restful import Api
from flask_uuid import FlaskUUID

from app.api.v1.routes import initialize_routes
from app.commands import create_superuser
from app.core import config
from app.core.db import init_db
from app.core.jwt_conf import init_jwt
from app.core.oauth import init_oauth
from app.core.tracer import configure_tracer

app = Flask(__name__)

blue_api = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blue_api)
app.register_blueprint(blue_api)

app.config.from_object(config.Config)

swagger = Swagger(app, template=app.config['SWAGGER_TEMPLATE'])
app.cli.add_command(create_superuser)

FlaskUUID(app)
configure_tracer(
    app,
    host=app.config['JAEGER_TRACE'],
    port=app.config['JAEGER_PORT']
)

init_db(app)
init_jwt(app)
init_oauth(app)

app.secret_key = 'some secret key'

with app.app_context():
    pass

initialize_routes(api)
