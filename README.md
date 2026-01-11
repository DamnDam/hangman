# Hangman online

## Utilisation

Installer le package
```bash
pip install git+https://github.com/DamnDam/hangman.git
```

Démarrer la CLI en python local
```bash
hangman play
```

Démarrer l'API en python local
```bash
uvicorn hangman.api:api --port 8000
```

Ajouter un mot
```bash
hangman words -a <my_word>
```

Supprimer un mot
```bash
hangman words -d <my_word>
```

Voir le profil d'un joueur
```bash
hangman player <player_name>
```

Voir le classement
```bash
hangman top
```

Démarrer la CLI en docker
```bash
docker compose run --rm hangman-cli <command> <options>
```

Démarrer l'API en docker
```bash
docker compose up -d hangman-api
```

## Développement

### Devcontainer

Ouvrir le projet dans VScode, installer l'extension officielle "Dev Container".
Le projet s'initialise avec UV, Python, et toutes ses dépendances dans un container dédié.
Le container est basé sur Debian, l'interface vers le Docker du système hôte est fournie.

### UV

UV est le gestionaire de projet Python le plus avancé à ce jour. 
https://docs.astral.sh/uv/#installation

Pour rebuilder le projet
```bash
uv sync
```

Par défaut, UV va créer un virtual env automatiquement.
On peut alors l'activer dans son shell, ou bien utiliser les commandes managées UV

Lancer une commande dans le contexte du projet UV
```bash
uv run hangman
```

Mettre à jour les sous-dépendances
```bash
uv lock --upgrade
```

Ajouter une dépendance
```bash
uv add <package>
```