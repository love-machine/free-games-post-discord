# 🎮 Free Games Bot

Un bot Discord qui surveille automatiquement les jeux gratuits sur **Epic Games** et **Steam**, et envoie une notification dès qu'un jeu est disponible gratuitement — sans jamais notifier deux fois le même jeu.

Conçu pour tourner **gratuitement et automatiquement** via **GitHub Actions**, sans serveur.

---

## ✨ Fonctionnalités

- 🟣 Détecte les jeux gratuits sur l'**Epic Games Store**
- 🔵 Détecte les jeux à **-100%** sur **Steam**
- 📨 Envoie une notification Discord avec le nom du jeu, le lien et l'image
- 🗄️ Historique SQLite pour éviter les doublons de notifications
- 🧹 Nettoyage automatique des entrées de plus de 30 jours
- ⚙️ Exécution automatique toutes les 6 heures via GitHub Actions
- 🪶 Léger, robuste et avec gestion des erreurs réseau

---

## 📋 Prérequis

- Python 3.8+
- Un compte **GitHub** (pour l'automatisation via Actions)
- Les bibliothèques suivantes :

```bash
pip install requests python-dotenv
```

> `sqlite3` est inclus dans la bibliothèque standard Python.

---

## 🗂️ Structure du projet

```
.
├── main.py                        # Script principal
├── requirements.txt               # Dépendances Python
├── .env                           # Variables d'environnement (non versionné)
├── .github/
│   └── workflows/
│       └── check_games.yml        # Workflow GitHub Actions
└── historique_jeux.db             # Base SQLite (créée automatiquement, versionnée)
```

---

## ⚙️ Configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/free-games-bot.git
cd free-games-bot
```

### 2. Créer le webhook Discord

1. Aller dans les paramètres d'un salon Discord
2. **Intégrations** → **Webhooks** → **Créer un webhook**
3. Copier l'URL

### 3. Ajouter le secret GitHub

Dans ton dépôt GitHub :

1. **Settings** → **Secrets and variables** → **Actions**
2. Cliquer sur **New repository secret**
3. Nom : `DISCORD_WEBHOOK`, Valeur : l'URL copiée

> Le workflow lit automatiquement ce secret via `${{ secrets.DISCORD_WEBHOOK }}`.

### 4. (Optionnel) Fichier `.env` pour usage local

```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/VOTRE_WEBHOOK_ICI
```

---

## 🚀 Utilisation

### En local

```bash
python main.py
```

### Via GitHub Actions (automatique)

Le workflow `check_games.yml` se déclenche :
- ⏰ **Automatiquement** toutes les 6 heures
- 🖱️ **Manuellement** depuis l'onglet **Actions** de ton dépôt via le bouton *Run workflow*

À chaque exécution, GitHub Actions :
1. Installe Python et les dépendances
2. Lance `main.py` avec le webhook en variable d'environnement
3. Commit et push la base `historique_jeux.db` pour persister l'historique entre les exécutions

> Le commit de sauvegarde inclut `[skip ci]` pour éviter de déclencher une nouvelle exécution en boucle.

---

## 🔔 Exemple de notification Discord

```
🎁 EPIC GAMES : Nom du jeu est GRATUIT !
https://cdn.epicgames.com/.../image.png
```

```
🎁 STEAM : Nom du jeu est GRATUIT !
https://store.steampowered.com/app/12345
https://cdn.akamai.steamstatic.com/.../header.jpg
```

---

## 🧠 Fonctionnement interne

### Démarrage
1. Chargement du `.env` via `python-dotenv`
2. Connexion à la base SQLite `historique_jeux.db` (création automatique si absente)
3. Nettoyage des entrées de plus de 30 jours

### Epic Games
1. Appel à l'API publique d'Epic Games avec les paramètres `locale=fr`, `country=FR`
2. Parcours de tous les éléments du catalogue
3. Si `discountPrice == 0` et jeu non déjà notifié → notification envoyée
4. Clé d'unicité : `EPIC_<nom_du_jeu>`

### Steam
1. Appel à l'endpoint `featuredcategories` de l'API Steam
2. Lecture de la catégorie `specials` (promotions en cours)
3. Si `discount_percent == 100` et jeu non déjà notifié → notification envoyée
4. Clé d'unicité : `STEAM_<app_id>`

---

## ⚠️ Limitations connues

- **Steam** : l'endpoint `featuredcategories` ne liste que les promotions mises en avant, certains jeux gratuits ponctuels peuvent être manqués.
- **Epic Games** : l'API utilisée est publique mais non officielle, elle peut évoluer sans préavis.
- **GitHub Actions** : le dépôt doit être **public**, ou avoir un abonnement GitHub payant pour bénéficier des minutes Actions gratuites sur un dépôt privé.

---

## 📄 Licence

Ce projet est personnel et non officiel. Il n'est pas affilié à Epic Games, Valve ni GitHub.