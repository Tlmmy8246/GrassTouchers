from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()


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

if __name__ == "__main__":
    uvicorn.run("example:app", host="127.0.0.1", port=8000, reload=True)

