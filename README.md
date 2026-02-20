# 🏥 Plateforme de Gestion des Dossiers Médicaux avec Reconnaissance Faciale

## 📌 Présentation

Ce projet est une application web de gestion médicale développée avec **Django** et un **microservice de reconnaissance faciale** en Python.

Il permet aux médecins de créer et gérer les dossiers médicaux des patients tout en utilisant une technologie de reconnaissance faciale pour identifier les patients de manière sécurisée.

Ce système illustre une architecture réelle combinant un backend Django classique avec un service d’intelligence artificielle.

---

## 🚀 Fonctionnalités

* 🔐 Authentification des utilisateurs (connexion / déconnexion)
* 👨‍⚕️ Accès des médecins aux dossiers patients
* 🧾 Création et gestion des dossiers médicaux
* 🖼 Téléversement des images des patients
* 🤖 Génération de signatures faciales
* 🧠 Vérification par reconnaissance faciale via un service externe
* 📂 Stockage des photos patients

---

## 🏗 Technologies utilisées

### Backend

* Django (Python)
* SQLite (base par défaut)

### Microservice IA

* Python
* NumPy
* Génération personnalisée de signatures faciales

### Frontend

* Templates Django
* Bootstrap

---

## 📁 Structure du projet

```id="c9fd9f"
medical_project/
│── manage.py
│── medical_project/
│── medical_application/
│── templates/
│── static/

face_id_service/
│── app.py
│── signature.py
│── requirements.txt
```

---

## ⚙️ Installation

### 1️⃣ Cloner le dépôt

```id="du1oij"
git clone <url-du-repo>
cd medical_project
```

---

### 2️⃣ Créer un environnement virtuel

```id="ddpj9r"
python -m venv venv
```

Activation Windows :

```id="3ujqau"
venv\Scripts\activate
```

Activation Mac/Linux :

```id="edmli2"
source venv/bin/activate
```

---

### 3️⃣ Installer les dépendances

```id="7sw0t5"
pip install -r requirements.txt
```

---

### 4️⃣ Appliquer les migrations

```id="fbpf3a"
python manage.py migrate
```

---

### 5️⃣ Lancer le serveur Django

```id="h06f7m"
python manage.py runserver
```

Ouvrir :

```id="60y3xk"
http://127.0.0.1:8000/
```

---

## 🤖 Lancer le service de reconnaissance faciale

Se placer dans le dossier :

```id="p7f7yx"
cd face_id_service
pip install -r requirements.txt
python app.py
```

Assurez-vous que ce service fonctionne avant d’utiliser la vérification faciale.

---

## 📸 Captures d’écran

*(Ajoutez ici des captures de la page login, tableau de bord, création dossier, etc.)*

---

## 🎯 Objectif du projet

Ce projet a été développé dans un but pédagogique et de portfolio afin de démontrer :

* le développement backend avec Django
* la simulation d’un workflow médical réel
* une architecture microservices
* l’intégration de l’intelligence artificielle dans une application web

---

## 👨‍💻 Auteur

**Hatim Chahdi**
Développeur Python / Django / IA

---

## 📄 Licence

Projet destiné à un usage éducatif et portfolio.
