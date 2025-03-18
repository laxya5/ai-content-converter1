import os
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import (
    text_to_audio,
    text_to_image,
    create_video,
    process_audio_to_video,
    process_text_to_video
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def handle_conversion(
    request: Request,
    mode: str = Form(...),
    text: str = Form(None),
    file: UploadFile = Form(None)
):
    if mode == "text2audio":
        audio = text_to_audio(text)
        return {"type": "audio", "data": audio}
    
    if mode == "text2image":
        image = text_to_image(text)
        return {"type": "image", "data": image}
    
    if mode == "audio2video":
        video = await process_audio_to_video(file)
        return {"type": "video", "data": video}
    
    if mode == "text2video":
        video = process_text_to_video(text)
        return {"type": "video", "data": video}
