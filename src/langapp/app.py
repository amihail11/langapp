from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def first():
    return {"mead": "fedsf"}
