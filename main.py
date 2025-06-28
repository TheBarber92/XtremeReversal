from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
import os
import pytesseract
from PIL import Image

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, file: UploadFile = File(...)):
    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(file_path)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result
    })

def analyze_image(file_path):
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img).lower()
        if "trigger base sell" in text:
            return "SELL Signal (Confirmed)"
        elif "trigger base buy" in text:
            return "BUY Signal (Confirmed)"
        elif "reversal buffer" in text:
            return "Setup Forming (Reversal Buffer)"
        elif "m4" in text or "ema4" in text:
            return "Setup Forming"
        else:
            return "Invalid Setup"
    except Exception as e:
        return f"Error analyzing image: {e}"