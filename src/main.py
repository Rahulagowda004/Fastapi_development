from fastapi import FastAPI
from .utils.utils import get_data

app = FastAPI()

@app.get("/")
async def homepage():
    return {"message": "Hello, this is the clinic!"}

@app.get("/about")
async def about():
    return {"message": "This page handles everything related to the clinic."}

@app.get("/view")
async def view_patients():
    data = get_data()
    return {"patients": data}