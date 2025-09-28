import os
import json
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from midi import send_midi
import httpx
from config import MEDIA_DIR, TEMPLATE_DIR, ARDUINO_BASE_URL, STATE

state = STATE.copy()

router = APIRouter()

# --- API ---
@router.post("/api/command")
async def handle_command(request: Request):
    body = await request.json()
    cmd = body.get("cmd")

    # Определяем объект и состояние по окончанию команды
    if cmd.endswith("On"):
        obj_name = cmd[:-2]  # убираем "On"
        new_state = True
    elif cmd.endswith("Off"):
        obj_name = cmd[:-3]  # убираем "Off"
        new_state = False
    else:
        return JSONResponse(status_code=400, content={"error": f"Invalid command: {cmd}"})

    # Обновляем локальное состояние, если объект существует
    if obj_name in state:
        state[obj_name] = new_state

    # Отправка команды на Arduino
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{ARDUINO_BASE_URL}/command", json={"cmd": cmd})
    except httpx.RequestError as e:
        print(f"[WARN] Не удалось отправить команду на Arduino: {e}")

    return {"ok": True, "object": obj_name, "state": new_state}

@router.get("/api/state")
async def handle_get_state():
    return state

@router.get("/api/files")
async def handle_list_files():
    try:
        files = [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith((".mp3", ".wav"))]
        return files
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/api/midi")
async def handle_send_midi(request: Request):
    body = await request.json()
    msg = body.get("msg")
    try:
        send_midi(msg)
        return {"ok": True}
    except Exception as e:
        return JSONResponse(status_code=502, content={"error": str(e)})

@router.get("/api/subscribe")
async def sse_subscribe():
    async def event_generator():
        while True:
            await asyncio.sleep(2)
            yield f"data: {json.dumps(state)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# --- Основная страница ---
@router.get("/")
async def serve_index():
    index_path = os.path.join(TEMPLATE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return JSONResponse(status_code=404, content={"error": "index.html not found"})

