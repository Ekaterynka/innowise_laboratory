from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}