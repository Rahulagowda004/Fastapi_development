from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated, Optional

class Patient(BaseModel):
    id : Annotated[str,Field(..., description="Unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(...,description="Full name of the patient", example="John Doe")]
    age: Annotated[int, Field(..., description="Age of the patient", example=30, ge=0)]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="Gender of the patient", example="male")]
    city: Annotated[str, Field(..., description="City of residence", example="New York")]
    height: Annotated[float, Field(..., description="Height in centimeters", example=175.5, gt=0)]
    weight: Annotated[float, Field(..., description="Weight in kilograms", example=70.0, gt=0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
class Patient_update(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Full name of the patient", example="John Doe")] = None
    age: Annotated[Optional[int], Field(None, description="Age of the patient", example=30, ge=0)] = None
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(None, description="Gender of the patient", example="male")] = None
    city: Annotated[Optional[str], Field(None, description="City of residence", example="New York")] = None
    height: Annotated[Optional[float], Field(None, description="Height in centimeters", example=175.5, gt=0)] = None
    weight: Annotated[Optional[float], Field(None, description="Weight in kilograms", example=70.0, gt=0)] = None