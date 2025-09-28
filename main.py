import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from handlers import router

app = FastAPI()

# --- Подключаем API-роуты ---
app.include_router(router)

# --- Раздача статики ---
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

