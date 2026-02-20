from django.db import models

class MedicalRecord(models.Model):
    patient = models.ForeignKey('auth_app.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('auth_app.Doctor', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    diagnostic = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)  
    follow_up_date = models.DateField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dossier médical de {self.patient} par {self.doctor} le {self.created_at}"
