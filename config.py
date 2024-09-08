import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv('SECRET_KEY', 'minha_chave_secreta')
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)  # Tempo do access token
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)  # Tempo do refresh token