from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object('config')

CORS(app, resources={r"/*": {"origins": "*"}})

# Configurações Swagger
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API de Cadastro de Empresas"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Inicializar o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models