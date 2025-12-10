from ast import main
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from .utils.utils import get_data, save_data
from .schema.patients import Patient, Patient_update

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

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="sort based on the height, weight or bmi", example="weight"), order: str = Query("asc", description="order can be asc or desc", example="asc")):
    data = get_data()
    if sort_by not in ["height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail="Invalid sort parameter.")
    sorted_patients = sorted(data.items(), key=lambda item: item[1].get(sort_by))
    if order == "desc":
        sorted_patients.reverse()
    return {"patients": sorted_patients}

@app.put("/update/{patient_id}")
def update_patient(patient_id: str = Path(..., description="ID of the patient to update", example="P001"), patient_update: Patient_update = ...):
    data = get_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str = Path(...,description="enter id of the patient to delete",example='P001')):
    data = get_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=400, content="patient doesn't exist in the database")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content = {"message":"patient deletes successfully"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)