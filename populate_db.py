from app import db, app  # Importar o 'app' para gerenciar o contexto
from app.models import Empresa
import random

# Função para gerar CNPJ aleatório
def gerar_cnpj():
    return f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/0001-{random.randint(10, 99)}"

# Função para gerar CNAE aleatório
def gerar_cnae():
    return f"{random.randint(1000, 9999)}-{random.randint(1, 9)}/{random.randint(10, 99)}"

# Função para gerar nomes aleatórios
def gerar_nome(tipo):
    if tipo == "razao":
        return f"Empresa Exemplo {random.randint(1, 100)} S.A."
    else:
        return f"Fantasia {random.randint(1, 100)}"

# Popular o banco com 50 empresas
def popular_empresas():
    for _ in range(150):
        nova_empresa = Empresa(
            cnpj=gerar_cnpj(),
            nome_razao=gerar_nome("razao"),
            nome_fantasia=gerar_nome("fantasia"),
            cnae=gerar_cnae()
        )
        db.session.add(nova_empresa)
    db.session.commit()
    print("150 empresas adicionadas com sucesso!")

if __name__ == "__main__":
    with app.app_context():  # Entrar no contexto da aplicação
        popular_empresas()