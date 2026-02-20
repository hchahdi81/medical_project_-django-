import os
import numpy as np
import face_recognition
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image

app = FastAPI()

# Chemin pour les signatures
SIGNATURES_PATH = 'Signatures.npy'
PATIENT_SIGNATURES_PATH='PatientSignatures.npy'

# Répertoire pour stocker temporairement les images capturées
UPLOAD_DIR = r"C:\Users\hatim\Desktop\2024\Automne\Documentation\medical_project(final)\medical_project\medical_project\uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Charger ou créer les signatures
if os.path.exists(SIGNATURES_PATH):
    signatures = np.load(SIGNATURES_PATH, allow_pickle=True)
else:
    signatures = np.empty((0, 129))  # 128 pour l'encodage et 1 pour l'email


@app.post("/add-signature/")
async def add_signature(file: UploadFile = File(...), email: str = Form(...)):
    try:
        # Charger l'image téléchargée et l'encoder
        img = face_recognition.load_image_file(file.file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) == 0:
            raise HTTPException(status_code=400, detail="Aucun visage détecté sur la photo.")

        # Récupérer le premier encodage
        encoding = encodings[0].tolist()
        encoding.append(email)  # Ajouter l'email au lieu du nom de la photo

        # Ajouter cette nouvelle signature aux signatures existantes
        global signatures
        signatures = np.vstack([signatures, encoding])

        # Sauvegarder les signatures mises à jour dans le fichier
        np.save(SIGNATURES_PATH, signatures)
        return {"message": f"Signature faciale ajoutée avec succès pour l'email : {email}."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la signature : {str(e)}")


@app.post("/verify-face-id/")
async def verify_face_id(email: str = Form(...), file: UploadFile = File(...)):
    try:
        print(f"Email reçu: {email}")
        
        # Charger l'image capturée et l'encoder
        img = face_recognition.load_image_file(file.file)
        encodesCurrent = face_recognition.face_encodings(img)

        if len(encodesCurrent) == 0:
            raise HTTPException(status_code=400, detail="Aucun visage détecté sur la photo.")

        print("Image capturée encodée avec succès.")

        # Charger les signatures
        global signatures
        if os.path.exists(SIGNATURES_PATH):
            signatures = np.load(SIGNATURES_PATH, allow_pickle=True)
            print("Signatures chargées avec succès.")
        else:
            raise HTTPException(status_code=500, detail="Pas de signatures disponibles.")

        # Trouver la signature correspondant à l'email du médecin
        for signature in signatures:
            stored_email = signature[-1]
            print(f"Vérification de la signature pour l'utilisateur avec l'email : {stored_email}")
            if stored_email == email:  # On vérifie si l'email correspond
                encoding = signature[:-1].astype('float')  # Récupérer l'encodage facial

                # Comparer avec l'encodage de l'image capturée
                matches = face_recognition.compare_faces([encoding], encodesCurrent[0])
                face_distance = face_recognition.face_distance([encoding], encodesCurrent[0])

                print(f"Distance faciale : {face_distance[0]}")

                if matches[0] and face_distance[0] < 0.5:  # Comparaison réussie
                    return {"message": "Double authentification réussie."}
                else:
                    raise HTTPException(status_code=401, detail=f"Authentification échouée : distance faciale trop élevée ({face_distance[0]}).")

        raise HTTPException(status_code=400, detail="Utilisateur non trouvé ou signature non correspondante.")

    except Exception as e:
        print(f"Erreur lors de la vérification : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification : {str(e)}")


@app.post("/add-patient-signature/")
async def add_patient_signature(file: UploadFile = File(...), email: str = Form(...)):
    try:
        # Charger l'image téléchargée et l'encoder
        img = face_recognition.load_image_file(file.file)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) == 0:
            raise HTTPException(status_code=400, detail="Aucun visage détecté sur la photo.")

        # Récupérer le premier encodage
        encoding = encodings[0].tolist()
        encoding.append(email)  # Ajouter l'email au lieu du nom de la photo

        # Ajouter cette nouvelle signature aux signatures existantes
        global patient_signatures
        patient_signatures = np.vstack([patient_signatures, encoding])

        # Sauvegarder les signatures mises à jour dans le fichier
        np.save(PATIENT_SIGNATURES_PATH, patient_signatures)
        return {"message": f"Signature faciale ajoutée avec succès pour l'email : {email}."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la signature faciale : {str(e)}")