# Hangman online

## TODO

Tout n'est pas forcément faisable dans le temps imparti. Il faut au moins faire un todo Non-fonctionnel et un todo Fonctionnel.

Le Non-fonctionnel est plus prioritaire que le Fonctionnel. La liste des TODO dans les sections Non-fonctionnel et Fonctionnel ne sont pas triés par ordre de priorité ou de valeur.

- Non-fonctionnel (prioritaire):
  - Rendre le jeu "online". La CLI utilise l'adapter python, ce serait bien qu'elle utilise l'API pour que le jeu soit vraiment "online"
  - Créer un "micro-service" pour gérer la liste de mots disponibles. Lorsqu'on aura 10 millions de joueurs concurrents, on veut pouvoir scaler de façon indépendante le moteur de jeu et la gestion des mots
  - Implémenter la persistance à long terme des parties. On ne veut pas perdre les données des parties en cours si le serveur redémarre
- Fonctionnel (moins prioritaire):
  - Permettre au joueur de consulter son palmarès/ses parties précédentes
  - Créer un classement entre joueurs
  - Pouvoir sélectionner la taille du mot à deviner
  - Ne plus pouvoir tricher
  - Pouvoir ajouter/supprimer des mots dans la liste des mots disponibles (admin seulement)


## Utilisation

Démarrer la CLI en python local
```bash
python hangman/cli.py hangman
```

Démarrer l'API en python local
```bash
python hangman/api.py
```

Démarrer la CLI en docker
```bash
docker compose run -it hangman-cli 
```

Démarrer l'API en docker
```bash
docker compose up -d hangman-api 
```

Ajouter un mot
```bash
python hangman/cli.py words -a myword
```

Supprimer un mot
```bash
python hangman/cli.py words -d <my_word>
```

Voir le profil d'un joueur
```bash
python hangman/cli.py player <player_name>
```

Voir le classement
```bash
python hangman/cli.py top
```