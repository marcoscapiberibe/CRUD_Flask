from app import db

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nome_razao = db.Column(db.String(40), nullable=False)
    nome_fantasia = db.Column(db.String(40), nullable=False)
    cnae = db.Column(db.String(7), nullable=False)

empresas = []