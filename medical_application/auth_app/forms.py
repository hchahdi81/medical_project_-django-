from django import forms
from .models import Doctor
from django.core.exceptions import ValidationError

class DoctorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['nom', 'prenom', 'email', 'password', 'numero_licence', 'image']
    
    # Validation for unique email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Doctor.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    # Validation for unique licence number
    def clean_numero_licence(self):
        numero_licence = self.cleaned_data.get('numero_licence')
        if Doctor.objects.filter(numero_licence=numero_licence).exists():
            raise ValidationError("This licence number is already in use.")
        return numero_licence

    # Validation to ensure image is uploaded
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError("You must upload a profile image.")
        return image
