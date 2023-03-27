from dataclasses import dataclass
import datetime


@dataclass
class DemoPatientDetails:
    date_of_birth: datetime.date
    is_radar_member: bool


DEMO_PATIENTS_MAP = {
    "9686368973": DemoPatientDetails(
        date_of_birth=datetime.date(1968, 2, 12), is_radar_member=True
    ),
    "9686368906": DemoPatientDetails(
        date_of_birth=datetime.date(1942, 2, 1), is_radar_member=True
    ),
    "9658218873": DemoPatientDetails(
        date_of_birth=datetime.date(1927, 6, 19), is_radar_member=True
    ),
    "9661034524": DemoPatientDetails(
        date_of_birth=datetime.date(1992, 10, 22), is_radar_member=True
    ),
    # "9658218881": DemoPatientDetails(
    #     date_of_birth=datetime.date(1921, 8, 8), is_radar_member=True
    # ),
    # Deliberately wrong date of birth, to test the radar_check endpoint when using NHS login
    "9658218881": DemoPatientDetails(
        date_of_birth=datetime.date(1920, 8, 8), is_radar_member=True
    ),
}
