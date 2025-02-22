from models.models import Message, User
from utils.encrypt import hash_password, verify_password
from utils.jwt import create_access_token
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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
    "http://localhost:3000",  # This should be your frontend URL
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
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token(user.username)

        return {
            "status": 200,
            "message": "Success",
            "data": {"token": token, "username": user.username},
        }

    except:
        raise HTTPException(status_code=401, detail="Invalid username")

    return {"message": "Success"}


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


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await send_old_messages(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                response = db_client.table("messages").insert(message).execute()
                await manager.broadcast(data)
            except APIError as error:
                print("Failed to send message, tell the client probably", error)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


"""ANTI-SOCIAL CREDIT CODE RESIDES HEREIN"""

@app.get("/antiSocialCredit/{username}")
async def get_anti_social_credit(username: str):
    try:
        response = (
            db_client.table("users")
            .select("username, anti_social_credit")
            .eq("username", username)
            .execute()
        )

        print("Here's the response.data: ", response.data)

        if not response.data:
            raise HTTPException(status_code=404, detail="Invalid username")
        
        return response.data[0]

    except Exception as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Invalid username")
        else:
            print(f"Something went wrong: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


"""GRASS CODE IS HERE"""
# How to use:
# In the websocket loop, when you're iterating over all the users, just poll 
#     the grass_status and return to user's front end their status

@app.get("/grass/{username}")
async def grass_status(username: str):
    if await user_exists(username):
        try:
            response = (
                db_client.table("grass")
                .select("username, x_coord, y_coord, grass_number, size, growth_rate")
                .eq("username", username)
                .execute()
            )
            return response.data[0]
        except Exception as e:
            if e.status_code == 404:
                raise HTTPException(status_code=404, detail="Invalid username")
            else:
                print(f"Something went wrong: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

# adds more grass, does not grow the grass that already exists
# number of grass to plant is based on AI assessment of cringe
#      or the number of reactions
@app.post("/grass/{username}/{num_grass_to_plant}")
async def plant_grass(username: str, num_grass_to_plant: int=1):
    if await user_exists(username):
        try:
            response = response = (
                db_client.table("grass")
                .select("username, x_coord, y_coord, grass_number, size, growth_rate")
                .eq("username", username)
                .execute()
            )
            if not response.data: # user has no grass records, start grass growth
                db_client.table("grass").insert(
                    {"username": username, 
                    "x_coord": (int)(random.random() * 100), 
                    "y_coord": (int)(random.random() * 100), 
                    "grass_number": 1,
                    "size": (int)(random.random() * 15) + 5, # range of 5-20
                    "growth_rate": (int)(random.random() * 20) + 100} # 100 +/- 20
                ).execute()
            else:
                db_client.table("grass").update(
                    {"grass_number": response.data[0]["grass_number"] + (int)(num_grass_to_plant)}
                ).eq("username", username
                ).execute()
        except Exception as e:
            print(f"Something went wrong: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

# grow the grass that already exists, does not add more grass
@app.patch("/grass/{username}")
async def grow_grass(username: str):
    if await user_exists(username):
        try:
            response = (
                db_client.table("grass")
                .select("username, x_coord, y_coord, grass_number, size, growth_rate")
                .eq("username", username)
                .execute()
            )
            if not response.data: # user has no grass records, start grass growth
                plant_grass(username)
            else:
                db_client.table("grass").update(
                        {"size": response.data[0]["size"] * (response.data[0]["growth_rate"])}
                    ).eq("username", username
                    ).execute()
        except Exception as e:
            print(f"Something went wrong: {e}")
            raise HTTPException(status_code=500, detail="Invternal Server Error")


# fertilize the grass (increase growth rate)
# can make the fertilizer extra strong if their messages were extra cringe
async def fertilize_grass(username: str, fertilizer_strength: int=20):
    if await user_exists(username):
        try:
            response = (
                db_client.table("grass")
                .select("username, x_coord, y_coord, grass_number, size, growth_rate")
                .eq("username", username)
                .execute()
            )
            if not response.data: # user has no grass records, start grass growth
                plant_grass(username)
            else:
                db_client.table("grass").update(
                    {"size": response.data[0]["size"] * (response.data[0]["growth_rate"]),
                    "growth_rate": response.data[0]["growth_rate"] +  (int)(fertilizer_strength)}
                ).eq("username", username
                ).execute()
        except Exception as e:
            print(f"Something went wrong: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

async def user_exists(username: str):
    try:
        response = (
            db_client.table("users")
            .select("username")
            .eq("username", username)
            .execute()
        )
        if len(response.data) != 1:
            raise HTTPException(status_code=404, detail="Invalid username")
        else:
            return True

    except Exception as e:
        print(f"Something went wrong: {e}")
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Invalid username")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("example:app", host="127.0.0.1", port=8000, reload=True)
