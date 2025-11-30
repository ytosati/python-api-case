# ARQUIVO COM AS CLASSES TRABALHADAS PELA API
from pydantic import BaseModel, EmailStr, Field

# Criar conta
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nome do usuário")
    email: EmailStr = Field(..., min_length=3,description="Email do usuário")
    password: str = Field(..., min_length=3, description="Senha")

# Return da api (sem a senha)
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

# Receber os dados no endpoint de login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Return do token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Criar Task
class TaskCreate(BaseModel):
    title: str = Field(..., description="Título da tarefa")
    description: str = Field(..., description="Descrição da tarefa")

# Return da api
class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    owner_id: str
