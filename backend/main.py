from models.models import Message, User
from utils.encrypt import hash_password, verify_password
from utils.jwt import create_access_token, verify_token
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from db.supabase import create_supabase_client
import json
from postgrest.exceptions import APIError
from messages import Message, MessageType
from ai.run_model import classify

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
    # "http://localhost",
    # "http://localhost:3000",  # This should be your frontend URL
    "*"
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

""" AUTHENTICATION STUFF STARTS HERE """


@app.post("/logout")
async def logout():
    return {"message": "Success"}


@app.post("/login")
async def login(user: User):
    try:
        response = (
            db_client.table("users")
            .select("password_hash")
            .eq("username", user.username)
            .single()
            .execute()
        )

        if not response or not verify_password(
            user.password, response.data.get("password_hash")
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(user.username)

        return {
            "status": 200,
            "message": "Success",
            "data": {"token": token, "username": user.username},
        }

    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/register")
async def register(user: User):
    password_hash = hash_password(user.password)

    try:
        db_client.table("users").insert(
            {"username": user.username, "password_hash": password_hash}
        ).execute()

        return {"message": "User created successfully"}

    except:
        raise HTTPException(status_code=400, detail="Username already exists")


""" AUTHENTICATION STUFF ENDS HERE """


@app.get("/leaderboard")
async def leaderboard(query: str = "messages"):
    if query == "messages":
        try:
            response = db_client.table("messages").select("username").execute()
            responseUsers = db_client.table(
                "users").select("username").execute()
            message_counts = {}
            result = {}
            for record in response.data:
                username = record["username"]
                if username in message_counts:
                    message_counts[username] += 1
                else:
                    message_counts[username] = 1

            for username, count in message_counts.items():
                result[username] = count

            for record in responseUsers.data:
                username = record["username"]
                if username not in result:
                    result[username] = 0

            return {"payload": result}
        except APIError as e:
            print("Rats", e)
    elif query == "credits":
        try:
            response = (
                db_client.table("users").select(
                    "username,anti_social_credit").execute()
            )

            result = {}

            for record in response.data:
                result[record["username"]] = record["anti_social_credit"]

            return {"payload": result}
        except APIError as e:
            print("Rats", e)


async def send_old_messages(websocket: WebSocket):
    response = None
    try:
        response = (
            db_client.table("messages")
            .select("*")
            .limit(OLD_MESSAGE_LOAD_AMOUNT)
            .execute()
        )
    except APIError as error:
        print("Failed to load messages, tell the client probably", error)
    if response != None:
        for message in response.data:
            await manager.send_personal_message(json.dumps(message), websocket)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await send_old_messages(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            message = Message.from_json(data)
            authenticated = verify_token(message.token) == message.username

            if authenticated:
                if message.message_type == MessageType.CHAT:
                    categories = classify(message.content.text)
                    dad_joke = categories[0]
                    nerdy = categories[1]
                    positive = categories[2]
                    negative = categories[3]
                    neutral = categories[4]
                    brainrot = categories[5]

                    if (dad_joke > nerdy and dad_joke > positive and dad_joke > negative and dad_joke > neutral and dad_joke > brainrot):
                        most_likely_category = "dad_joke"
                    elif (nerdy > dad_joke and nerdy > positive and nerdy > negative and nerdy > neutral and nerdy > brainrot):
                        most_likely_category = "nerdy"
                    elif (positive > dad_joke and positive > nerdy and positive > negative and positive > neutral and positive > brainrot):
                        most_likely_category = "positive"
                    elif (negative > dad_joke and negative > nerdy and negative > positive and negative > neutral and negative > brainrot):
                        most_likely_category = "negative"
                    elif (neutral > dad_joke and neutral > nerdy and neutral > positive and neutral > negative and neutral > brainrot):
                        most_likely_category = "neutral"
                    elif (brainrot > dad_joke and brainrot > nerdy and brainrot > positive and brainrot > negative and brainrot > neutral):
                        most_likely_category = "brainrot"

                    db_message = {
                        "username": message.username,
                        "text": message.content.text,
                        "timestamp": message.content.timestamp,
                        "classification": most_likely_category,
                    }

                    response = db_client.table(
                        "messages").insert(db_message).execute()
                    db_message["message_id"] = response.data[0]["message_id"]

                    await manager.broadcast(json.dumps(db_message))
                elif message.message_type == MessageType.REACTION:
                    pass
            else:
                raise HTTPException(
                    status_code=401, detail="Invalid token, please reauthenticate!"
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


"""ANTI-SOCIAL CREDIT CODE RESIDES HEREIN"""


@app.get("/antiSocialCredit/{username}")
async def get_anti_social_credit(username: str):
    try:
        response = (
            db_client.table("users")
            .select("anti_social_credit")
            .eq("username", username)
            .execute()
        )

        print("Here's the response.data: ", response.data)

        if not response.data:
            raise HTTPException(status_code=404, detail="Invalid username")

        return {
            "username": username,
            "anti_social_credit": response.data[0]["anti_social_credit"],
        }

    except Exception as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Invalid username")
        else:
            print(f"Something went wrong: {e}")
            raise HTTPException(
                status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run("example:app", host="127.0.0.1", port=8000, reload=True)
