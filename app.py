from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from models import Empresa, empresas
import os

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API de Cadastro de Empresas"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.yaml')
def swagger_yaml():
    return send_from_directory(os.getcwd(), 'swagger.yaml')

@app.route('/empresa', methods=['POST'])
def criar_empresa():
    data = request.get_json()
    nova_empresa = Empresa(
        cnpj=data['cnpj'],
        nome_razao=data['nome_razao'],
        nome_fantasia=data['nome_fantasia'],
        cnae=data['cnae']
    )
    empresas.append(nova_empresa)
    return jsonify({'mensagem': 'Empresa criada com sucesso!'}), 201

@app.route('/empresas', methods=['GET'])
def listar_empresas():
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 10))
    empresas_paginadas = empresas[start:start + limit]
    resultado = [{
        'cnpj': empresa.cnpj,
        'nome_razao': empresa.nome_razao,
        'nome_fantasia': empresa.nome_fantasia,
        'cnae': empresa.cnae
    } for empresa in empresas_paginadas]
    return jsonify(resultado), 200

@app.route('/empresa/<cnpj>', methods=['PUT'])
def atualizar_empresa(cnpj):
    # Remover caracteres especiais do CNPJ
    cnpj = cnpj.replace('.', '').replace('-', '').replace('/', '')
    data = request.get_json()
    for empresa in empresas:
        if empresa.cnpj.replace('.', '').replace('-', '').replace('/', '') == cnpj:
            empresa.nome_fantasia = data.get('nome_fantasia', empresa.nome_fantasia)
            empresa.cnae = data.get('cnae', empresa.cnae)
            return jsonify({'mensagem': 'Empresa atualizada com sucesso!'}), 200
    return jsonify({'mensagem': 'Empresa não encontrada'}), 404

@app.route('/empresa/<cnpj>', methods=['DELETE'])
def deletar_empresa(cnpj):
    global empresas
    # Remover caracteres especiais do CNPJ
    cnpj = cnpj.replace('.', '').replace('-', '').replace('/', '')
    empresas = [empresa for empresa in empresas if empresa.cnpj.replace('.', '').replace('-', '').replace('/', '') != cnpj]
    return jsonify({'mensagem': 'Empresa removida com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)