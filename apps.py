# apps.py de medical_records_app
from django.apps import AppConfig

class MedicalRecordsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical_records_app'  # Assure-toi que ce nom est unique dans l'ensemble de tes projets
