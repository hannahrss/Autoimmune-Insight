from fastapi import FastAPI #library and important parameters
from pydantic import BaseModel, field_validator #for data validation
from typing import Optional #used to add descriptions
import datetime

class UserSymptom(BaseModel):
    date: Optional[datetime.date]
    symptom: str | None = None
    severity: int
    sleep_hours: float
    energy_level: int

    @field_validator('severity')
    @classmethod
    def severity_must_be_valid(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Severity must be on scale between 1 and 10')
        return v
    
    @field_validator(sleep_hours)
    @classmethod
    def sleep_must_be_valid(cls, s):
        if not 1 <= s <= 24:
            raise ValueError('Hours of sleep must be less than a day')
        return s
    




app = FastAPI()
symptoms = []
#homepage:
@app.get("/")

def hello():
    return {"message": "symptom management system api"}

# creating an endpoint as "view" where all the data shows up
# when a user accesses https://{url}/view API will display records

# placing food order; can update model; automatic JSON parsing/validation
@app.post("/symptom", response_model=UserSymptom) 
async def track_symptom(symptom: UserSymptom):
    symptoms.append(symptom)
    return symptom

# decorator defines endpoint (asking to see menu)
# can return HTTP exceptions 
# (e.g. warning that item doesn't exist, success placing item)
@app.get("/symptom", response_model=list[UserSymptom])
async def get_all_symptoms():
    return symptoms
