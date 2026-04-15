from fastapi import FastAPI #library and important parameters
from pydantic import BaseModel, field_validator #for data validation
from typing import Optional #used to add descriptions
from enum import Enum # creates set of symptoms
import datetime

class Symptom(str, Enum):
    FATIGUE = "fatigue"
    JOINT_PAIN = "joint_pain"
    DIGESTION_ISSUES = "digestion_issues"
    HEADACHE = "headache"
    ANXIETY = "anxiety"
    SKIN_ISSUES = "skin_issues"
    COLD_INTOLERANCE = "cold_intolerance"
    UNSTEADY_FEVER = "unsteady_fever"
    MUSCLE_ISSUES = "muscle_issues"
    HEAT = "heat"
    LOSS_OF_APPETITE = "loss_of_appetite"
    SHORTNESS_OF_BREATH = "shortness_of_breath"
    BRAIN_FOG = "brain_fog"


class DailyLog(BaseModel):
    date: Optional[datetime.date]
    symptom: list[Symptom]
    severity: int
    sleep_hours: float
    energy_level: int

    @field_validator('severity')
    @classmethod
    def severity_must_be_valid(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Severity level must be on scale between 1 and 10')
        return v
    
    @field_validator('sleep_hours')
    @classmethod
    def sleep_must_be_valid(cls, s):
        if not 1 <= s <= 24:
            raise ValueError('Hours of sleep must be less than a day')
        return s
    
    @field_validator('energy_level')
    @classmethod
    def energy_must_be_valid(cls, e):
        if not 1 <= e <= 10:
            raise ValueError("Energy level must be on a scale between 1 and 10")
        return e




app = FastAPI()
symptoms = []
#homepage:
@app.get("/")

def hello():
    return {"message": "symptom management system api"}

# creating an endpoint as "view" where all the data shows up
# when a user accesses https://{url}/view API will display records

# placing food order; can update model; automatic JSON parsing/validation
@app.post("/symptom", response_model=DailyLog) 
async def track_symptom(symptom: DailyLog):
    symptoms.append(symptom)
    return symptom

# decorator defines endpoint (asking to see menu)
# can return HTTP exceptions 
# (e.g. warning that item doesn't exist, success placing item)
@app.get("/symptom", response_model=list[DailyLog])
async def get_all_symptoms():
    return symptoms
