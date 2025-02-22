from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Message(BaseModel):
    text: str
    timestamp: int
    uid: str


class LoginData(BaseModel):
    username: str
    password: str


origins = [
    "http://localhost",
    "http://localhost:3000"  # This should be your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

log = []

@app.post("/post-login/")
def post_login(loginData: LoginData):
    print("% LOGIN DATA", loginData)
    return {"message": "Success"}


@app.get("/login")
async def get_login():
    return {"message": "Success"}

global_chat_log = []

@app.post("/global/messages")
async def global_chat(message: Message):
    global_chat_log.append(message)
    return {"message": "success"}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept() 
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

async def send_old_messages(websocket: WebSocket):
    for message in global_chat_log[:50]:
        await manager.send_personal_message(str(message), websocket)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await send_old_messages(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            global_chat_log.append(data)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)    

if __name__ == "__main__":
    uvicorn.run("example:app", host="127.0.0.1", port=8000, reload=True)
