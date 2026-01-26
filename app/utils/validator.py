import re
from fastapi import HTTPException

# ---- Phone Validation ----
# Supports:
#  - Indian numbers
#  - International + country code
#  - 10 digit clean numbers
phone_pattern = re.compile(r"^(\+?\d{1,3}[- ]?)?\d{10}$")


def validate_phone(phone: str):
    if not phone_pattern.match(phone):
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number. Please enter a valid 10-digit number."
        )
    return phone


# ---- City Validation ----
def validate_city(city: str):
    if len(city.strip()) < 2:
        raise HTTPException(status_code=400, detail="City name is too short.")
    if not re.match("^[A-Za-z ]+$", city):
        raise HTTPException(status_code=400, detail="City name must contain only letters.")
    return city


# ---- Purpose Validation ----
def validate_purpose(purpose: str):
    if len(purpose.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please describe purpose properly.")
    return purpose


# ---- Email Validation (Optional Future) ----
email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def validate_email(email: str):
    if not email_pattern.match(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return email


# ---- Combined Lead Validator ----
def validate_lead(data: dict):
    validate_phone(data["phone"])
    validate_city(data["city"])
    validate_purpose(data["purpose"])
    return True
