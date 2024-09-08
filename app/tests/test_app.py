import pytest
import json
from flask import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app, db 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Cria o banco de dados para os testes
        yield client
        with app.app_context():
            db.drop_all()  # Limpa o banco de dados após os testes

def obter_token(client):
    # Autentica API e obtem o token JWT
    login_data = {
        'username': 'admin',
        'password': 'senha654321'
    }
    rv = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    return json.loads(rv.data)['access_token']  # Substitui 'access_token' se o nome do campo for diferente

def test_get_empresas(client):
    """Teste para garantir que a rota de listar empresas está funcionando"""
    token = obter_token(client)  # Obtém o token
    rv = client.get('/empresas', headers={'Authorization': f'Bearer {token}'})
    
    assert rv.status_code == 200
    
    # Verifica se a resposta contém a chave 'empresas' e se é uma lista (mesmo que vazia)
    data = json.loads(rv.data)
    assert 'empresas' in data
    assert isinstance(data['empresas'], list)

def test_post_empresa(client):
    """Teste para criar uma empresa"""
    token = obter_token(client)  # Obtém o token
    new_empresa = {
        'cnpj': '12.345.678/0001-95',
        'nome_razao': 'Empresa Teste',
        'nome_fantasia': 'Fantasia Teste',
        'cnae': '1234-5/67'
    }
    rv = client.post('/empresa', data=json.dumps(new_empresa), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert rv.status_code == 201  # Verifica se foi criado com sucesso

def test_put_empresa(client):
    """Teste para atualizar uma empresa"""
    token = obter_token(client)  # Obtém o token

    # Cria uma empresa
    new_empresa = {
        'cnpj': '12.345.678/0001-95',
        'nome_razao': 'Empresa Teste',
        'nome_fantasia': 'Fantasia Teste',
        'cnae': '1234-5/67'
    }
    client.post('/empresa', data=json.dumps(new_empresa), content_type='application/json', headers={'Authorization': f'Bearer {token}'})

    # Atualização dos dados
    updated_data = {
        'nome_fantasia': 'Fantasia Teste Atualizada',
        'cnae': '5678-9/01'
    }
    rv = client.put('/empresa/12345678000195', data=json.dumps(updated_data), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert rv.status_code == 200  # Verifica se a atualização foi bem-sucedida

def test_delete_empresa(client):
    """Teste para deletar uma empresa"""
    token = obter_token(client)  # Obtém o token

    # Cria uma empresa
    new_empresa = {
        'cnpj': '12.345.678/0001-95',
        'nome_razao': 'Empresa Teste',
        'nome_fantasia': 'Fantasia Teste',
        'cnae': '1234-5/67'
    }
    client.post('/empresa', data=json.dumps(new_empresa), content_type='application/json', headers={'Authorization': f'Bearer {token}'})

    # Deleta Empresa
    rv = client.delete('/empresa/12345678000195', headers={'Authorization': f'Bearer {token}'})
    assert rv.status_code == 200  # Verifica se a exclusão foi bem-sucedida