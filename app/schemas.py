import re
from marshmallow import Schema, fields, validate, ValidationError

# Validar e permitir CNPJ com pontos e traços
def validate_cnpj(cnpj):
    # Remover pontos, traços e barras
    cnpj_limpo = re.sub(r'[^\d]', '', cnpj)
    if len(cnpj_limpo) != 14 or not cnpj_limpo.isdigit():
        raise ValidationError("CNPJ deve conter 14 dígitos numéricos, incluindo ou não pontos, traços e barras.")

# Validar e permitir CNAE com pontos e traços
def validate_cnae(cnae):
    # Remover pontos e traços
    cnae_limpo = re.sub(r'[^\d]', '', cnae)
    if len(cnae_limpo) != 7 or not cnae_limpo.isdigit():
        raise ValidationError("CNAE deve conter 7 dígitos numéricos, incluindo ou não pontos e traços.")

# Schema para validar os dados de Empresa
class EmpresaSchema(Schema):
    cnpj = fields.String(required=True, validate=validate_cnpj)
    nome_razao = fields.String(required=True, validate=validate.Length(min=3, max=100))
    nome_fantasia = fields.String(required=True, validate=validate.Length(min=3, max=100))
    cnae = fields.String(required=True, validate=validate_cnae)