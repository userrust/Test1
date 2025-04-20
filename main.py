from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def f():
    return "Hello"