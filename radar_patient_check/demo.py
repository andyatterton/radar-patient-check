import datetime
from dataclasses import dataclass


@dataclass
class DemoPatientDetails:
    date_of_birth: datetime.date
    is_radar_member: bool

check_digit_weights = {0: 10, 1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2}

def calculate_check_digit(nhs_number: str) -> int:
    """Given the first 9 or 10 digits of a 10-digit NHS number, calculate the check digit.

    Returns:
        int: The check digit.
             Note that this function may return 10, in which case the NHS number is invalid.

    """

    products = [int(nhs_number[i]) * check_digit_weights[i] for i in range(9)]
    sum_products = sum(products)
    remainder = sum_products % 11
    eleven_minus_remainder = 11 - remainder

    if eleven_minus_remainder == 11:
        return 0

    return eleven_minus_remainder

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
    # New test patients added 2023-07-27 at request of Steve Donovan
    "9686368450": DemoPatientDetails(
        date_of_birth=datetime.date(1954, 6, 14), is_radar_member=True
    ),
    "9686368469": DemoPatientDetails(
        date_of_birth=datetime.date(1955, 8, 26), is_radar_member=True
    ),
    "9686368477": DemoPatientDetails(
        date_of_birth=datetime.date(1958, 4, 6), is_radar_member=True
    ),
    "9686368485": DemoPatientDetails(
        date_of_birth=datetime.date(1957, 9, 9), is_radar_member=True
    ),
    "9686368604": DemoPatientDetails(
        date_of_birth=datetime.date(1985, 5, 17), is_radar_member=True
    ),
    "9686368620": DemoPatientDetails(
        date_of_birth=datetime.date(1975, 3, 8), is_radar_member=True
    ),
    # New test patient added 2024-02-19 at request of Steve Donovan
    "9990568847": DemoPatientDetails(
        date_of_birth=datetime.date(1992, 7, 7), is_radar_member=True
    ),
}

for i in range(999000001, 999000011):
    """
    Create extra test patients:
        9990000018: 1972-01-15
        9990000026: 1972-01-16
        9990000034: 1972-01-17
        9990000042: 1972-01-18
        9990000050: 1972-01-19
        9990000069: 1972-01-20
        9990000077: 1972-01-21
        9990000085: 1972-01-22
        9990000093: 1972-01-23
        9990000107: 1972-01-24
    """
    nhs_number_pre = "{:09d}".format(i)
    nhs_number = nhs_number_pre + str(calculate_check_digit(nhs_number_pre))
    date_of_birth = datetime.date(1972, 1, i%31)

    DEMO_PATIENTS_MAP[nhs_number] = DemoPatientDetails(
        date_of_birth=date_of_birth,
        is_radar_member=True
    )
