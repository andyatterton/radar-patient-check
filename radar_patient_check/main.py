import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from ukrdc_sqla.ukrdc import PatientNumber, ProgramMembership

from radar_patient_check.database import ukrdc_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def api_key_auth(request_key: str = Depends(oauth2_scheme)):
    api_keys = os.getenv("APIKEYS")
    if request_key not in api_keys:
        raise HTTPException(status_code=401, detail="Forbidden")


@app.get("/radar_check/{nhs_number}", dependencies=[Depends(api_key_auth)])
async def radar_check(nhs_number: str) -> bool:
    """
    checks to see if an NHS number is linked to a Radar membership

    Args:
        nhs_number (str): supplied NHS number

    Returns:
        bool: true if membership exists otherwise false
    """
    with Session(ukrdc_engine) as session:
        if (
            patient_numbers := session.query(PatientNumber)
            .filter_by(patientid=nhs_number)
            .all()
        ):
            pids = [patient_number.pid for patient_number in patient_numbers]
            if (
                membership := session.query(ProgramMembership)
                .filter(
                    ProgramMembership.pid.in_(pids),
                    ProgramMembership.program_name == "RADAR",
                    ProgramMembership.to_time == None,
                )
                .first()
            ):
                return bool(membership)
        return False
