from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from analyzer import analyze_screenshot

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>XtremeReversal Analyzer</h2>
    <form action='/analyze' enctype='multipart/form-data' method='post'>
        <input name='file' type='file'>
        <input type='submit' value='Analyze'>
    </form>
    """

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_screenshot(file)
    return {"signal": result}