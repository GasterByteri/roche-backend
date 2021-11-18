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