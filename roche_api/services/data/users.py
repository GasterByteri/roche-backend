from roche_api import constants as api_constants
from roche_api.models import users as user_models


def create_user_profile(request_post: dict) -> None:
    if request_post.get("role") == api_constants.PATIENT:
        patient_data = {
            "municipality" : request_post.get("municipality", ""),
            "medical_record_number" : request_post.get("medical_record_number", ""),
            "diagnosis" : request_post.get("diagnosis", ""),
        }
        patient = user_models.Patient(patient_data)
        return patient

    elif request_post.get("role") == api_constants.DOCTOR:
        doctor_data = {
                            "employee_number": request_post.get("employee_number", ""),
                            "department": request_post.get("department", ""),
                            "title": request_post.get("title", ""),
                            "room_number": request_post.get("room_number"),
                            "hospital": request_post.get("hospital", ""),
                            "city": request_post.get("city", ""),
                       }
        doctor = user_models.Doctor(doctor_data)
        return doctor