from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalRecord
from .forms import MedicalRecordForm
from django.contrib import messages
import requests


def homepage(request):
    return render(request, 'base.html')

def get_doctor_data(request):
    """
    Vérifie si le docteur est connecté et retourne ses données.
    Si le docteur n'est pas trouvé ou l'email est vide, redirige vers la page de connexion.
    """
    email = request.GET.get('email') or request.session.get('doctor_email')

    if email:
        api_url = f'http://127.0.0.1:8000/auth/api/doctor/{email}/'
        response = requests.get(api_url)

        if response.status_code == 200:
            request.session['doctor_email'] = email
            return response.json()
        else:
            return None
    return None

def doctor_medical_record_list(request):
    doctor_data = get_doctor_data(request)
    
    if not doctor_data:
        messages.error(request, "Veuillez vous connecter.")
        return redirect('http://127.0.0.1:8000/auth/login/')

    doctor_id = doctor_data.get('id')
    records = MedicalRecord.objects.filter(doctor_id=doctor_id)

    context = {
        'records': records,
        'doctor_name': f"{doctor_data.get('nom')} {doctor_data.get('prenom')}",
    }
    return render(request, 'doctor_record_list.html', context)


FASTAPI_PATIENT_SIGNATURE_URL = "http://127.0.0.1:8002/add-patient-signature/"  # URL for FastAPI to add patient signature

def create_medical_record(request):
    doctor_data = get_doctor_data(request)

    if not doctor_data:
        messages.error(request, "Veuillez vous connecter.")
        return redirect('http://127.0.0.1:8000/auth/login/')

    doctor_id = doctor_data.get('id')

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        
        print("Form data:", request.POST)
        print("Files data:", request.FILES)

        if form.is_valid():
            medical_record = form.save(commit=False)

            # Collect patient data
            patient_email = form.cleaned_data.get('patient_email')
            patient_image = form.cleaned_data.get('patient_image')

            # Create patient and check response
            create_patient_response = requests.post(
                'http://localhost:8000/auth/api/patients/create',
                data={
                    'email': patient_email,
                    'nom': form.cleaned_data.get('patient_nom'),
                    'prenom': form.cleaned_data.get('patient_prenom'),
                    'ramq': form.cleaned_data.get('patient_ramq'),
                    'password': form.cleaned_data.get('patient_password'),
                },
                files={'image': patient_image}
            )
            
            if create_patient_response.status_code == 201:
                patient_id = create_patient_response.json()['id']
                medical_record.patient_id = patient_id
                medical_record.doctor_id = doctor_id

                # Now we generate the patient's facial signature
                if patient_image:
                    try:
                        response = requests.post(
                            FASTAPI_PATIENT_SIGNATURE_URL,  # URL de FastAPI pour ajouter une signature
                            files={'file': patient_image},  # Utiliser le fichier d'image directement
                            data={'email': patient_email}  # Envoi de l'email avec l'image
                        )
                        if response.status_code != 200:
                            raise Exception("Erreur lors de la création de la signature faciale.")
                        else:
                            messages.success(request, "Dossier médical et signature faciale créés avec succès !")
                    except Exception as e:
                        print(f"Erreur lors de la création de la signature : {str(e)}")
                        messages.error(request, "Une erreur est survenue lors de l'ajout de la signature faciale. Veuillez réessayer.")
                
                medical_record.save()
                messages.success(request, "Dossier médical créé avec succès !")
                return redirect('doctor_medical_record_list')
            else:
                messages.error(request, "Erreur lors de la création du patient.")
                return redirect('create_medical_record')
    else:
        form = MedicalRecordForm()

    context = {
        'form': form,
    }

    return render(request, 'create_record.html', context)



def medical_record_detail(request, record_id):
    doctor_data = get_doctor_data(request)

    if not doctor_data:
        messages.error(request, "Veuillez vous connecter.")
        return redirect('http://127.0.0.1:8000/auth/login/')

    doctor_id = doctor_data.get('id')
    record = get_object_or_404(MedicalRecord, id=record_id, doctor_id=doctor_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Dossier médical mis à jour avec succès !")
            return redirect('doctor_medical_record_list')
    else:
        form = MedicalRecordForm(instance=record)
    
    context = {
        'form': form,
        'record': record,
        'doctor_name': f"{doctor_data.get('nom')} {doctor_data.get('prenom')}"
    }
    
    return render(request, 'record_detail.html', context)

def delete_medical_record(request, record_id):
    doctor_data = get_doctor_data(request)

    if not doctor_data:
        messages.error(request, "Veuillez vous connecter.")
        return redirect('http://127.0.0.1:8000/auth/login/')

    doctor_id = doctor_data.get('id')
    record = get_object_or_404(MedicalRecord, id=record_id, doctor_id=doctor_id)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Dossier médical supprimé avec succès !")
        return redirect('doctor_medical_record_list')
    
    context = {
        'record': record,
        'doctor_name': f"{doctor_data.get('nom')} {doctor_data.get('prenom')}"
    }
    
    return render(request, 'confirm_delete.html', context)
