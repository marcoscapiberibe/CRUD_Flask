from flask import Flask, request, jsonify
from models import Empresa, empresas

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)