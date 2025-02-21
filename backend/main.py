from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# An example
# @app.post("/chat")
# async def do():
#     return {"json": "cool"}
