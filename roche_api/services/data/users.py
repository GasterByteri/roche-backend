from roche_api import constants as api_constants
from roche_api.models import users as user_models


def create_user_profile(request_post: dict) -> None:
    if request_post.get("role") == api_constants.PATIENT:
        patient = user_models.Patient(
            municipality=request_post.get("municipality", ""),
            medical_record_number=request_post.get("medical_record_number", ""),
            diagnosis=request_post.get("diagnosis", ""),
        )
        return patient

    elif request_post.get("role") == api_constants.DOCTOR:
        doctor = user_models.Doctor(
            employee_number=request_post.get("employee_number", ""),
            department=request_post.get("department", ""),
            title=request_post.get("title", ""),
            room_number=request_post.get("room_number"),
            hospital=request_post.get("hospital", ""),
            city=request_post.get("city", ""),
        )
        return doctor


def get_user_data(request_post: dict) -> dict:
    return {
        "username": request_post.get("username", ""),
        "email": request_post.get("department", ""),
        "password": request_post.get("password", ""),
        "first_name": request_post.get("first_name"),
        "last_name": request_post.get("last_name", ""),
        "sex": request_post.get("sex", ""),
        "role": request_post.get("role"),
        "birth_date": request_post.get("birth_date", ""),
        "phone_number": request_post.get("phone_number", ""),
    }


def get_doctor_data(request_post: dict) -> dict:
    return {
        "employee_number" : request_post.get("employee_number", ""),
        "department" : request_post.get("department", ""),
        "title" : request_post.get("title", ""),
        "room_number" : request_post.get("room_number"),
        "hospital" : request_post.get("hospital", ""),
        "city" : request_post.get("city", ""),
    }


def get_patient_data(request_post: dict) -> dict:
    return {
        "municipality" : request_post.get("municipality", ""),
        "medical_record_number" : request_post.get("medical_record_number", ""),
        "diagnosis" : request_post.get("diagnosis", ""),
    }