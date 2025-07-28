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

## 🚀 Installation & lancement
Prérequis
- Python 3.11+

- MySQL (base de données)

- Git

### Étapes
#### Cloner le dépôt :

```bash
git clone https://github.com/ton-utilisateur/mini-simulio.git
cd mini-simulio
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

#### Importer la base de données MySQL :

```bash
mysql -u user -p nom_de_la_base < dump.sql
```
#### Configurer les variables d’environnement (fichier .env) :

```ini
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/mini_simu
SECRET_KEY=une_chaine_secrete_pour_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Lancer le serveur de développement :

```bash
uvicorn app.main:app --reload
```
#### L'API sera accessible à l'adresse : http://localhost:8000

## 📋 Endpoints importants
| Route                    | Méthode | Description                                  | Authentification requise |
| ------------------------ | ------- | -------------------------------------------- | ------------------------ |
| `/login`                 | POST    | Connexion utilisateur (retourne JWT)         | Non                      |
| `/simulate`              | POST    | Lancer une simulation                        | Oui                      |
| `/clients`               | POST    | (Bonus) Créer un client                      | Oui                      |
| `/clients/{id}/simulate` | POST    | (Bonus) Attribuer une simulation à un client | Oui                      |

## 📄 Scripts SQL
Le fichier dump.sql contient la structure et les données nécessaires pour initialiser la base MySQL.