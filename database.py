import motor.motor_asyncio

# setando conexões (lembrar de alterar localhost para testes em outro pc)
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.python_api_case

# setando os 2 objetos que serão persistidos no banco
user_collection = database.get_collection("users")
task_collection = database.get_collection("tasks")