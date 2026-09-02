from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from telethon import TelegramClient

import config
from store import TeleDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = config.load()

    required = ("API_ID", "API_HASH", "CHANNEL_ID")
    missing = [key for key in required if not cfg.get(key)]
    if missing:
        raise SystemExit(f"Missing values in .env: {', '.join(missing)}")

    client = TelegramClient("anon", int(cfg["API_ID"]), cfg["API_HASH"])
    await client.start()
    client.parse_mode = None

    db = TeleDB(client, int(cfg["CHANNEL_ID"]))
    await db.build_index()

    app.state.db = db

    try:
        yield
    finally:
        await client.disconnect()


app = FastAPI(lifespan=lifespan)


class SetRequest(BaseModel):
    value: str


@app.get("/health")
async def health():
    return {"keys": len(app.state.db.records)}


@app.get("/kv/{key}")
async def get_key(key: str):
    value = app.state.db.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"key not found: {key}")
    return {"key": key, "value": value}


@app.put("/kv/{key}")
async def set_key(key: str, payload: SetRequest):
    try:
        await app.state.db.set(key, payload.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"key": key, "value": payload.value}


@app.delete("/kv/{key}")
async def delete_key(key: str):
    try:
        await app.state.db.delete(key)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"key not found: {key}")
    return Response(status_code=204)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
