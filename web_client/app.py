from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="web_client/templates")

API_URL = "https://shl-assessment-api-21yg.onrender.com/recommend"

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
def search(request: Request, query: str = Form(...)):
    response = requests.post(API_URL, json={"query": query})
    results = response.json()["recommendations"]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
            "query": query
        }
    )
