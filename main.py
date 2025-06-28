from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from auth import register_user, login_user, check_upload_limit, increment_uploads
from analyzer import analyze_screenshot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

sessions = {}

@app.get("/", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return """
    <h2>Login</h2>
    <form action='/login' method='post'>
        ID: <input type='text' name='id'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Login'>
    </form>
    <p>New user? <a href='/register'>Register here</a></p>
    """

@app.post("/login")
async def login(id: str = Form(...), password: str = Form(...)):
    if login_user(id, password):
        sessions[id] = True
        return RedirectResponse(url=f"/dashboard?id={id}", status_code=302)
    return HTMLResponse("<p>Login failed</p><a href='/login'>Try again</a>")

@app.get("/register", response_class=HTMLResponse)
async def register_page():
    return """
    <h2>Register</h2>
    <form action='/register' method='post'>
        ID: <input type='text' name='id'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Register'>
    </form>
    """

@app.post("/register")
async def register(id: str = Form(...), password: str = Form(...)):
    if register_user(id, password):
        return RedirectResponse(url="/login", status_code=302)
    return HTMLResponse("<p>ID already exists</p><a href='/register'>Try again</a>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(id: str):
    if id not in sessions:
        return RedirectResponse(url="/login")
    return HTMLResponse(f"""
    <h2>Welcome, {id}</h2>
    <form action='/analyze' enctype='multipart/form-data' method='post'>
        <input name='id' type='hidden' value='{id}'>
        <input name='file' type='file'><br>
        <input type='submit' value='Analyze Screenshot'>
    </form>
    """)

@app.post("/analyze")
async def analyze(id: str = Form(...), file: UploadFile = File(...)):
    if not check_upload_limit(id):
        return {"status": "Trial limit reached. Please upgrade to continue."}
    result = await analyze_screenshot(file)
    increment_uploads(id)
    return {"signal": result}