from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models.models import Message, LoginData
from db.supabase import create_supabase_client
import json
import postgrest
from postgrest.exceptions import APIError

db_client = create_supabase_client()
OLD_MESSAGE_LOAD_AMOUNT = 50

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

app = FastAPI()

manager = ConnectionManager()

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


async def send_old_messages(websocket: WebSocket):
    response = None
    try:
        response = (db_client.table("messages")
            .select("*")
            .limit(OLD_MESSAGE_LOAD_AMOUNT)
            .execute()
        )
    except APIError as error:
        print("Failed to load messages, tell the client probably",error)
    if response != None:
        for message in response.data:
            await manager.send_personal_message(json.dumps(message), websocket)
    

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await send_old_messages(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                response = (db_client.table("messages")
                    .insert(message)
                    .execute()
                )
                await manager.broadcast(data)
            except APIError as error:
                print("Failed to send message, tell the client probably",error)

    except WebSocketDisconnect:
        manager.disconnect(websocket)    

if __name__ == "__main__":
    uvicorn.run("example:app", host="127.0.0.1", port=8000, reload=True)
