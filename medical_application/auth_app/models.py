from django.db import models
from django.contrib.auth.hashers import make_password
import os




# Fonction pour gérer le téléchargement des images et nettoyer le nom du fichier
def upload_to(instance, filename):
    ext = filename.split('.')[-1]  # Extraire l'extension de l'image
    
    # Nettoyer l'email en remplaçant les caractères spéciaux
    safe_email = instance.email.replace('@', '_').replace('.', '_')
    
    # Renommer le fichier avec l'email nettoyé
    filename = f"{safe_email}.{ext}"  # Par exemple, lizahmz_gmail_com.jpg
    
    return os.path.join('image_doctors/', filename) 

class Doctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    numero_licence = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True) 

    def save(self, *args, **kwargs):
        if not self.id and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.numero_licence}"
    

def upload_to_patients(instance, filename):
    ext = filename.split('.')[-1]  # Extraire l'extension de l'image
    
    # Nettoyer l'email en remplaçant les caractères spéciaux
    safe_email = instance.email.replace('@', '_').replace('.', '_')
    
    # Renommer le fichier avec l'email nettoyé
    filename = f"{safe_email}.{ext}"  # Par exemple, lizahmz_gmail_com.jpg
    
    return os.path.join('image_patients/', filename) 


class Patient(models.Model):
    id = models.BigAutoField(primary_key=True)  
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    ramq = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to_patients, blank=True, null=True) 

    def save(self, *args, **kwargs):
        # Hacher le mot de passe uniquement si c'est un nouvel enregistrement
        if not self.id and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.ramq}"