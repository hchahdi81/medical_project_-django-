from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import DoctorRegistrationForm
from .models import Doctor, Patient
from django.contrib.auth.hashers import check_password
import base64
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import DoctorRegistrationForm
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes 
from .serializers import DoctorSerializer, PatientSerializer
import urllib.parse
from rest_framework.parsers import MultiPartParser, FormParser

def homepage(request):
    return render(request, 'homepage.html')


FASTAPI_URL = 'http://127.0.0.1:8002/add-signature/'  
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()  # Sauvegarder le médecin dans la base de données
            photo_path = doctor.image.path  # Chemin de la photo

            # Appeler FastAPI pour générer la signature
            try:
                # Envoyer la photo et l'email à FastAPI
                with open(photo_path, 'rb') as image_file:
                    response = requests.post(
                        FASTAPI_URL,  # URL de FastAPI pour ajouter une signature
                        files={'file': image_file},
                        data={'email': doctor.email}  # Envoi de l'email avec l'image
                    )
                if response.status_code != 200:
                    raise Exception("Erreur lors de la création de la signature faciale.")
                else:
                    # Signature faciale créée avec succès
                    messages.success(request, "Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.")
                    return redirect('login')  # Rediriger vers la page de connexion
            except Exception as e:
                # Afficher un message d'erreur si la requête à FastAPI échoue
                print(f"Erreur : {str(e)}")
                messages.error(request, "Une erreur est survenue lors de l'ajout de la signature faciale. Veuillez réessayer.")
                return redirect('register_doctor')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')  # Get the user type (doctor/patient)
        licence_number = request.POST.get('numero_licence')  # For doctor
        ramq_number = request.POST.get('ramq')  # For patient

        if user_type == 'doctor':
            # Authentication for doctors
            try:
                doctor = Doctor.objects.get(email=email)
                if check_password(password, doctor.password):
                    # Check licence number
                    if doctor.numero_licence == licence_number:
                        # Store information in session
                        request.session['user_email'] = doctor.email
                        request.session['user_type'] = 'doctor'
                        request.session['user_id'] = doctor.id
                        return redirect('face_id_capture')  # Redirect to face capture page
                    else:
                        messages.error(request, "Incorrect licence number for the doctor.")
                else:
                    messages.error(request, "Incorrect login credentials for the doctor.")
            except Doctor.DoesNotExist:
                messages.error(request, "Doctor not found. Please register first.")

        elif user_type == 'patient':
            # Authentication for patients
            try:
                patient = Patient.objects.get(email=email)
                if check_password(password, patient.password):
                    # Check RAMQ number
                    if patient.ramq == ramq_number:
                        # Store information in session
                        request.session['user_email'] = patient.email
                        request.session['user_type'] = 'patient'
                        request.session['user_id'] = patient.id
                        return redirect('face_id_capture')  # Redirect to face capture page
                    else:
                        messages.error(request, "Incorrect RAMQ number for the patient.")
                else:
                    messages.error(request, "Incorrect login credentials for the patient.")
            except Patient.DoesNotExist:
                messages.error(request, "Patient not found. Please register first.")
        else:
            messages.error(request, "Please select Doctor or Patient.")

    return render(request, 'login.html')



def get_stored_image(request, email):
    try:
        # Fetch the doctor object based on the email
        doctor = Doctor.objects.get(email=email)
        if doctor.image:
            # Return the relative path to the image (e.g., 'image_doctors/Hamzi_AQge74n.jpg')
            return JsonResponse({"image_path": doctor.image.url}, status=200)
        else:
            return JsonResponse({"error": "No image found for this user"}, status=404)
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

def list_doctors(request):
    # Récupérer tous les médecins depuis la base de données
    doctors = Doctor.objects.all()
    return render(request, 'list_doctors.html', {'doctors': doctors})


def face_id_capture(request):
    return render(request, 'face_id_capture.html')


def verify_face_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        face_image_file = request.FILES.get('face_image')

        if not face_image_file:
            messages.error(request, "No image received.")
            return redirect('face_id_capture')

        try:
            # Create formData object and send the image as a file
            files = {'file': face_image_file}
            data = {'email': email}

            # Send the request to FastAPI
            response = requests.post('http://127.0.0.1:8002/verify-face-id/', files=files, data=data)

            if response.status_code == 200:
                # Encode l'email avant de l'ajouter à l'URL
                encoded_email = urllib.parse.quote(email)
                # Rediriger avec l'email encodé dans l'URL
                messages.success(request, "Face ID verified successfully.")
                return redirect(f'http://127.0.0.1:8001/records/?email={encoded_email}')

            else:
                messages.error(request, "Face ID did not match.")
                return redirect('face_id_capture')

        except Exception as e:
            messages.error(request, f"Verification error: {e}")
            return redirect('face_id_capture')

    return redirect('login')



@api_view(['GET'])
def get_doctor_by_email(request, email):
    decoded_email = urllib.parse.unquote(email)  
    print(f"Requête reçue pour l'email encodé : {email}")
    print(f"Email décodé : {decoded_email}")

    try:
        doctor = Doctor.objects.get(email=decoded_email)
        print(f"Docteur trouvé : {doctor}")
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    except Doctor.DoesNotExist:
        print(f"Docteur non trouvé pour l'email : {decoded_email}")
        return Response({'error': 'Doctor not found'}, status=404)


@api_view(['GET'])
def get_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_patient_by_id(request, id):
    try:
        patient = Patient.objects.get(id=id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=404)

@api_view(['GET'])
def get_doctor_by_id(request, id):
    try:
        doctor = Doctor.objects.get(id=id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=404)
    

@api_view(['GET'])
def get_patient_by_email(request, email):
    try:
        patient = Patient.objects.get(email=email)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=404)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  
def create_patient(request):
    serializer = PatientSerializer(data=request.data)
    
    if serializer.is_valid():
        patient = serializer.save()
        return Response({'id': patient.id}, status=201)
    else:
        return Response(serializer.errors, status=400)