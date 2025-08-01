# Mini Simulio - Test Technique
## ⚙️ Introduction
Bienvenue dans le projet Mini Simulio, une version simplifiée du simulateur Simulio.

Ce projet est une API backend développée avec FastAPI et une base de données MySQL. Il permet à un utilisateur authentifié de se connecter et d'effectuer des simulations.

## 🎯 Fonctionnalités
- #### Authentification (connexion via JWT)

## 📦 Technologies utilisées
- Python 3.11+

- FastAPI (framework web)

- Uvicorn (serveur ASGI)

- SQLAlchemy (ORM)

- PyMySQL (driver MySQL)

- Passlib[bcrypt] (hachage sécurisé des mots de passe)

- python-jose (gestion JWT)

- python-multipart (upload / formulaire multipart)

- cryptography (sécurité)


## 🚀 Installation & Lancement (version manuelle, sans Docker)
#### 🔧 Prérequis
- Python 3.11+
- MySQL installé et en fonctionnement
- Git
- Node.js

#### 🧭 Étapes de configuration manuelle
### 1. Cloner le dépôt
bash
Copier
```
git clone https://github.com/Kae134/Simulio/edit/main/
cd Simulio
```
### 2. Configurer la base de données MySQL
Lancer MySQL et exécuter :

```sql
    CREATE DATABASE IF NOT EXISTS simulio CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON simulio.* TO 'user'@'localhost';
    FLUSH PRIVILEGES;
```
#### Importer les données depuis le dump :

```bash
mysql -u user -p mini_simu < dump.sql
```

### 3. Configurer et lancer le backend

#### Aller dans le dossier backend :

```bash
cd backend
Créer un fichier .env à la racine du dossier backend avec le contenu suivant :
```

```ini
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mini_simu
SECRET_KEY=une_chaine_secrete_pour_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Créer un environnement virtuel et activer :

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Installer les dépendances :

```bash
pip install -r requirements.txt
```

#### Lancer le serveur FastAPI :

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
L’API est maintenant accessible à : http://localhost:8000

### 4. Lancer le frontend
#### Aller dans le dossier frontend :

```bash
cd ../frontend
```

#### Installer les dépendances :

```bash
npm install
```

#### Lancer le serveur de développement :

```bash
npm run dev --host
```
Le frontend sera alors accessible sur http://localhost:5173

## 📋 Endpoints importants
| Route                    | Méthode | Description                                  | Authentification requise |
| ------------------------ | ------- | -------------------------------------------- | ------------------------ |
| `/login`                 | POST    | Connexion utilisateur (retourne JWT)         | Non                      |
| `/simulate`              | POST    | Lancer une simulation                        | Oui                      |
| `/clients`               | POST    | (Bonus) Créer un client                      | Oui                      |
| `/clients/{id}/simulate` | POST    | (Bonus) Attribuer une simulation à un client | Oui                      |

## 📄 Scripts SQL
Le fichier dump.sql contient la structure et les données nécessaires pour initialiser la base MySQL.
