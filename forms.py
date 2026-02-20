from django import forms
from .models import MedicalRecord
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
import requests

class MedicalRecordForm(forms.ModelForm):
    # Fields for creating a new patient
    patient_nom = forms.CharField(label="Nom du patient", max_length=100)
    patient_prenom = forms.CharField(label="Prénom du patient", max_length=100)
    patient_email = forms.EmailField(label="Email du patient")
    patient_ramq = forms.CharField(label="Numéro RAMQ du patient", max_length=50)
    patient_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe temporaire")
    patient_image = forms.ImageField(label="Image du patient", required=True)

    class Meta:
        model = MedicalRecord
        fields = ['description', 'diagnostic', 'patient_nom', 'patient_prenom', 'patient_email', 'patient_ramq', 'patient_password', 'patient_image']

    def save(self, commit=True):
        # On gère la création du patient dans la vue
        return super().save(commit=commit)
