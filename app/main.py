
from fastapi import FastAPI

uuid_pet_dict = {}

app = FastAPI()


@app.post('/create_account')
async def create_account():
    pass


@app.get('/')
async def index():
    return {"Real": "Python"}
