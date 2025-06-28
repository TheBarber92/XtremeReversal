from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import init_db, has_access, increment_upload
import shutil
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    if not has_access(user_id):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Upload limit reached. Please complete payment to continue.",
        })

    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    increment_upload(user_id)
    result = "Setup Forming"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "user_id": user_id
    })