from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from .utils.utils import get_data, save_data
from .model.patients import Patient

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
    # **...** indicates mandatory field in the Path function.
    #Path function improves readability and documentation of the API.
    
    data = get_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.post("/create")
def create_patient(patient: Patient):
    data = get_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude="id")
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient created'})