from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API de Cadastro de Empresas"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)