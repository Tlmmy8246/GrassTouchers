from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str
    timestamp: str
    uid: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/global/messages")
async def globalMessage(message: Message):
    print(message)


# An example
# @app.post("/chat")
# async def do():
#     return {"json": "cool"}
