# gestafEvolution

Ce repo sert à sauvegarder le code utilisé pour générer les graphs d'équipe.

Vous pouvez contribuer en :
- Ouvrant un [nouveau ticket](https://scm.cstb.fr/dee/rgp/gestafevolution/-/issues/new) si vous souhaitez faire un commentaire, envoyer des mots doux ou faire une proposition d'amélioration
- Clone le repo chez vous et faire une merge request si vous souhaitez apporter des améliorations par vous-même ;) 

## Premiers pas dans le code

1) Cloner le repo : `git clone https://{token_name}:{token}@scm.cstb.fr/dee/rgp/gestafevolution.git`
2) Insérer un fichier secrets.yml dans le dossier app/src en vous inspirant du fichier secrets_template.yml déjà existant (il sert à enregistrer les tockens d'accès à Airtable)
3) Lancer la commande `python app.py` pour lancer le serveur Flask en mode dev
4) Le code javascript qui génère le graph est dans `static/js/app.js`. Il utilise les données envoyées par la route api/data (configurée dans app.py)

