import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from ukrdc_sqla.ukrdc import PatientNumber

from radar_patient_check.database import APIKeys, key_engine, ukrdc_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def api_key_auth(request: Request, request_key: str = Depends(oauth2_scheme)):
    request_ip = request.client.host
    with Session(key_engine) as session:
        api_key = session.query(APIKeys).filter_by(ip=request_ip).first()
    if api_key.key != request_key:
        raise HTTPException(status_code=401, detail="Forbidden")


@app.get("/radar_check/{nhs_number}", dependencies=[Depends(api_key_auth)])
async def radar_check(nhs_number: str):
    with Session(ukrdc_engine) as session:
        patient = session.query(PatientNumber).filter_by(patientid=nhs_number).first()
        return {nhs_number: bool(patient)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
