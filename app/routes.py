from flask import Flask, request, jsonify, send_from_directory
import os
from marshmallow import ValidationError
from app import app, db
from app.models import Empresa
from app.schemas import EmpresaSchema
import jwt
import datetime
from functools import wraps

empresa_schema = EmpresaSchema()

# Configurações para os tempos de expiração dos tokens
ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)

def generate_token(user, expires_in, token_type="access"):
    return jwt.encode({
        'user': user,
        'exp': datetime.datetime.now(datetime.timezone.utc) + expires_in,
        'type': token_type
    }, app.config['SECRET_KEY'], algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or "Bearer " not in token:
            return jsonify({'mensagem': 'Token de autenticação é necessário!'}), 403

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            if decoded_token['type'] != 'access':
                return jsonify({'mensagem': 'Token de acesso inválido!'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirou, faça login novamente!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido!'}), 403

        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()

    if dados['username'] == 'admin' and dados['password'] == 'senha654321':
        access_token = generate_token(dados['username'], ACCESS_TOKEN_EXPIRES, "access")
        refresh_token = generate_token(dados['username'], REFRESH_TOKEN_EXPIRES, "refresh")

        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas!'}), 401

@app.route('/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.get_json().get('refresh_token')

    if not refresh_token:
        return jsonify({'mensagem': 'Refresh token é necessário!'}), 403

    try:
        decoded_refresh_token = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=["HS256"])
        if decoded_refresh_token['type'] != 'refresh':
            return jsonify({'mensagem': 'Token inválido!'}), 403

        # Gerar um novo access token
        new_access_token = generate_token(decoded_refresh_token['user'], ACCESS_TOKEN_EXPIRES, "access")
        return jsonify({'access_token': new_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'mensagem': 'Refresh token expirou, faça login novamente!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'mensagem': 'Token inválido!'}), 403

@app.route('/swagger.json')
def swagger_json():
    return send_from_directory(os.path.join(os.path.dirname(__file__)), 'swagger.json')

@app.route('/empresa', methods=['POST'])
@token_required
def criar_empresa():
    data = request.get_json()
    cnpj_limpo = data['cnpj'].replace('.', '').replace('-', '').replace('/', '')
    nova_empresa = Empresa(
        cnpj=cnpj_limpo,
        nome_razao=data['nome_razao'],
        nome_fantasia=data['nome_fantasia'],
        cnae=data['cnae']
    )
    db.session.add(nova_empresa)
    db.session.commit()
    return jsonify({'mensagem': 'Empresa criada com sucesso!'}), 201

@app.route('/empresas', methods=['GET'])
def listar_empresas():
    # Parâmetros de paginação e ordenação
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 10))
    sort = request.args.get('sort', 'id')  # Ordenar por 'id' por padrão
    dir = request.args.get('dir', 'asc')  # Direção padrão é ascendente

    # Ajustar a direção de ordenação
    if dir == 'desc':
        sort_param = getattr(Empresa, sort).desc()
    else:
        sort_param = getattr(Empresa, sort).asc()

    # Contar o número total de empresas no banco de dados
    total_empresas = Empresa.query.count()

    # Query com paginação e ordenação
    empresas_paged = Empresa.query.order_by(sort_param).offset(start).limit(limit).all()

    # Montar o resultado da paginação
    resultado = [{
        'cnpj': empresa.cnpj,
        'nome_razao': empresa.nome_razao,
        'nome_fantasia': empresa.nome_fantasia,
        'cnae': empresa.cnae
    } for empresa in empresas_paged]

    # Retornar os dados paginados e o número total de empresas
    return jsonify({
        'empresas': resultado,
        'total': total_empresas  # Retorna o número total de empresas
    }), 200

@app.route('/empresa/<cnpj>', methods=['PUT'])
@token_required
def atualizar_empresa(cnpj):
    try:
        cnpj_limpo = cnpj.replace('.', '').replace('-', '').replace('/', '')
        print(f"CNPJ para atualizar: {cnpj_limpo}")
        
        empresa = Empresa.query.filter_by(cnpj=cnpj_limpo).first()
        print(f"Empresa encontrada: {empresa}")
        
        if empresa:
            # Dados enviados na requisição
            data = request.get_json()
            print(f"Dados recebidos: {data}")
            
            # Carregar e validar os dados enviados no corpo da requisição (parcial)
            validated_data = empresa_schema.load(data, partial=True)  # Permitir atualização parcial
            print(f"Dados validados: {validated_data}")
            
            # Atualizar os campos permitidos
            if 'nome_fantasia' in validated_data:
                empresa.nome_fantasia = validated_data['nome_fantasia']
            if 'cnae' in validated_data:
                empresa.cnae = validated_data['cnae']
            
            db.session.commit()
            return jsonify({'mensagem': 'Empresa atualizada com sucesso!'}), 200
        
        return jsonify({'mensagem': 'Empresa não encontrada'}), 404
    except ValidationError as err:
        print(f"Erros de validação: {err.messages}")
        return jsonify(err.messages), 400

@app.route('/empresa/<cnpj>', methods=['DELETE'])
@token_required
def deletar_empresa(cnpj):
    # Remover caracteres especiais do CNPJ
    cnpj = cnpj.replace('.', '').replace('-', '').replace('/', '')
    print(f"CNPJ formatado: {cnpj}")
    empresa = Empresa.query.filter_by(cnpj=cnpj).first()

    if empresa:
        db.session.delete(empresa)
        db.session.commit()
        return jsonify({'mensagem': 'Empresa removida com sucesso!'}), 200
    return jsonify({'mensagem': 'Empresa não encontrada'}), 404