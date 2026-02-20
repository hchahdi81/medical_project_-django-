import os
import cv2
import numpy as np
import face_recognition

# Répertoires où sont stockées les images
doctors_path = r"C:\Users\hatim\Desktop\2024\Automne\Documentation\medical_project(final)\medical_project\medical_project\medical_application\media\image_doctors"
patients_path = r"C:\Users\hatim\Desktop\2024\Automne\Documentation\medical_project(final)\medical_project\medical_project\medical_application\media\image_patients\image_patients"

images_list_doctors = []
emails_doctors = []
images_list_patients = []
emails_patients = []

# Fonction pour obtenir l'email à partir du nom de fichier
def get_email_from_filename(filename):
    # Extraire la partie sans l'extension
    name = filename.split('.')[0]
    
    # Remplacer le premier '_' par '@' et le deuxième '_' par '.'
    parts = name.split('_', 2)  # Limiter à 2 séparations (nom@domaine.extension)
    if len(parts) >= 3:
        email = f'{parts[0]}@{parts[1]}.{parts[2]}'
    else:
        email = name  # Si le format ne correspond pas, on garde le nom tel quel

    return email

# Charger les images des médecins et extraire les emails correspondants
myList_doctors = os.listdir(doctors_path)

for img_name in myList_doctors:
    if img_name.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.tiff')):
        curImg = cv2.imread(os.path.join(doctors_path, img_name))
        images_list_doctors.append(curImg)
        
        # Récupérer l'email correspondant au nom de l'image
        email = get_email_from_filename(img_name)
        emails_doctors.append(email)

# Fonction pour extraire les caractéristiques faciales
def extractFaceFeatures(Images, emails, signature_file):
    features = []
    count = 1
    for image, email in zip(Images, emails):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        feature = face_recognition.face_encodings(img)
        if len(feature) > 0:
            # Associer l'encodage à l'email et non au nom de l'image
            feature = feature[0].tolist() + [email]
            features.append(feature)
            print(f'{int((count / len(Images)) * 100)} % extracted')
        count += 1
    if features:
        array = np.array(features)
        np.save(signature_file, array)
        print(f'Signatures saved to {signature_file}!')
    else:
        print(f'Aucune signature à enregistrer.')

# Appeler la fonction pour extraire les caractéristiques faciales et les enregistrer avec les emails pour les médecins
extractFaceFeatures(images_list_doctors, emails_doctors, 'Signatures.npy')

# Charger les images des patients
print("Vérification des fichiers dans le dossier des patients:")
myList_patients = os.listdir(patients_path)

for img_name in myList_patients:
    print(img_name)  # Print the filenames
    if img_name.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.tiff')):
        curImg = cv2.imread(os.path.join(patients_path, img_name))
        images_list_patients.append(curImg)
        
        # Récupérer l'email correspondant au nom de l'image
        email = get_email_from_filename(img_name)
        emails_patients.append(email)

# Appeler la fonction pour extraire les caractéristiques faciales et les enregistrer avec les emails pour les patients
extractFaceFeatures(images_list_patients, emails_patients, 'PatientSignatures.npy')
