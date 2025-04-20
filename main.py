from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import add_message
from fastapi.responses import FileResponse
app = FastAPI()


class TextSchema(BaseModel):
    user_id: str
    text: str


@app.get("/")
async def f():
    return FileResponse("index.html")


@app.post("/new_text")
async def new(data: TextSchema):
    try:
        await add_message(data.user_id, data.text)

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"{e}")
