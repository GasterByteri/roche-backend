import random

from django.core.management.base import BaseCommand
from roche_api.models import users as user_models


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--force', type=bool, help="Mode")

    def handle(self, *args, **options):
        self.run_seed_db(options['force'])

    @staticmethod
    def run_seed_db(mode):
        if mode:
            user_models.User.objects.all().delete()
            user_models.Patient.objects.all().delete()
            user_models.Doctor.objects.all().delete()
            user_models.PatientDoctorMembership.objects.all().delete()
        Command._seed_db()

    @staticmethod
    def _seed_db():
        user_1 = user_models.User(
            role="patient",
            phone_number="067832032",
            sex="F",
            birth_date="1995-10-25",
            first_name="Petra",
            last_name="Petrovic",
            username="petra",
            email="petra@gmail.com"
        )
        user_1.set_password("petra12345")
        user_1.save()

        user_2 = user_models.User(
            role="patient",
            phone_number="0678324332",
            sex="F",
            birth_date="1985-11-25",
            first_name="F2",
            last_name="L2",
            username="F2L2",
            email="f2l2@gmail.com"
        )
        user_2.save()

        user_3 = user_models.User(
            role="patient",
            phone_number="064832052",
            sex="F",
            birth_date="1964-10-25",
            first_name="F3",
            last_name="L3",
            username="F3L3",
            email="f3l3@gmail.com"
        )
        user_3.save()

        patient_1 = user_models.Patient(
            municipality="Podgorica",
            medical_record_number="3234343",
            diagnosis="cancer",
            user=user_1,
        )
        patient_1.save()

        patient_2 = user_models.Patient(
            municipality="Podgorica",
            medical_record_number="3754343",
            diagnosis="cancer",
            user=user_2,
        )
        patient_2.save()

        patient_3 = user_models.Patient(
            municipality="Bar",
            medical_record_number="76438",
            diagnosis="cancer",
            user=user_3,
        )
        patient_3.save()

        user_4 = user_models.User(
            role="doctor",
            phone_number="067832032",
            sex="M",
            birth_date="1965-10-25",
            first_name="Petar",
            last_name="Petrovic",
            username="petar",
            email="petar@gmail.com"
        )
        user_4.set_password("petar12345")
        user_4.save()

        user_5 = user_models.User(
            role="doctor",
            phone_number="06435424332",
            sex="M",
            birth_date="1965-11-25",
            first_name="D2",
            last_name="D2",
            username="D2L2",
            email="d2l2@gmail.com"
        )
        user_5.save()

        doctor_1 = user_models.Doctor(
            employee_number="4367643",
            department="onkologija",
            title="DR",
            room_number="327632",
            hospital="JZU",
            city="Podgorica",
            user=user_4,
        )
        doctor_1.save()

        doctor_2 = user_models.Doctor(
            employee_number="43343643",
            department="onkologija",
            title="DR",
            room_number="45",
            hospital="JZU",
            city="Podgorica",
            user=user_5,
        )
        doctor_2.save()
        doctor_2.patients.set([patient_1, patient_2])

        patient_doctor_1 = user_models.PatientDoctorMembership(
            patient=patient_3,
            doctor=doctor_2,
            mainDoctor=False,
        )
        patient_doctor_1.save()

        patient_doctor_2 = user_models.PatientDoctorMembership(
            patient=patient_3,
            doctor=doctor_1,
            mainDoctor=True,
        )
        patient_doctor_2.save()

        admin_1 = user_models.User(
            role="admin",
            phone_number="0678324332",
            sex="F",
            birth_date="1985-11-25",
            first_name="Admin",
            last_name="Admin",
            username="admin",
            email="admin@gmail.com"
        )
        admin_1.set_password("admin12345")
        admin_1.save()
