from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
#import do cors middleware para facilitar futura integraçao para o frontend
from fastapi.middleware.cors import CORSMiddleware

from database import *
from models import *
from security import *

# Função qeu gerencia o ciclo de vida da api para acompanhamentos e testes
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("iniciando api")
    try:
        await database.list_collection_names()
        print("conexão bem sucedida")
    except Exception as e:
        print(f"falha ao conectar ao banco : {e}")
    yield
    print("encerrando api")

    
# instanciando lifespan no app
app = FastAPI(lifespan=lifespan)

# Configuração do cors. Pesquisei as rotas mais usadas pelos principais frameworks de front end para facilitar a integraçao.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setando endpoint para receber o token como login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para validar o token do usuario ativo
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, key, algorithms=[algoritmo])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = await user_collection.find_one({"email": email})
    if user is None:
        raise credentials_exception
        
    return user


# --------------------------------- ENDPOINTS PÚBLICOS --------------------------------- #

@app.get("/")
def read_root():
    return {"message": "API rodando", "status": "ok"}

# Endpoint de registro do usuário
@app.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # logica para validar se já existe o email na base
    existing_user = await user_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400 , detail="Email já cadastrado")
    
    # Criptografar a senha
    hashed_password = get_password_hash(user.password)

    user_dict = user.model_dump()
    user_dict["password"] = hashed_password

    # Persistir no mongoDB
    result = await user_collection.insert_one(user_dict)

    # Retornar dados do usuário (sem a senha)
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }

# Endpoint de login
@app.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    user = await user_collection.find_one({"email": login_data.email})

    # Logica para verificar credenciais
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    # Gera e retorna o token
    token = create_access_token(data={"sub": user["email"]})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# --------------------------------- ENDPOINTS PROTEGIDOS --------------------------------- #

# CREATE - Endpoint para criar nova tarefa, validando o token
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):

    task_dict = task.model_dump()
    
    # sincronizar ID da tarefa com ID do dono para futuras manipulações
    task_dict["owner_id"] = str(current_user["_id"])

    result = await task_collection.insert_one(task_dict)

    return {
        "id": str(result.inserted_id),
        "title": task.title,
        "description": task.description,
        "owner_id": task_dict["owner_id"]
    }

# READ - Endpoint que lista as tarefas do usuário
@app.get("/tasks", response_model=list[TaskResponse])
async def list_my_tasks(current_user: dict = Depends(get_current_user)):

    # Busca no banco pelo ID do usuário e retorna apenas as tasks referentes ao mesmo
    tasks_cursor = task_collection.find({"owner_id": str(current_user["_id"])})
    
    tasks = []
    async for task in tasks_cursor:
        tasks.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"],
            "owner_id": task["owner_id"]
        })
        
    return tasks

# UPDATE - Endpoint para atualizar tasks, caso exista pelo id
@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskCreate, current_user: dict = Depends(get_current_user)):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID da tarefa inválido")

    task = await task_collection.find_one({"_id": ObjectId(task_id), "owner_id": str(current_user["_id"])})
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    await task_collection.update_one(
        {"_id": ObjectId(task_id)}, 
        {"$set": task_data.model_dump()}
    )

    return {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description,
        "owner_id": str(current_user["_id"])
    }

# DELETE - Endpoint para deletar uma task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):

    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID da tarefa inválido")

    result = await task_collection.delete_one({"_id": ObjectId(task_id), "owner_id": str(current_user["_id"])})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return None