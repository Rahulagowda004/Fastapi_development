from fastapi import FastAPI, HTTPException, Path
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

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    data = get_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')
