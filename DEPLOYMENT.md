# Déploiement production Check-IA

Ce document décrit le déploiement complet de :

- **Backend Django/DRF** sur **Railway**
- **Mobile React Native Expo** via **EAS Build** (APK Android)

---

## 1) Prérequis

- Compte Railway
- Compte Expo (EAS)
- Repo GitHub connecté
- Projet backend et mobile fonctionnels en local

---

## 2) Déploiement backend sur Railway

### 2.1 Fichiers utilisés

- `railway.json`
- `backend/Procfile`
- `backend/build.sh`
- `backend/.env.production.example`
- `backend/checkia/settings.py`

### 2.2 Créer le service Railway

1. Aller sur https://railway.app
2. Créer un nouveau projet
3. Sélectionner **Deploy from GitHub repo**
4. Choisir le repository `fact_check_datasets`
5. Ajouter un plugin **PostgreSQL** dans le projet Railway

### 2.3 Variables d'environnement Railway

Définir ces variables dans le service backend :

```env
DEBUG=False
SECRET_KEY=change-me-with-a-long-random-secret
DATABASE_URL=postgresql://postgres:password@host:5432/railway
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
ALLOWED_HOSTS=check-ia-backend.railway.app
CORS_ALLOWED_ORIGINS=https://check-ia.expo.dev,https://check-ia.app
```

### 2.4 Build et démarrage

Railway va :

1. Installer les dépendances Python de `backend/requirements.txt`
2. Exécuter le script de build :
   ```bash
   cd backend
   ./build.sh
   ```
3. Lancer le serveur web :
   ```bash
   cd backend && gunicorn checkia.wsgi --bind 0.0.0.0:$PORT
   ```

### 2.5 Vérifications post-déploiement

- Ouvrir l'URL publique Railway
- Vérifier que l'API répond (ex: `/api/`)
- Vérifier que les migrations sont passées
- Vérifier que CORS autorise bien l'app mobile

---

## 3) Déploiement mobile Expo avec EAS (APK)

### 3.1 Fichiers utilisés

- `mobile/eas.json`
- `mobile/app.json`
- `mobile/.env.example`
- `mobile/src/services/api.js`

### 3.2 Préparer Expo/EAS

Dans `mobile/` :

```bash
npm install
npm install -g eas-cli
```

Se connecter :

```bash
eas login
```

Configurer l'environnement local :

```bash
cp .env.example .env
```

Vérifier la valeur :

```env
EXPO_PUBLIC_API_URL=https://check-ia-backend.railway.app/api
```

### 3.3 Configuration de build

Le profil `preview` dans `mobile/eas.json` génère un APK Android :

```json
{
  "build": {
    "preview": {
      "android": {
        "buildType": "apk"
      }
    }
  }
}
```

### 3.4 Lancer le build APK

```bash
cd mobile
eas build -p android --profile preview
```

### 3.5 Récupérer et tester l'APK

- Ouvrir le lien renvoyé par EAS
- Télécharger l'APK
- Installer sur appareil Android
- Tester : login, scan, historique, profil

---

## 4) Commandes utiles

### Backend local (prod-like)

```bash
cd backend
export DEBUG=False
export SECRET_KEY='replace-me'
export DATABASE_URL='postgresql://...'
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn checkia.wsgi --bind 0.0.0.0:8000
```

### Mobile build rapide

```bash
cd mobile
eas build:list
eas build -p android --profile preview
```

---

## 5) Checklist finale

- [ ] Variables Railway configurées
- [ ] Domaine backend présent dans `ALLOWED_HOSTS`
- [ ] Domaine mobile présent dans `CORS_ALLOWED_ORIGINS`
- [ ] Migrations appliquées
- [ ] Fichiers statiques collectés
- [ ] APK généré via EAS
- [ ] Flux auth + API validé depuis l'app Android
