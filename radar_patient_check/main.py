import os
from datetime import date
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from ukrdc_sqla.ukrdc import Patient, PatientNumber, ProgramMembership

from radar_patient_check.database import ukrdc_engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def api_key_auth(request_key: str = Depends(oauth2_scheme)):
    api_keys = os.getenv("APIKEYS")
    if request_key not in api_keys:
        raise HTTPException(status_code=401, detail="Forbidden")


@app.get("/radar_check/", dependencies=[Depends(api_key_auth)])
async def radar_check(nhs_number: str, dob: date) -> Dict[bool, bool]:
    """
    checks to see if an NHS number is linked to a Radar membership and if the dob provided
    matches that on file. Can return true for the NHS number and false for the dob.

    Args:
        nhs_number (str): supplied NHS number
        dob (date): supplied DoB format YYYY-MM-DD

    Returns:
        Dict[bool, bool]: 1st true if membership exists 1nd true if dob matches
    """
    response = {"nhs_number": False, "dob": False}
    with Session(ukrdc_engine) as session:
        if (
            patient_numbers := session.query(PatientNumber)
            .filter_by(patientid=nhs_number, numbertype="NI")
            .all()
        ):
            pids = [patient_number.pid for patient_number in patient_numbers]

            if membership := (
                session.query(ProgramMembership)
                .filter(
                    ProgramMembership.pid.in_(pids),
                    ProgramMembership.program_name == "RADAR",
                    ProgramMembership.to_time == None,
                )
                .first()
            ):
                response["nhs_number"] = True

                recorded_dobs = (
                    session.query(Patient.birth_time)
                    .filter(Patient.pid.in_(pids))
                    .all()
                )

                recorded_dobs = [
                    recorded_dob.birth_time.date() for recorded_dob in recorded_dobs
                ]

                response["dob"] = dob in recorded_dobs
        return response
