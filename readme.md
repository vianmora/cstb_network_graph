 # Le graphique des projets RGP
 
 ## Quelques liens utiles

[Site pour visualiser le graphique](https://vmorain.perso.centrale-marseille.fr/)  
[Fiche de cadrage](https://cstbgroup.sharepoint.com/:w:/r/sites/01_INT_DEE_Division_RGP_306/_layouts/15/Doc.aspx?sourcedoc=%7B133641E9-1129-4C1C-9772-6DC3CC8F89D3%7D&file=diagramme%20de%20l%27%C3%A9quipe%20-%20cadrage.docx&action=default&mobileredirect=true)

## Pour reproduire le graph

1) forker le repo
2) créer un fichier `secrets.yml` avec la clé d'API de l'airtable et l'identifiant de la table

```
api_key: {api_key}
rgp_base_id: {rgp_base_id}
```

3) lancer le notebook python `play_with_airtable.ipynb`

Le notebook utilise les librairies : 
- pyvis
- airtable
- os

## TODO si on veut améliorer le graph :

- [ ] Transformer les bulles "agent" avec la photo
- [ ] Trouver un moyen de l'incorporer sur le sharepoint
- [ ] Le convertir pour faire directement du javascript
- [ ] Faire des vues outils en plus de la vue projet
