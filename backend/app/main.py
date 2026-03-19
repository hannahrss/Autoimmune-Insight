from fastapi import FastAPI, Path, HTTPException, Query #library and important parameters
from pydantic import BaseModel, Field, computed_field #for data validation
from pydantic import Annotated, Literal, Optional #used to add descriptions
from fastapi.responses import JSONResponse
import datetime
import json

class UserSymptom(BaseModel):
    date: Annotated[Optional[datetime.date]]
    symptom: str | None = None
    severity: int
    description: str | None = None

app = FastAPI()
symptoms = []
#homepage:
@app.get("/")

def hello():
    return {"message": "symptom management system api"}

# creating an endpoint as "view" where all the data shows up
# when a user accesses https://{url}/view API will display records

@app.put("/symptom", response_model=UserSymptom)
async def track_symptom(symptom: UserSymptom):
    symptoms.append(symptom)
    return symptom

@app.get("/symptom", response_model=list[UserSymptom])
async def get_all_symptoms():
    return symptoms
