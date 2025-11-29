# ARQUIVO DE SEGURANÇA E CRIPTOGRAFIA
import bcrypt
from datetime import datetime, timedelta
from jose import jwt

# Funções de hash e verificação utilizando bcrypt

# Recebe a senha e retorna hashed
def get_password_hash(password: str) -> str:

    # encoding utf-8 adicionado para evitar um erro que acontecia com o tamanho da senha em bytes
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')

# Booleana que retorna true caso bata com o hash n obanco
def verify_password(plain_password: str, hashed_password: str) -> bool:

    # Mesmo encoding para evitar o erro que acontecia anteriormente.
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hash_bytes)


# Configuração do token JWT
key = "SECRETKEYabc123def456"
algoritmo = "HS256"
token_expire_minutes = 30

# Função que gera o token, recebendo um dicionario
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key, algorithm=algoritmo)

    return encoded_jwt


