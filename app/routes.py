from flask import Flask, request, jsonify, send_from_directory
import os
from marshmallow import ValidationError
from app import app
from app.models import Empresa, empresas
from app.schemas import EmpresaSchema

empresa_schema = EmpresaSchema()

@app.route('/swagger.json')
def swagger_json():
    return send_from_directory(os.path.join(os.path.dirname(__file__)), 'swagger.json')

@app.route('/empresa', methods=['POST'])
def criar_empresa():
    try:
        # Validação dos dados
        dados = empresa_schema.load(request.get_json())
        # Se passar na validação, criar a nova empresa
        nova_empresa = Empresa(
            cnpj=dados['cnpj'],
            nome_razao=dados['nome_razao'],
            nome_fantasia=dados['nome_fantasia'],
            cnae=dados['cnae']
        )
        empresas.append(nova_empresa)
        return jsonify({'mensagem': 'Empresa criada com sucesso!'}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

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
    try:
        dados = empresa_schema.load(request.get_json())
        for empresa in empresas:
            if empresa.cnpj == cnpj:
                empresa.nome_fantasia = dados['nome_fantasia']
                empresa.cnae = dados['cnae']
                return jsonify({'mensagem': 'Empresa atualizada com sucesso!'}), 200
        return jsonify({'mensagem': 'Empresa não encontrada'}), 404
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route('/empresa/<cnpj>', methods=['DELETE'])
def deletar_empresa(cnpj):
    global empresas
    # Remover caracteres especiais do CNPJ
    cnpj = cnpj.replace('.', '').replace('-', '').replace('/', '')
    empresas = [empresa for empresa in empresas if empresa.cnpj.replace('.', '').replace('-', '').replace('/', '') != cnpj]
    return jsonify({'mensagem': 'Empresa removida com sucesso!'}), 200
