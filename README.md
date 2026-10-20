# SK — Mode & élégance

Landing page de vente SK (pièces uniques, livraison à Conakry, commande sur WhatsApp).

- `index.html` : la page complète (aucune installation nécessaire)
- `photos/` : photos des tenues et des clientes
- `logo-sk*` : logo SK (monogramme couture), dont la version ronde pour les photos de profil

## Mettre à jour

- **Pièce vendue** : dans `index.html`, en bas, `const VENDUES = [];` → ajouter son numéro, ex. `[3]` ou `[3, 7]`. La fiche affiche « Vendue ».
- **Numéro WhatsApp** : ligne `const WHATSAPP = '224614903303';`.
- **Liens de pub suivis** : ajouter `?src=fb` ou `?src=tiktok` à l'adresse du site ; la référence apparaît dans chaque message WhatsApp reçu.

## Mise en ligne

Netlify → « Import a Git repository » → GitHub → ce dépôt. Pas de commande de build, dossier de publication : la racine.
