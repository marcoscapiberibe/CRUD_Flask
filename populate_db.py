from app import db, app  # Importar o 'app' para gerenciar o contexto
from app.models import Empresa
import random

def gerar_cnpj():
    # Exemplo simples para gerar um CNPJ fictício
    return "{}{}{}.{}{}{}.{}{}{}{}-{}".format(
        random.randint(0, 9), random.randint(0, 9), random.randint(0, 9),
        random.randint(0, 9), random.randint(0, 9), random.randint(0, 9),
        random.randint(0, 9), random.randint(0, 9), random.randint(0, 9),
        random.randint(0, 9), random.randint(0, 9)
    )

def limpar_cnpj(cnpj):
    # Remove pontos, barras e hífens do CNPJ
    return cnpj.replace('.', '').replace('-', '').replace('/', '')

def popular_empresas():
    for _ in range(50):  # Por exemplo, 50 empresas
        cnpj = limpar_cnpj(gerar_cnpj())
        nova_empresa = Empresa(
            cnpj=cnpj,
            nome_razao=f"Razão Social {_}",
            nome_fantasia=f"Nome Fantasia {_}",
            cnae=str(random.randint(1000, 9999)) + '-' + str(random.randint(1, 9)) + '/' + str(random.randint(10, 99))
        )
        db.session.add(nova_empresa)

    db.session.commit()
    print("Empresas cadastradas com sucesso!")

if __name__ == "__main__":
    with app.app_context():  # Entrar no contexto da aplicação
        popular_empresas()