# Check-IA

Check-IA est une plateforme de **vérification des faits basée sur l'IA**. Le projet est structuré en deux parties :

- `backend/` : API Django + Django REST Framework, authentification JWT, PostgreSQL.
- `mobile/` : application React Native avec Expo, navigation Auth + onglets principaux.

## 1) Architecture du projet

```text
fact_check_datasets/
├── backend/
│   ├── checkia/                 # Configuration Django (settings, urls, wsgi, asgi)
│   ├── accounts/                # Gestion utilisateur (Custom User + profil)
│   ├── facts/                   # Vérifications de faits (FactCheck)
│   ├── media_analysis/          # Fichiers médias et scoring deepfake (MediaFile)
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
└── mobile/
    ├── App.js
    ├── app.json
    ├── package.json
    └── src/
        ├── navigation/          # RootNavigator, AuthNavigator, MainTabs
        ├── screens/auth/        # Login, Register
        ├── screens/main/        # Home, Scan, History, Profile
        └── components/
```

## 2) Backend (Django + DRF)

### Apps incluses

1. **accounts**
   - `User` custom (hérite de `AbstractUser`)
   - Champs de base : `role`, `bio`, `avatar_url`
   - Endpoints de profil utilisateur.

2. **facts**
   - Modèle `FactCheck` pour stocker la vérification d'un contenu (article/blog/image/vidéo/audio)
   - Verdict IA (`true`, `false`, `mixed`, `unknown`) + score de confiance.

3. **media_analysis**
   - Modèle `MediaFile` relié à un `FactCheck`
   - Support image/vidéo/audio, statut d'analyse et `deepfake_score`.

### Authentification

- JWT avec `djangorestframework-simplejwt`
- Endpoints :
  - `POST /api/auth/token/`
  - `POST /api/auth/token/refresh/`

### Base de données

- PostgreSQL (configurable via variables d'environnement dans `.env.example`)

### Installation backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API disponible sur `http://127.0.0.1:8000/`.

## 3) Mobile (React Native + Expo)

### Navigation initiale

- **Auth Stack**
  - `LoginScreen`
  - `RegisterScreen`
- **Main Tabs**
  - `Home`
  - `Scan`
  - `History`
  - `Profile`

`RootNavigator` bascule entre Auth et Main (flag `isAuthenticated` à connecter au state réel plus tard).

### Installation mobile

```bash
cd mobile
npm install
npm run start
```

Puis lancer sur simulateur ou Expo Go:
- `npm run android`
- `npm run ios`
- `npm run web`

## 4) Étapes suivantes recommandées

1. Connecter les écrans mobile à l'API Django (Axios + gestion du token JWT).
2. Ajouter des endpoints d'analyse IA (`OpenAI API` + pipeline deepfake).
3. Mettre en place la file de tâches (Celery + Redis) pour traitements médias longs.
4. Ajouter upload média sécurisé (S3 ou stockage objet), pagination historique, filtres.
5. Ajouter tests backend (`pytest-django`) et tests mobile (`jest` + `react-native-testing-library`).

## 5) Notes IA & Deepfake

Cette étape initialise les structures de données et les écrans. L'intégration des modèles IA (OpenAI et détection deepfake) sera branchée dans les services backend de `facts` et `media_analysis` à l'étape suivante.
