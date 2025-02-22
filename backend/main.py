from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models.models import Message, User
from db.supabase import create_supabase_client
from utils.encrypt import hash_password, verify_password
from utils.jwt import create_access_token

app = FastAPI()
supabase_client = create_supabase_client()

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

''' AUTHENTICATION STUFF STARTS HERE '''


@app.post("/login")
async def login(user: User):
    try:
        response = supabase_client.table("users").select(
            "password_hash").eq("username", user.username).single().execute()

        if not response or not verify_password(user.password, response.data.get('password_hash')):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token(user.username)

        return {"status": 200, "message": "Success", "data": {"token": token, "username": user.username}}

    except:
        raise HTTPException(status_code=401, detail="Invalid username")

    return {"message": "Success"}


@ app.post("/register")
async def register(user: User):
    password_hash = hash_password(user.password)

    try:
        supabase_client.table("users").insert(
            {"username": user.username, "password_hash": password_hash}
        ).execute()

        return {"message": "User created successfully"}

    except:
        raise HTTPException(status_code=400, detail="Username already exists")

''' AUTHENTICATION STUFF ENDS HERE '''

global_chat_log = []


@ app.post("/global/messages")
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


@ app.websocket("/ws/{client_id}")
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
